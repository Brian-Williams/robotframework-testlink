from robot.libraries.BuiltIn import BuiltIn


def get_input_as_list(input_):
    if isinstance(input_, list):
        return input_
    else:
        return [input_]


reportTCResult_PARAMS = [
    'testcaseid', 'testplanid', 'buildname', 'status', 'notes', 'testcaseexternalid', 'buildid', 'platformid',
    'platformname', 'guess', 'bugid', 'custumfields', 'overwrite', 'user', 'execduration', 'timestamp', 'steps',
    'devkey']
ADDITIONAL_PARAMS = ['testplanname']
ROBOT_REPORT_PARAMS = {str(param): 'testlink' + str(param) for param in reportTCResult_PARAMS + ADDITIONAL_PARAMS}


def setdefault_if_not_none(di, key, val):
    if key not in di:
        if val is not None:
            di[key] = val


def update_missing_params_from_robot_variables(param_dict):
    for testlink_param, robot_variable in ROBOT_REPORT_PARAMS.items():
        setdefault_if_not_none(param_dict, testlink_param, get_param_from_robot(robot_variable))


def get_param_from_robot(robot_variable):
    """Returns the found robot variable, defaults to None."""
    return BuiltIn().get_variable_value("${" + str(robot_variable) + "}")
