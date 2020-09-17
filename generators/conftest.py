# set up a hook to be able to check if a test has failed
import logging
import subprocess
import sys

import pytest

parameters = []


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


def pytest_generate_tests(metafunc):
    if "db" in metafunc.fixturenames:
        metafunc.parametrize("db", parameters, indirect=True)


@pytest.fixture
def db(request):

    for i in range(10):
        parameters.append((i, i + 1))