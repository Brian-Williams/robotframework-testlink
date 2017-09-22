from robottestlink.utils import get_param_from_robot
from testlink import TestLinkHelper


class RobotTestLinkHelper(TestLinkHelper):
    """
    We preface all testlink inputs with 'testlink'.

    So, to pass the serverurl as a variable in a robot test set the variable ${testlinkserverurl}.

    This is to avoid polluting the robot framework variable namespace with common variable names.
    """

    def _setParamsFromRobot(self):
        """
        fill empty slots from robot variables
        _server_url <- TESTLINK_API_PYTHON_SERVER_URL <- robot_variable`testlinkserverurl`
        _devkey     <- TESTLINK_API_PYTHON_DEVKEY     <- robot_variable`testlinkdevkey`
        _proxy      <- http_proxy                     <- robot_variable`testlinkproxy`

        If robot variables are not defined, values are kept as None for other _setParams* to handle.
        """
        if self._server_url is None:
            self._server_url = get_param_from_robot('testlinkserverurl')
        if self._devkey is None:
            self._devkey = get_param_from_robot('testlinkdevkey')
        if not self._proxy:
            self._proxy = get_param_from_robot('testlinkproxy')

    # Remove this and use commented below override when pull #24 goes through
    def _setParamsFromEnv(self):
        self._setParamsFromRobot(),
        super(RobotTestLinkHelper, self)._setParamsFromEnv()
    
    # This is dependant on https://github.com/orenault/TestLink-API-Python-client/pull/24
    # def _setParams(self):
    #     """fill slots _server_url, _devkey and _proxy
    #     Priority:
    #     1. init args
    #     2. robot variables
    #     2. environment variables
    #     3. default values
    #     """
    #     self._setParamsFromRobot()
    #     super(RobotTestLinkHelper, self)._setParams()
