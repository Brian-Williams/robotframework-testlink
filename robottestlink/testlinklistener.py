from robot.api import logger as robot_logger
from testlink import TestlinkAPIClient
from testlink.testreporter import TestGenReporter
from robottestlink.utils import update_missing_params_from_robot_variables
from .parsers import MultiParser, TestDocParser, TestNameParser
from .robottestlinkhelper import RobotTestLinkHelper


class testlinklistener(object):
    ROBOT_LISTENER_API_VERSION = 3
    PARSERS = [TestDocParser, TestNameParser]

    def __init__(self, server_url=None, devkey=None, proxy=None, *report_kwargs):
        """
        This is specifically for looking at testcaseexternalids in testcase documentation and sending results to all
        testcases found.

        If you would like to set a default input from the test itself you can add 'testlink' to the beginning of the
        parameter and it will select and add if it wasn't passed in at __init__.
        For example if you wanted to pass in the platformname you would set testlinkplatformname. This is to avoid
        robot name collisions with incredibly common variable names like user and timestamp.
        Note: dev_key is set during testlink connection and used as a default by the testlink library.
              So, if `testlinkdevkey` is passed in it will effectively take priority as the second positional arg
              dev_key is *not* put into report_kwargs. This is by design.

        Since kwargs are not supported in listeners you must pass in args with an equal sign between the key and the
        value (<argument>=<value). Arguments or values with equal signs in them are not supported.

        :param server_url: The testlink server
        :param devkey: API key of the user running the tests
        :param proxy: Testlink proxy
        :param report_kwargs: These are args in the format `<argument>=<value>`. These values are assumed parameters
                              for reportTCResults with the following special cases:
            - also_console: Whether to log the reportTCResults response to console; boolean, deafults to True
            - test_prefix: The letters preceding testlink numbers. ex. abc-1234 the test_prefix would be 'abc'
        """
        self.server = server_url
        # Allow for string None for CLI input
        self.devkey = devkey if devkey != 'None' else None
        self.proxy = proxy if proxy != 'None' else None

        # Listeners don't support real kwargs
        self.report_kwargs = {}
        for kwarg in report_kwargs:
            try:
                arg, value = kwarg.split('=')
            except ValueError:
                raise RuntimeError("Report kwarg was passed in without equal sign. '{}'".format(kwarg))
            if isinstance(value, list):
                raise RuntimeError("Report kwarg was passed in with multiple equal signs. '{}'".format(kwarg))
            self.report_kwargs[arg] = value

        self.also_console = self.report_kwargs.pop('also_console', True)
        self.test_prefix = self.report_kwargs.pop('test_prefix', None)

        self._tlh = self._tls = None

    @property
    def tlh(self):
        if not self._tlh:
            self._make_testlinkhelper()
        return self._tlh

    def _make_testlinkhelper(self):
        self._tlh = RobotTestLinkHelper(self.server, self.devkey, self.proxy)

    @property
    def tls(self):
        if not self._tls:
            self._tls = self.tlh.connect(TestlinkAPIClient)
        return self._tls

    def _get_testcases(self, test):
        # Needs to be a list to marshal
        return list(MultiParser(*[parser(self.test_prefix) for parser in self.PARSERS]).get_testcases(test))

    def _get_testlink_status(self, test):
        # testlink accepts p/f for passed and failed
        status = 'f'
        if test.passed:
            status = 'p'
        return status

    def _get_robot_values(self, test):
        update_missing_params_from_robot_variables(self.report_kwargs)
        self.report_kwargs['status'] = self._get_testlink_status(test)
        return self._get_testcases(test)

    def _get_reporter(self, test):
        """Update kwargs and get TestReporter"""
        testcases = self._get_robot_values(test)
        return TestGenReporter(self.tls, testcases, **self.report_kwargs)

    def end_test(self, data, test):
        reporter = self._get_reporter(test)
        # This is supposed to default to true by the API spec, but doesn't on some testlink versions
        # rkwargs.setdefault('guess', True)
        for result in reporter.reportgen():
            # Listeners don't show up in the log so setting also_console to False effectively means don't log
            robot_logger.info(result, also_console=self.also_console)
