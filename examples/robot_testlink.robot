*** Settings ***
Documentation    This shows the basics of required variables and documentation for organization's testlink listener.
...   Suggested input location:
...     From robot:
...       1.  'abc-<testcase number>` in the test's documentation or test name
...       2.  testlinkplatform as variable ${testlinkplatformname} in the test
...           * Note this is because <org> uses the same tests against multiple platforms. The VariableFiles set the
...             testlinkplatform by the inventory used.
...     From CLI:
...       3.  testlinktestplanname name or id
...       4.  testlinkbuildname (most likely provided by Jenkins)
...
...   The testlink variables can be defined from the command line as a varaible, imported as a resource, set by a test
...   or set in the variables tab as long as it is set before the test ends.
...   Here is an example with org's testlink listener:
...     `robot --listener "reportlink:testplanname=Example1:testlinkbuildname=1" robot_testlink.robot`

*** Variables ***
${testlinkplatformname}    Exampleplatform

*** Test Cases ***
Report a testcase
    [Documentation]  abc-123: Other text can be here too.
    log to console   \nThis will report to testlink with planname: ${testlinkplatformname}

A test without documentation
    log to console  \nThis won't send anything to testlink

# Example Pass Output:
# robot --listener "reportlink:testplanname=Example1:buildname=1" robot_testlink.robot
#==============================================================================
#Robot Testlink :: This shows the basics of required variables and documenta...
#==============================================================================
#Report a testcase :: abc-123
#This will report to testlink with planname: Exampleplatform
#.[{'status': True, 'operation': 'reportTCResult', 'message': 'Success!', 'overwrite': False, 'id': '56923'}]
#Report a testcase :: abc-123                                          | PASS |
#------------------------------------------------------------------------------
#A test without documentation
#This won't send anything to testlink
#A test without documentation                                          | PASS |
#------------------------------------------------------------------------------
#Robot Testlink :: This shows the basics of required variables and ... | PASS |
#2 critical tests, 2 passed, 0 failed
#2 tests total, 2 passed, 0 failed
#==============================================================================
#Output:  /home/app/examples/output.xml
#Log:     /home/app/examples/log.html
#Report:  /home/app/examples/report.html