# Robottestlink listener
This is an alternative to robotframework testlink libraries.

It instead uses a listener, which can gather the test information from
robot and then can either update testcases with the information it
found or alternatively try to idempotently create the inputs and
then send.
