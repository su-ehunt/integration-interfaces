from typing import Dict
from package_testers.test_protocol import EndpointUnitTester
from package_testers.endpoint_tests import tests
from src.integration_interfaces.logging import log

results = {}

def run_tests(tests):
    failure = False
    for test in tests:
        result = run_test(test)
        results[test] = result
        if result[0] == True:
            failure = True
    summarize(results)
    if failure == True:
        log.error("Failure encountered while running package tests")
        raise RuntimeError("Failure encountered while running package tests.")
        

def run_test(test:EndpointUnitTester):
    try:
        test.run_tests()
        failure = False
    except Exception as e:
        log.error(f"Exception Encountered while running {test.info()}")
        log.exception(e)
        failure = True
    return (failure,test.info())

def summarize(results):
    pass