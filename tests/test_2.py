import pytest
import pandas as pd
import plotly.graph_objects as go
from definition_b43c9d8821184dc7ae132cb17717740f import create_timeline_visualization

@pytest.fixture
def sample_transactions():
    data = {'timestamp': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-02', '2023-01-03', '2023-01-04']),
            'amount': [100, 200, 150, 300, 250]}
    return pd.DataFrame(data)

def test_create_timeline_visualization_empty_dataframe():
    empty_df = pd.DataFrame({'timestamp': [], 'amount': []})
    fig = create_timeline_visualization(empty_df)
    assert isinstance(fig, go.Figure)

def test_create_timeline_visualization_valid_dataframe(sample_transactions):
    fig = create_timeline_visualization(sample_transactions)
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0

def test_create_timeline_visualization_correct_data_types():
    data = {'timestamp': ['2023-01-01', '2023-01-02'], 'amount': [100, 200]}
    df = pd.DataFrame(data)
    with pytest.raises(TypeError):
        create_timeline_visualization(df)

def test_create_timeline_visualization_missing_timestamp_column():
    data = {'amount': [100, 200]}
    df = pd.DataFrame(data)
    with pytest.raises(KeyError) as excinfo:
        create_timeline_visualization(df)
    assert "timestamp" in str(excinfo.value)

def test_create_timeline_visualization_missing_amount_column(sample_transactions):
    transactions = sample_transactions.drop('amount', axis=1)
    fig = create_timeline_visualization(transactions)
    assert isinstance(fig, go.Figure)
