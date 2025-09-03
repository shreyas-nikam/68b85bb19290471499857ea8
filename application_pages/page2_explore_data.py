
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from collections import Counter

def create_timeline_visualization(transactions):
    """Generates an interactive timeline visualization of transaction data.

    Args:
        transactions (Pandas DataFrame): DataFrame with 'timestamp' and 'transaction_amount' columns.

    Returns:
        plotly.graph_objects.Figure: Plotly figure object representing the timeline.
    """
    if not isinstance(transactions, pd.DataFrame):
        raise TypeError("transactions must be a Pandas DataFrame")

    if 'timestamp' not in transactions.columns:
        raise KeyError("timestamp column missing")

    if len(transactions) == 0:
        fig = go.Figure()
        fig.update_layout(title="Transaction Timeline")
        return fig

    if not pd.api.types.is_datetime64_any_dtype(transactions['timestamp']):
        raise TypeError("timestamp column must be datetime objects")

    if 'transaction_amount' in transactions.columns:
        fig = px.line(transactions, x='timestamp', y='transaction_amount', title='Transaction Timeline: Amount Over Time')
    else:
        transactions['count'] = 1
        transactions_by_time = transactions.groupby('timestamp')['count'].sum().reset_index()
        fig = px.line(transactions_by_time, x='timestamp', y='count', title='Transaction Timeline: Number of Transactions Over Time')


    return fig


def create_geo_map_visualization(transactions):
    """Generates a geographic map visualization of transaction origins and destinations.

    Args:
        transactions (Pandas DataFrame): DataFrame with transaction data, including
                                      'origin_latitude', 'origin_longitude',
                                      'destination_latitude', 'destination_longitude', and 'transaction_amount' columns.

    Returns:
        A Plotly figure object.
    """

    if transactions.empty:
        print("Transactions DataFrame is empty. Cannot create geo map.")
        return go.Figure()

    required_columns = ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude', 'transaction_amount']
    for col in required_columns:
        if col not in transactions.columns:
            raise KeyError(f"Column '{col}' missing in DataFrame. Please ensure synthetic data includes these or add dummy values.")

    # Check if lat/lon columns are numeric
    for col in ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude']:
        if not pd.api.types.is_numeric_dtype(transactions[col]):
            raise TypeError(f"Column '{col}' must contain numeric data.")

    fig = go.Figure(data=go.Scattergeo(
        lon=transactions['origin_longitude'],
        lat=transactions['origin_latitude'],
        mode='markers',
        marker=dict(
            size=transactions['transaction_amount'] / transactions['transaction_amount'].max() * 20,  # Scale marker size by amount
            opacity=0.8,
            reversescale=True,
            symbol='circle',
            line=dict(
                width=0,
                color='rgba(102, 102, 102)'
            ),
            sizemode='area',
        ),
        text=[f"Amount: {amount:,.2f}" for amount in transactions['transaction_amount']],
    ))

    fig.update_layout(
        title_text='Transaction Origins (Marker Size ~ Amount)',
        geo=dict(
            scope='world',
            showland=True,
            landcolor="rgb(217, 217, 217)",
        )
    )

    return fig


def create_counterparty_network_graph(transactions):
    """Creates a network graph of transaction counterparties.

    Args:
        transactions (Pandas DataFrame): DataFrame with transaction data,
                                      expected to have 'Source' and 'Target' columns.

    Returns:
        networkx.Graph: A NetworkX graph object.
    """
    graph = nx.Graph()
    if transactions.empty:
        return graph

    required_columns = ['Source', 'Target']
    for col in required_columns:
        if col not in transactions.columns:
            raise KeyError(f"Column '{col}' missing in DataFrame. Please ensure synthetic data includes these or add dummy values.")

    # Add edges to the graph
    for index, row in transactions.iterrows():
        source = row['Source']
        target = row['Target']
        if source != target: # Avoid self-loops for clearer visualization
            graph.add_edge(source, target)
    return graph


def run_page2():
    st.header(