import pytest
import pandas as pd
from definition_3b4ce43a2feb4ca88e08f830c5d3f42f import calculate_summary_kpis

@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        'customer_id': [1, 1, 2, 3, 3, 3],
        'transaction_amount': [100, 200, 150, 50, 75, 100],
    })

def test_calculate_summary_kpis_basic(sample_transactions):
    kpis = calculate_summary_kpis(sample_transactions)
    assert isinstance(kpis, dict)
    assert 'total_transaction_volume' in kpis
    assert 'average_transaction_amount' in kpis
    assert 'transactions_per_customer' in kpis
    assert kpis['total_transaction_volume'] == 675
    assert kpis['average_transaction_amount'] == 112.5
    assert kpis['transactions_per_customer'] == {1: 2, 2: 1, 3: 3}


def test_calculate_summary_kpis_empty_dataframe():
    empty_df = pd.DataFrame({'customer_id': [], 'transaction_amount': []})
    kpis = calculate_summary_kpis(empty_df)
    assert isinstance(kpis, dict)
    assert kpis['total_transaction_volume'] == 0
    assert kpis['average_transaction_amount'] == 0
    assert kpis['transactions_per_customer'] == {}

def test_calculate_summary_kpis_single_transaction(sample_transactions):
    single_transaction_df = sample_transactions.iloc[[0]]
    kpis = calculate_summary_kpis(single_transaction_df)
    assert kpis['total_transaction_volume'] == 100
    assert kpis['average_transaction_amount'] == 100
    assert kpis['transactions_per_customer'] == {1: 1}

def test_calculate_summary_kpis_different_customer_ids(sample_transactions):
    different_ids_df = pd.DataFrame({
        'customer_id': [10, 20, 30],
        'transaction_amount': [100, 200, 300],
    })
    kpis = calculate_summary_kpis(different_ids_df)
    assert kpis['transactions_per_customer'] == {10: 1, 20: 1, 30: 1}

def test_calculate_summary_kpis_large_transaction_amounts(sample_transactions):
    large_amounts_df = pd.DataFrame({
        'customer_id': [1, 2],
        'transaction_amount': [100000, 200000],
    })
    kpis = calculate_summary_kpis(large_amounts_df)
    assert kpis['total_transaction_volume'] == 300000
    assert kpis['average_transaction_amount'] == 150000
    assert kpis['transactions_per_customer'] == {1: 1, 2: 1}
