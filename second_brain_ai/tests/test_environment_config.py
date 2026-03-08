import os
import pytest
from config.environment import EnvironmentConfig


def test_get_existing_env():
    os.environ["TEST_ENV"] = "value"
    assert EnvironmentConfig.get("TEST_ENV") == "value"


def test_get_default():
    assert EnvironmentConfig.get("NON_EXISTENT", "default") == "default"


def test_require_success():
    os.environ["REQUIRED_ENV"] = "ok"
    assert EnvironmentConfig.require("REQUIRED_ENV") == "ok"


def test_require_failure():
    with pytest.raises(EnvironmentError):
        EnvironmentConfig.require("MISSING_ENV")


def test_get_int():
    os.environ["INT_ENV"] = "5"
    assert EnvironmentConfig.get_int("INT_ENV") == 5


def test_get_bool():
    os.environ["BOOL_ENV"] = "true"
    assert EnvironmentConfig.get_bool("BOOL_ENV") is True