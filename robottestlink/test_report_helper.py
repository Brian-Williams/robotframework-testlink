from testlink.testlinkerrors import TLResponseError


class TestReport(dict):
    def __init__(self, tls, testcases=None, *args, **kwargs):
        """This can be given one or more testcases, but they all must have the same project, plan, and platform."""
        super(TestReport, self).__init__(*args, **kwargs)
        self.tls = tls
        self.testcases = testcases
        self._plan_testcases = None

    @property
    def testprojectname(self):
        return self.get('testprojectname')

    @property
    def testprojectid(self):
        return self.get('testprojectid')

    @property
    def testplanid(self):
        return self.get('testplanid')

    @property
    def platformname(self):
        """Return a platformname added to the testplan if there is one."""
        return self.get('platformname')

    @property
    def platformid(self):
        return self.get('platformid')

    @property
    def plan_tcids(self):
        if not self._plan_testcases:
            self._plan_testcases = set()
            tc_dict = self.tls.getTestCasesForTestPlan(self.testplanid)
            for _, platform in tc_dict.items():
                for k, v in platform.items():
                    self._plan_testcases.add(v['full_external_id'])
        return self._plan_testcases


class TestReportGenerator(TestReport):
    def __init__(self, tls, testcases=None, *args, **kwargs):
        super(TestReportGenerator, self).__init__(tls, testcases, *args, **kwargs)
        self._testplanname = self._testprojectid = self._testplanid = None

    def setup_testlink(self):
        self.ensure_testcases_in_plan()

    def ensure_testcases_in_plan(self):
        for testcase in self.testcases:
            if testcase not in self.plan_tc_ext_ids:
                self.tls.addTestCaseToTestPlan(
                    self.testprojectid, self.testplanid, testcase, self.get_latest_tc_version(testcase),
                    platformid=self.platformid
                )

    @property
    def testprojectname(self):
        if not self.get('testprojectname'):
            try:
                self['testprojectname'] = self.tls.getProjectIDByName(self['testprojectid'])
            except IndexError:
                raise RuntimeError('Need a testprojectname or id to generate other testlink arguments.')
        return self['testprojectname']

    @property
    def testprojectid(self):
        if not self.get('testprojectid'):
            try:
                self['testprojectid'] = self.tls.getTestProjectByName(self.testprojectname)['id']
            except TypeError:
                # TODO: Should we generate a testproject?
                raise

        return self['testprojectid']

    @property
    def testplanid(self):
        if not self._testplanid:
            try:
                self._testplanid = self.tls.getTestPlanByName(self.testprojectname, self.testplanname)[0]['id']
            except TypeError:
                self._testplanid = self.generate_testplanid()
        return self._testplanid

    def generate_testplanid(self):
        """This won't necessarily be able to create a testplanid. It requires a planname and projectname."""
        if 'testplanname' not in self:
            raise RuntimeError("Need testplanname to generate a testplan for results.")

        tp = self.tls.createTestPlan(self['testplanname'], self.testprojectname)
        self['testplanid'] = tp[0]['id']
        return self['testplanid']

    @property
    def platformname(self):
        """Return a platformname added to the testplan if there is one."""
        pn_kwarg = self.get('platformname')
        if pn_kwarg:
            self.generate_platformname(pn_kwarg)
        return pn_kwarg

    def generate_platformname(self, platformname):
        if platformname not in self.tls.getTestPlanPlatforms(self.testplanid):
            try:
                self.tls.createPlatform(self['testplanname'], platformname)
            except TLResponseError as e:
                if e.code == 12000:
                    # platform already exists
                    pass
                else:
                    raise
            self.tls.addPlatformToTestPlan(self.testplanid, platformname)

    @property
    def platformid(self):
        if not self.get('platformid'):
            self['platformid'] = self.getPlatformID(self.platformname, self.testprojectid)
        return self['platformid']

    def getPlatformID(self, platformname, projectid, _ran=False):
        platforms = self.tls.getProjectPlatforms(projectid)
        # key is duplicate info from key 'name' of dictionary
        for _, platform in platforms.items:
            if platform['name'] == platformname:
                return platform['id']
        else:
            if _ran:
                raise RuntimeError("Couldn't find platformid for {}.{} after creation.".format(projectid, platformname))
            self.generate_platformname(platformname)
            self.getPlatformID(platformname, projectid, _ran=True)

    @property
    def plan_tc_ext_ids(self):
        if not self._plan_testcases:
            self._plan_testcases = set()
            tc_dict = self.tls.getTestCasesForTestPlan(self.testplanid)
            for _, platform in tc_dict.items():
                for k, v in platform.items():
                    self._plan_testcases.add(v['full_external_id'])
        return self._plan_testcases

    def get_latest_tc_version(self, testcaseexternalid):
        # TODO: Remote his when PR goes through https://github.com/orenault/TestLink-API-Python-client/pull/23
        return self.tls.getTestCase(None, testcaseexternalid=testcaseexternalid)[0]['version']
