import pytest
import pandas as pd
import networkx as nx
from definition_7c55f3268ece4aff91975e1cca48e531 import create_counterparty_network_graph

@pytest.fixture
def sample_transactions():
    data = {'Source': ['A', 'B', 'C', 'A', 'D'],
            'Target': ['B', 'C', 'D', 'E', 'A'],
            'Amount': [100, 200, 150, 300, 250]}
    return pd.DataFrame(data)


def test_create_counterparty_network_graph_empty_dataframe():
    empty_df = pd.DataFrame({'Source': [], 'Target': [], 'Amount': []})
    graph = create_counterparty_network_graph(empty_df)
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_create_counterparty_network_graph_basic(sample_transactions):
    graph = create_counterparty_network_graph(sample_transactions)
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 5  # A, B, C, D, E
    assert len(graph.edges) == 5


def test_create_counterparty_network_graph_self_loop():
    data = {'Source': ['A', 'B', 'C'], 'Target': ['A', 'B', 'C'], 'Amount': [100, 200, 150]}
    df = pd.DataFrame(data)
    graph = create_counterparty_network_graph(df)
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 3  # Includes self-loops

def test_create_counterparty_network_graph_duplicate_transactions(sample_transactions):
    # Add a duplicate transaction to the dataframe
    duplicated_transactions = pd.concat([sample_transactions, sample_transactions.iloc[[0]]], ignore_index=True)
    graph = create_counterparty_network_graph(duplicated_transactions)
    assert isinstance(graph, nx.Graph)
    assert len(graph.nodes) == 5
    assert len(graph.edges) == 6 #Because of A->B transactions repeated.
