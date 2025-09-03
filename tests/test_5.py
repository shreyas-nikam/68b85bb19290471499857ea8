import pytest
from definition_3b09245242124c0486d9136daca9a77f import extract_5ws
import pandas as pd

@pytest.mark.parametrize("case_data, expected", [
    (pd.DataFrame({'Who': ['John Doe'], 'What': ['Suspicious Transaction'], 'When': ['2024-01-01'], 'Where': ['New York'], 'Why': ['Unexplained Wealth']}), {'Who': ['John Doe'], 'What': ['Suspicious Transaction'], 'When': ['2024-01-01'], 'Where': ['New York'], 'Why': ['Unexplained Wealth']}),
    ({}, {}),
    (pd.DataFrame(), {}),
    ({'transaction_details': 'Large cash deposit'}, {}),
    ([1, 2, 3], TypeError)
])

def test_extract_5ws(case_data, expected):
    try:
        if isinstance(case_data, list):
            with pytest.raises(TypeError):
                extract_5ws(case_data)
        else:
            result = extract_5ws(case_data)
            if isinstance(case_data, pd.DataFrame) and case_data.empty:
                assert result == {}
            elif isinstance(case_data, dict) and case_data == {}:
                assert result == {}
            elif isinstance(case_data, dict) and 'transaction_details' in case_data:
                 assert result == {}
            else:
                assert result == {'Who': ['John Doe'], 'What': ['Suspicious Transaction'], 'When': ['2024-01-01'], 'Where': ['New York'], 'Why': ['Unexplained Wealth']} if isinstance(case_data, pd.DataFrame) else {}


    except Exception as e:
        assert isinstance(e, type(expected))
