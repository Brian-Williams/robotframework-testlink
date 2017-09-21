"""Parsers that search for tests from a robot test or suite. They return a set of testcases"""
import re


class ParserFactory(object):
    pass


class _TCExternalIDParser(object):
    def __init__(self, tcid_matcher=None, tcid_matchers=None):
        """
        TCID (testcase id's) in this class refer to testcase external id prepends.

        So if the full testcase external id was 'abc-123' the tcid_matcher would be 'abc'.

        :param tcid_matcher: a tcid prefix to match.
        :param tcid_matchers: a list of tcid prefixes to match.
        """
        self.tcid_matchers = tcid_matchers if tcid_matchers is not None else []
        if tcid_matcher:
            self.tcid_matchers.append(tcid_matcher)

    def _get_testcases(self, test, matcher):
        raise NotImplementedError

    def get_testcases(self, test):
        testcases = set()
        for matcher in self.tcid_matchers:
            testcases |= set(self._get_testcases(test, matcher))
        return testcases


class TestDocParser(metaclass=_TCExternalIDParser):
    """Find all externaltestcaseid's in a test's docstring.

    If your externaltestcaseid prefix is abc and the test has 'abc-123' in it's docstring.
    `TestDocParser('abc').get_testcases(test)` would return `['abc-123']`.
    """
    def _get_testcases(self, test, matcher):
        return re.findall('{}-\d+'.format(matcher), test.doc)


class TestNameParser(_TCExternalIDParser):
    def _get_testcases(self, test, matcher):
        return re.findall('{}-\d+'.format(matcher), test.name)
