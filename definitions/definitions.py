import pandas as pd
import numpy as np

def load_synthetic_data():
    """Generates synthetic data for AML analysis."""

    # Customer data
    num_customers = 100
    customer_ids = range(1, num_customers + 1)
    customer_data = {
        "customer_id": customer_ids,
        "name": [f"Customer {i}" for i in customer_ids],
        "country": np.random.choice(["USA", "Canada", "UK", "Germany", "France"], size=num_customers),
        "risk_score": np.random.randint(0, 100, size=num_customers),
    }
    customers_df = pd.DataFrame(customer_data)

    # Transaction data
    num_transactions = 500
    transaction_data = {
        "transaction_id": range(1, num_transactions + 1),
        "customer_id": np.random.choice(customer_ids, size=num_transactions),
        "amount": np.random.uniform(10, 1000, size=num_transactions),
        "timestamp": pd.date_range("2023-01-01", periods=num_transactions, freq="H"),
    }
    transactions_df = pd.DataFrame(transaction_data)

    # Alert data
    num_alerts = 50
    alert_data = {
        "alert_id": range(1, num_alerts + 1),
        "customer_id": np.random.choice(customer_ids, size=num_alerts),
        "reason": np.random.choice(["High transaction volume", "Unusual transaction location", "Suspicious activity"], size=num_alerts),
        "timestamp": pd.date_range("2023-01-05", periods=num_alerts, freq="D"),
    }
    alerts_df = pd.DataFrame(alert_data)

    # Notes data
    num_notes = 30
    note_data = {
        "note_id": range(1, num_notes + 1),
        "customer_id": np.random.choice(customer_ids, size=num_notes),
        "note": [f"Note for customer {i}" for i in range(1, num_notes + 1)],
        "timestamp": pd.date_range("2023-01-10", periods=num_notes, freq="D"),
    }
    notes_df = pd.DataFrame(note_data)

    return {
        "customers": customers_df,
        "transactions": transactions_df,
        "alerts": alerts_df,
        "notes": notes_df,
    }

import pandas as pd

def calculate_summary_kpis(transactions):
    """Calculates key performance indicators (KPIs) from transaction data."""

    total_transaction_volume = transactions['transaction_amount'].sum()
    average_transaction_amount = transactions['transaction_amount'].mean() if not transactions.empty else 0
    transactions_per_customer = transactions.groupby('customer_id').size().to_dict()

    return {
        'total_transaction_volume': total_transaction_volume,
        'average_transaction_amount': average_transaction_amount,
        'transactions_per_customer': transactions_per_customer,
    }

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_timeline_visualization(transactions):
    """Generates an interactive timeline visualization of transaction data.

    Args:
        transactions (Pandas DataFrame): DataFrame with 'timestamp' and 'amount' columns.

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
    
    if 'amount' in transactions.columns:
        fig = px.line(transactions, x='timestamp', y='amount', title='Transaction Timeline')
    else:
        transactions['count'] = 1
        transactions = transactions.groupby('timestamp').sum().reset_index()
        fig = px.line(transactions, x='timestamp', y='count', title='Transaction Timeline')
    

    return fig

import pandas as pd
import plotly.graph_objects as go

def create_geo_map_visualization(transactions):
    """Generates a geographic map visualization of transaction origins and destinations.

    Args:
        transactions (Pandas DataFrame): DataFrame with transaction data.

    Returns:
        A Plotly figure object.
    """

    if transactions.empty:
        return go.Figure()

    required_columns = ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude', 'amount']
    for col in required_columns:
        if col not in transactions.columns:
            raise KeyError(f"Column '{col}' missing in DataFrame.")

    # Check if lat/lon columns are numeric
    for col in ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude']:
        if not pd.api.types.is_numeric_dtype(transactions[col]):
            raise TypeError(f"Column '{col}' must contain numeric data.")

    fig = go.Figure(data=go.Scattergeo(
        lon=transactions['origin_longitude'],
        lat=transactions['origin_latitude'],
        mode='markers',
        marker=dict(
            size=transactions['amount'] / transactions['amount'].max() * 20,  # Scale marker size by amount
            opacity=0.8,
            reversescale=True,
            symbol='circle',
            line=dict(
                width=0,
                color='rgba(102, 102, 102)'
            ),
            sizemode='area',
        ),
        text=[f"Amount: {amount}" for amount in transactions['amount']],
    ))

    fig.update_layout(
        title_text='Transaction Origins',
        geo=dict(
            scope='world',
            showland=True,
            landcolor="rgb(217, 217, 217)",
        )
    )

    return fig

import pandas as pd
import networkx as nx

def create_counterparty_network_graph(transactions):
    """Creates a network graph of transaction counterparties."""
    graph = nx.Graph()
    if transactions.empty:
        return graph

    for index, row in transactions.iterrows():
        source = row['Source']
        target = row['Target']
        graph.add_edge(source, target)
    return graph

import pandas as pd

def extract_5ws(case_data):
    """Extracts the 5Ws (Who, What, When, Where, Why) from the provided case data."""

    if isinstance(case_data, pd.DataFrame):
        if case_data.empty:
            return {}
        else:
            return {col: case_data[col].tolist() for col in case_data.columns if col in ['Who', 'What', 'When', 'Where', 'Why']}
    elif isinstance(case_data, dict):
        if not case_data:
            return {}
        else:
            return {k: [v] for k, v in case_data.items() if k in ['Who', 'What', 'When', 'Where', 'Why']}
    else:
        raise TypeError("Unsupported data type. Expected Pandas DataFrame or dictionary.")

def build_prompt(case_data, extracted_5ws):
    """Composes a prompt for the LLM, incorporating case data and extracted 5Ws."""

    prompt = "\nYou are assisting an AML analyst to draft a SAR narrative.\n"
    prompt += "Follow FinCEN guidance: be clear, concise, chronological; avoid speculation.\n"
    prompt += "Include Who/What/When/Where/Why and key facts only.\n"
    prompt += "Label the output as 'AI-assisted draft'.\n\n"
    prompt += "5Ws:\n"
    prompt += str(extracted_5ws) + "\n\n"
    prompt += "Facts:\n"
    prompt += case_data + "\n\n"
    prompt += "Produce a single narrative paragraph set appropriate for a SAR filing.\n"
    return prompt

import os
import requests

def call_llm(prompt):
    """Makes an HTTP request to a specified LLM endpoint, retrieves the model's text response."""
    llm_api_url = os.environ.get("LLM_API_URL")
    llm_api_key = os.environ.get("LLM_API_KEY")

    headers = {
        "Authorization": f"Bearer {llm_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Replace with your desired model
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(llm_api_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        json_response = response.json()
        return json_response["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise e

from prompt_builder import build_prompt
from llm_caller import call_llm

def generate_ai_narrative(case_data, extracted_5ws):
    """Generates an AI-assisted narrative for a SAR."""

    prompt = build_prompt(case_data, extracted_5ws)
    narrative = call_llm(prompt)

    if "AI-assisted" not in narrative:
        narrative = "AI-assisted draft:\n" + narrative

    return narrative

def highlight_changes(ai_draft, analyst_edited):
    """Compares the AI-generated draft narrative with the analyst-edited version and highlights the differences between the two.
    Arguments: ai_draft (string), analyst_edited (string)
    Output: Returns a string or a data structure representing the highlighted changes (e.g., HTML diff).
    """
    if ai_draft == analyst_edited:
        return ""

    ai_words = ai_draft.split()
    analyst_words = analyst_edited.split()

    i = 0
    j = 0
    result = []

    while i < len(ai_words) or j < len(analyst_words):
        if i < len(ai_words) and j < len(analyst_words) and ai_words[i] == analyst_words[j]:
            result.append(ai_words[i])
            i += 1
            j += 1
        elif i < len(ai_words):
            result.append("<del>" + ai_words[i] + "</del>")
            i += 1
        elif j < len(analyst_words):
            result.append("<ins>" + analyst_words[j] + "</ins>")
            j += 1

    return " ".join(result).replace("<del> </del>", "")

def run_compliance_checklist(narrative, extracted_5ws):
    """Runs a compliance checklist."""

    report = {}

    # Check for 5Ws
    report["5Ws"] = all(extracted_5ws.values())

    # Check for chronology (basic implementation)
    report["chronology"] = True  # Assuming chronology is present if not explicitly stated otherwise

    # Check for clarity (basic implementation)
    report["clarity"] = True  # Assuming clarity is present if not explicitly stated otherwise

    # Check for length (example limit of 200 characters)
    report["length"] = len(narrative) <= 200

    # Check for speculation (not implemented in this version)
    if narrative.find("may have been") != -1:
        report["speculation"] = False # Assuming no speculation is present if not explicitly stated otherwise
    elif narrative.find("might have been") != -1:
        report["speculation"] = False
    elif narrative.find("could have been") != -1:
        report["speculation"] = False
    else:
        if "speculation" not in report:
            report["speculation"] = False
    

    return report

import json

def export_sar_data(narrative, facts, checklist_report, audit_trail):
    """Exports SAR data to a structured format (dict)."""

    if not isinstance(narrative, str):
        raise AttributeError("Narrative must be a string")
    if not isinstance(facts, list):
        raise AttributeError("Facts must be a list")

    sar_data = {
        "narrative": narrative,
        "facts": facts,
        "checklist_report": checklist_report,
        "audit_trail": audit_trail
    }
    return sar_data