import pytest
import pandas as pd
from definition_bd1489d74210475a8d2d04d0a39e9f8f import load_synthetic_data

def test_load_synthetic_data_returns_dict():
    data = load_synthetic_data()
    assert isinstance(data, dict)

def test_load_synthetic_data_contains_expected_keys():
    data = load_synthetic_data()
    expected_keys = ["customers", "transactions", "alerts", "notes"]
    assert all(key in data for key in expected_keys)

def test_load_synthetic_data_values_are_dataframes():
    data = load_synthetic_data()
    for key, value in data.items():
        assert isinstance(value, pd.DataFrame)

def test_load_synthetic_data_dataframes_not_empty():
    data = load_synthetic_data()
    for key, value in data.items():
        assert not value.empty

def test_load_synthetic_data_no_error():
    try:
        load_synthetic_data()
    except Exception as e:
        pytest.fail(f"load_synthetic_data raised an exception: {e}")
