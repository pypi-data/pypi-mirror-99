#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright IBM Corp. 2010, 2020. All Rights Reserved.

import pkg_resources
import pytest
from resilient_circuits import helpers, function, ResilientComponent


def test_get_fn_names():

    class FunctionComponentA(ResilientComponent):
        @function("mock_fn")
        def _mock_function(self):
            return True

    assert helpers.get_fn_names(FunctionComponentA) == ["mock_fn"]

    class FunctionComponentB(ResilientComponent):
        @function("mock_fn_2a")
        def _other_name_a(self):
            return True

        @function("mock_fn_2b")
        def _other_name_b(self):
            return True

    assert helpers.get_fn_names(FunctionComponentB) == ["mock_fn_2a", "mock_fn_2b"]

    with pytest.raises(ValueError, match=r"Usage: @function\(api_name\)"):
        class FunctionComponentC(ResilientComponent):
            @function("mock_fn_3a", "mock_fn_3b")
            def _other_name_a(self):
                return True


def test_check_exists():
    assert helpers.check_exists("mock", {"mock": "data"}) == "data"
    assert helpers.check_exists("mock", {}) is False
    assert helpers.check_exists("mock", None) is False
    with pytest.raises(AssertionError):
        helpers.check_exists("mock", "abc")


def test_validate_configs():
    mock_configs = {
        "mock_config_1": "unicode å æ ç è é unicode",
        "mock_config_2": 11,
        "mock_config_3": "<mock_config_3_here>",
        "mock_config_4": ""
    }

    mock_required_config = {
        "required": True
    }

    mock_config_2 = {
        "required": True,
        "valid_condition": lambda x: True if x >= 1 and x <= 10 else False,
        "invalid_msg": "mock_config_2 must be in range"
    }

    mock_config_3 = {
        "required": True,
        "placeholder_value": "<mock_config_3_here>"
    }

    # test unicode
    helpers.validate_configs(mock_configs, {"mock_config_1": mock_required_config})

    # test required
    with pytest.raises(ValueError, match=r"'mock_config_5' is mandatory and is not set in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_5": mock_required_config})

    # test empty string
    with pytest.raises(ValueError, match=r"'mock_config_4' is mandatory and is not set in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_4": mock_required_config})

    # test placeholder_value
    with pytest.raises(ValueError, match=r"'mock_config_3' is mandatory and still has its placeholder value of '<mock_config_3_here>' in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_3": mock_config_3})

    # test valid_condition fails
    with pytest.raises(ValueError, match=r"mock_config_2 must be in range"):
        helpers.validate_configs(mock_configs, {"mock_config_2": mock_config_2})

    # test valid_condition passes
    mock_configs["mock_config_2"] = 5
    helpers.validate_configs(mock_configs, {"mock_config_2": mock_config_2})


def test_get_packages():

    pkgs = helpers.get_packages(pkg_resources.working_set)

    for pkg in pkgs:
        assert len(pkg) == 2
        assert isinstance(pkg[0], str)
        assert isinstance(pkg[1], str)


def test_env_str():

    env_str = helpers.get_env_str(pkg_resources.working_set)

    assert "Environment" in env_str
    assert "Python Version" in env_str
    assert "Installed packages" in env_str
    assert "\n\tresilient-circuits" in env_str


def test_remove_tag():

    mock_res_obj = {
        "tags": [{"tag_handle": "fn_tag_test", "value": None}],
        "functions": [
            {"export_key": "fn_tag_test_function", "tags": [{'tag_handle': 'fn_tag_test', 'value': None}]}
        ],
        "workflows": {
            "nested_2": [{"export_key": "fn_tag_test_function", "tags": [{'tag_handle': 'fn_tag_test', 'value': None}]}]
        }
    }

    new_res_obj = helpers.remove_tag(mock_res_obj)

    assert new_res_obj.get("tags") == []
    assert new_res_obj.get("functions", [])[0].get("tags") == []
    assert new_res_obj.get("workflows", []).get("nested_2")[0].get("tags") == []
