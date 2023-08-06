from lettuce import *
import eikon as eik
from eikon.eikonError import EikonError

__package__ = "lettuce"


@before.each_scenario
def setup_before_each_scenario(scenario):
    """Clean up variables before running each scenarios."""
    world.exception = None
    world.response = None
    eik.set_app_id('')


@step('the daemon is running')
def is_daemon_running(step):
    # TO ADD : mock an http server to simulate that the daemon is running
    pass


@step('the daemon is not running')
def daemon_is_not_running(step):
    pass


@step('application ID is set with a valid EPAID')
def set_a_valid_EPAID(step):
    eik.set_app_id("8A4AD23BBA5182D097D64F")


@step('application ID is set with an invalid EPAID')
def set_an_invalid_EPAID(step):
    eik.set_app_id("INVALID_EPAID")


@step('application ID is not set')
def EPAID_not_set(step):
    eik.set_app_id('')


@step('a JSON request is sent')
def send_a_JSON_request(step):
    payload = '{ "Analysis": [ "OHLCV"], ' \
              '"EndDate": "2015-10-01T10:00:00","StartDate": "2015-09-01T10:00:00", "Tickers": [ "EUR="]}'
    try:
        world.response = eik.send_json_request("TATimeSeries", payload)
    except EikonError as eik_error:
        world.exception = eik_error


@step('a successful response is received')
def successful_response_received(step):
    assert world.exception is None, "An Exception was raised"
    if world.exception is not None:
        assert world.response != '', "Response is empty"


@step('an exception EikonError is raised with text: "(.*)"')
def exception_raised(step, exception_message):
    assert world.exception is not None, "No exception raised"
    assert world.exception.text == exception_message, "Invalid exception message"
