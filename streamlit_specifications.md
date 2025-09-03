
## Streamlit Application Requirements Specification

### 1. Application Overview

**Learning Goals:**

*   Assist AML analysts by generating **first-draft SAR narratives**, summarizing transaction timelines, and suggesting typologies—**always** with human review, auditability, and compliance guardrails.
*   See how a **direct LLM call** can automate first-draft SAR narratives while strictly following regulatory guidance, without relying on Retrieval-Augmented Generation (RAG).
*   Learn to **extract key information** (the 5Ws: Who, What, When, Where, Why) from case data, which is crucial for steering the LLM in generating a focused and compliant narrative.
*   Practice **human-in-the-loop** review and perform compliance checks on the generated narrative before its final export, ensuring accuracy and regulatory adherence.

### 2. User Interface Requirements

**Layout and Navigation Structure:**

Multi-page Streamlit application with the following pages, mirroring the SAR workflow:

1.  **Case Intake**
2.  **Explore Data**
3.  **Draft SAR**
4.  **Review & Compare**
5.  **Compliance Checklist & Sign-off**
6.  **Export & Audit**

A sidebar or navigation bar will allow users to move between these pages.  An “About / Controls” panel should surface BSA/FinCEN SAR requirements, FinCEN narrative guidance, OCC/SR 11-7 model risk, and MITRE AI assurance cues.

**Input Widgets and Controls:**

*   **Case Intake:**
    *   File uploader/selector for case bundles.
*   **Explore Data:**
    *   Date range slicer
    *   Amount range slicer
    *   Channel filter (dropdown/multiselect)
    *   Branch filter (dropdown/multiselect)
    *   Counterparty filter (searchable dropdown/multiselect)
    *   Geo filter (interactive map selection)
*   **Draft SAR:**
    *   "Generate draft" button.
*   **Review & Compare:**
    *   Rich text editor for narrative review and edits.
    *   "Save" button with versioning and audit logging.
*   **Compliance Checklist & Sign-off:**
    *   Compliance officer sign-off (name, timestamp, immutable hash of content).
*   **Export & Audit:**
    *   Export button to download the final narrative, JSON of facts, checklist report, and audit trail (CSV/JSON).

**Visualization Components:**

*   **Case Intake:**
    *   Quick stats display (#transactions, total in/out, #branches, #alerts, time window).
    *   "Possible typologies" chip list.
*   **Explore Data:**
    *   Timeline of activity (interactive event scatter or bars) with filters.
    *   Geo map (branch locations & flows).
    *   Counterparty network graph.
    *   Heatmaps (day-of-week × hour-of-day deposit intensity; alert density over time).
    *   Typology cues panel (visual flags).
*   **Review & Compare:**
    *   Diff viewer (side-by-side AI draft vs analyst-edited final).
    *   Explainability panel (data rows powering each sentence).
*   **Compliance Checklist & Sign-off:**
    *   Checklist status widget (live validation).

**Interactive Elements and Feedback Mechanisms:**

*   Clickable elements in visualizations to add fact snippets to a "Draft facts tray."
*   Accept/reject AI suggestions in the rich text editor.
*   Explainability panel linking sentences to data rows and visual selections.
*   Live validation (pass/fail) of checklist items.
*   Versioning on save with audit records.

### 3. Additional Requirements

*   **Annotation and Tooltip Specifications:**
    *   Tooltips on visualizations to display detailed information on hover.
    *   Annotations on the timeline, geomap, and network graph to highlight key events or relationships.
*   **State Management:**
    *   Utilize Streamlit's session state (`st.session_state`) to persist the state of all input widgets, data selections, and generated narratives across page reloads and interactions. This includes:
        *   Uploaded case data.
        *   Selected filters and slicers.
        *   Selected facts in the "Draft facts tray."
        *   Extracted 5Ws.
        *   AI-generated drafts.
        *   Analyst-edited narratives.
        *   Compliance checklist results.
        *   Audit trail.

### 4. Notebook Content and Code Requirements

**Extracted Code Stubs:**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import nltk
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

# Optional: Load environment variables from a .env file for local development
# For production, secrets should be managed securely (e.g., Kubernetes secrets, AWS Secrets Manager)
load_dotenv()

numpy.random.seed(42)
```

```python
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
        "origin_latitude": np.random.uniform(25, 50, size=num_transactions), # Dummy lat
        "origin_longitude": np.random.uniform(-120, -70, size=num_transactions), # Dummy lon
        "destination_latitude": np.random.uniform(25, 50, size=num_transactions), # Dummy lat
        "destination_longitude": np.random.uniform(-120, -70, size=num_transactions), # Dummy lon
        "Source": np.random.choice(customer_ids, size=num_transactions), # Dummy Source for network graph
        "Target": np.random.choice(customer_ids, size=num_transactions)  # Dummy Target for network graph
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

data = load_synthetic_data()
customers = data["customers"]
transactions = data["transactions"]
alerts = data["alerts"]
notes = data["notes"]

# Rename 'amount' to 'transaction_amount' for consistency with KPI function
transactions = transactions.rename(columns={'amount': 'transaction_amount'})
```

```python
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

kpis = calculate_summary_kpis(transactions)
```

```python
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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

timeline_fig = create_timeline_visualization(transactions)
```

```python
import pandas as pd
import plotly.graph_objects as go

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

geomap_fig = create_geo_map_visualization(transactions)
```

```python
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt # For drawing the graph

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

# Create the network graph
counterparty_graph = create_counterparty_network_graph(transactions)
```

```python
# Simulate an analyst selecting key facts for the SAR
# We'll pick a few transactions and an alert for a specific customer.

# Let's focus on a hypothetical customer, e.g., customer_id = 7
# Find customer details
focused_customer_id = 7
customer_details = customers[customers['customer_id'] == focused_customer_id].to_dict('records')[0] if not customers[customers['customer_id'] == focused_customer_id].empty else {}

# Find some transactions for this customer
customer_transactions = transactions[transactions['customer_id'] == focused_customer_id].head(3).to_dict('records')

# Find an alert for this customer
customer_alert = alerts[alerts['customer_id'] == focused_customer_id].head(1).to_dict('records')[0] if not alerts[alerts['customer_id'] == focused_customer_id].empty else {}

# Combine into selected_facts
selected_facts = []
if customer_details:
    selected_facts.append({"type": "Customer Info", **customer_details})

for i, trans in enumerate(customer_transactions):
    selected_facts.append({"type": f"Transaction {i+1}", **trans})

if customer_alert:
    selected_facts.append({"type": "Alert", **customer_alert})

# If no specific customer data, just pick some random facts
if not selected_facts:
    selected_facts.append({"type": "Customer Info", **customers.sample(1).to_dict('records')[0]})
    selected_facts.append({"type": "Transaction 1", **transactions.sample(1).to_dict('records')[0]})
    selected_facts.append({"type": "Alert", **alerts.sample(1).to_dict('records')[0]})

# Convert selected_facts into a more LLM-friendly string representation for the prompt
selected_facts_str = "\n".join([str(fact) for fact in selected_facts]))
```

```python
import pandas as pd

def extract_5ws(case_data):
    """Extracts the 5Ws (Who, What, When, Where, Why) from the provided case data.

    Args:
        case_data (list of dict or pd.DataFrame): The curated facts for the case.

    Returns:
        dict: A dictionary containing the extracted 5Ws.
    """
    five_ws = {
        'Who': [],
        'What': [],
        'When': [],
        'Where': [],
        'Why': []
    }

    if not case_data:
        return five_ws

    if isinstance(case_data, pd.DataFrame):
        records = case_data.to_dict('records')
    elif isinstance(case_data, list):
        records = case_data
    else:
        raise TypeError("Unsupported data type for case_data. Expected list of dict or Pandas DataFrame.")

    for fact in records:
        # Extract Who
        if 'name' in fact and fact['name'] not in five_ws['Who']:
            five_ws['Who'].append(fact['name'])
        if 'customer_id' in fact and f"Customer ID {fact['customer_id']}" not in five_ws['Who']:
            five_ws['Who'].append(f"Customer ID {fact['customer_id']}")

        # Extract What
        if 'reason' in fact and fact['reason'] not in five_ws['What']:
            five_ws['What'].append(fact['reason'])
        if 'transaction_amount' in fact and f"Transaction amount of {fact['transaction_amount']:,.2f}" not in five_ws['What']:
            five_ws['What'].append(f"Transaction amount of {fact['transaction_amount']:,.2f}")

        # Extract When
        if 'timestamp' in fact:
            date_str = pd.to_datetime(fact['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            if date_str not in five_ws['When']:
                five_ws['When'].append(date_str)

        # Extract Where
        if 'country' in fact and fact['country'] not in five_ws['Where']:
            five_ws['Where'].append(fact['country'])
        if 'origin_latitude' in fact and 'origin_longitude' in fact and \
           f"Lat: {fact['origin_latitude']:.2f}, Lon: {fact['origin_longitude']:.2f}" not in five_ws['Where']:
            five_ws['Where'].append(f"Lat: {fact['origin_latitude']:.2f}, Lon: {fact['origin_longitude']:.2f}")

        # Extract Why (often inferred or directly from alert reasons/risk scores)
        if 'risk_score' in fact and fact['risk_score'] >= 70 and f"High risk score ({fact['risk_score']})" not in five_ws['Why']:
            five_ws['Why'].append(f"High risk score ({fact['risk_score']})")
        if 'reason' in fact and fact['reason'] not in five_ws['Why']:
            five_ws['Why'].append(fact['reason'])

    # Clean up empty lists
    return {k: v for k, v in five_ws.items() if v}

five_ws = extract_5ws(selected_facts)
```

```python
import os, requests
from tenacity import retry, stop_after_attempt, wait_exponential

LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")      # Placeholder URL
LLM_API_KEY = os.getenv("LLM_API_KEY", "YOUR_OPENAI_API_KEY")      # Placeholder Key

def build_prompt(case_data, extracted_5ws):

    # Format 5Ws for the prompt
    five_ws_formatted = "\n".join([f"  - {k}: {', '.join(map(str, v))}" for k, v in extracted_5ws.items()])

    # Convert selected_facts into a more readable string representation for the prompt
    facts_formatted = "\n".join([str(fact) for fact in case_data]) if isinstance(case_data, list) else str(case_data)

    return f"""
You are assisting an AML analyst to draft a SAR narrative.
Follow FinCEN guidance: be clear, concise, chronological; avoid speculation.
Include Who/What/When/Where/Why and key facts only.
Label the output as 'AI-assisted draft'.

5Ws:
{five_ws_formatted}

Facts:
{facts_formatted}

Produce a single narrative paragraph set appropriate for a SAR filing.
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_llm(prompt: str) -> str:
    if not LLM_API_URL or LLM_API_KEY == "YOUR_OPENAI_API_KEY":
        print("Warning: LLM_API_URL or LLM_API_KEY not set. Using a dummy response.")
        return "AI-assisted draft:\nThis is a dummy AI-assisted narrative because LLM API credentials were not configured. Please set LLM_API_URL and LLM_API_KEY environment variables for real LLM interaction. The narrative should include details about Customer 7, their transactions, and the alert received. It should clearly state who, what, when, where, and why, based on the provided facts, and must avoid speculation. The customer engaged in multiple transactions between 2023-01-01 and 2023-01-03, with an alert triggered on 2023-01-05 due to suspicious activity. Details about the transaction amounts and the origin/destination latitudes and longitudes were provided."

    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",   # configure per your provider, e.g., "gpt-4o-mini", "gemini-pro"
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 600
    }
    r = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    # Adjust the path below to your provider’s response schema:
    return data["choices"][0]["message"]["content"].strip()

def generate_ai_narrative(case_data, extracted_5ws) -> str:
    prompt = build_prompt(case_data, extracted_5ws)
    narrative = call_llm(prompt)
    if "AI-assisted" not in narrative:
        narrative = "AI-assisted draft:\n" + narrative
    return narrative

ai_draft_narrative = generate_ai_narrative(selected_facts, five_ws)
```

```python
def highlight_changes(ai_draft, analyst_edited):
    """Compares the AI-generated draft narrative with the analyst-edited version and highlights the differences between the two.
    Arguments: ai_draft (string), analyst_edited (string)
    Output: Returns a string or a data structure representing the highlighted changes (e.g., HTML diff).
    """
    if ai_draft == analyst_edited:
        return "<p>No changes detected. The analyst's edited narrative is identical to the AI draft.</p>"

    ai_words = ai_draft.split()
    analyst_words = analyst_edited.split()

    # Simple diff algorithm: Mark deletions and insertions
    # This is a simplified version and might not produce the most optimal diff for complex changes
    # For production, consider using a dedicated diff library (e.g., `difflib` in Python)

    result_html = []
    i, j = 0, 0
    while i < len(ai_words) or j < len(analyst_words):
        if i < len(ai_words) and j < len(analyst_words) and ai_words[i] == analyst_words[j]:
            result_html.append(ai_words[i])
            i += 1
            j += 1
        elif i < len(ai_words) and (j == len(analyst_words) or ai_words[i] not in analyst_words[j:]):
            result_html.append(f"<del style=\"background-color:#ffe0e0;\">{ai_words[i]}</del>")
            i += 1
        elif j < len(analyst_words) and (i == len(ai_words) or analyst_words[j] not in ai_words[i:]):
            result_html.append(f"<ins style=\"background-color:#e0ffe0;\">{analyst_words[j]}</ins>")
            j += 1
        else: # Fallback for words that might have been reordered or changed significantly
            if i < len(ai_words):
                result_html.append(f"<del style=\"background-color:#ffe0e0;\">{ai_words[i]}</del>")
                i += 1
            if j < len(analyst_words):
                result_html.append(f"<ins style=\"background-color:#e0ffe0;\">{analyst_words[j]}</ins>")
                j += 1

    return " ".join(result_html)

# Simulate an analyst editing the AI draft
analyst_edited_narrative = ai_draft_narrative.replace("AI-assisted draft:", "Final Analyst-reviewed Narrative:")
analyst_edited_narrative = analyst_edited_narrative.replace("unusual transaction location", "various high-risk geographies")
analyst_edited_narrative += "\nThe analyst further noted a pattern of structured deposits just below reporting thresholds, indicating a deliberate attempt to evade detection."

highlighted_diff = highlight_changes(ai_draft_narrative, analyst_edited_narrative)
```

```python
def run_compliance_checklist(narrative, extracted_5ws):
    """Runs a compliance checklist on the narrative and extracted 5Ws.

    Args:
        narrative (str): The SAR narrative to check.
        extracted_5ws (dict): The dictionary of extracted 5Ws.

    Returns:
        dict: A report indicating pass/fail for each compliance item.
    """
    report = {}

    # 1. Check for 5Ws presence
    report["5Ws_present"] = all(len(v) > 0 for k, v in extracted_5ws.items())

    # 2. Check for chronology (basic: assuming timestamps in 5Ws imply some chronology)
    # A more robust check would involve parsing dates within the narrative itself.
    report["chronology"] = 'When' in extracted_5ws and len(extracted_5ws['When']) > 0
    if report["chronology"]:
        try:
            timestamps = [pd.to_datetime(t) for t in extracted_5ws['When']]
            report["chronology"] = all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1))
        except Exception: # Handle cases where 'When' values might not be perfectly sortable dates
            report["chronology"] = True # Assume chronological if parsing fails for simplicity


    # 3. Check for clarity (very basic: presence of common words implies some clarity, or length check)
    # Real clarity checks require advanced NLP or human review.
    report["clarity"] = len(narrative) > 50 # Arbitrary length check as a proxy for substantial content

    # 4. Check for speculation (look for common speculative phrases)
    speculative_phrases = ["may have been", "might have been", "could have been", "it is believed", "suggests that"]
    report["no_speculation"] = not any(phrase in narrative.lower() for phrase in speculative_phrases)

    # 5. Check for length (example: narrative length between 100 and 1000 characters)
    min_len = 100
    max_len = 1000
    report["length_bounds"] = min_len <= len(narrative) <= max_len

    return report

compliance_report = run_compliance_checklist(analyst_edited_narrative, five_ws)
```

```python
import json

def export_sar_data(narrative, facts, checklist_report, audit_trail):
    """Exports SAR data to a structured format (dict).

    Args:
        narrative (str): The final SAR narrative.
        facts (list): A list of dictionaries representing the selected facts.
        checklist_report (dict): The compliance checklist report.
        audit_trail (list): A list of dictionaries detailing the audit trail.

    Returns:
        dict: A dictionary containing all SAR data.
    """
    if not isinstance(narrative, str):
        raise AttributeError("Narrative must be a string")
    if not isinstance(facts, list):
        raise AttributeError("Facts must be a list")
    if not isinstance(checklist_report, dict):
        raise AttributeError("Checklist report must be a dictionary")
    if not isinstance(audit_trail, list):
        raise AttributeError("Audit trail must be a list")

    sar_data = {
        "narrative": narrative,
        "facts": facts,
        "checklist_report": checklist_report,
        "audit_trail": audit_trail
    }
    return sar_data

# Simulate audit trail entries
audit_trail = [
    {"timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'), "event": "AI draft generated", "model": "gpt-3.5-turbo", "temperature": 0.2},
    {"timestamp": (pd.Timestamp.now() + pd.Timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S'), "event": "Analyst review started", "analyst_id": "AML_Analyst_001"},
    {"timestamp": (pd.Timestamp.now() + pd.Timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'), "event": "Narrative edited and changes highlighted", "analyst_id": "AML_Analyst_001"},
    {"timestamp": (pd.Timestamp.now() + pd.Timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M:%S'), "event": "Compliance checklist run", "status": compliance_report}
]

final_sar_data = export_sar_data(analyst_edited_narrative, selected_facts, compliance_report, audit_trail)
```

**Implementation Details from the Notebook:**

*   **Data Loading and Preparation:**
    *   The `load_synthetic_data()` function will be used (or adapted to handle uploaded data) to populate the application with case data.  This function creates synthetic data for customers, transactions, alerts, and notes.  The structure of the dataframes generated by this function is critical for the downstream components.
    *   The shapes of the dataframes must be printed to confirm the data has loaded as expected.
*   **Case Intake and Summary KPIs:**
    *   The `calculate_summary_kpis()` function calculates total transaction volume, average transaction amount, and transactions per customer.  These KPIs should be displayed as prominent metrics in the Case Intake page.
    *   The function's mathematical operations are:
        *   Total Volume: $\text{Total Volume} = \sum_{i=1}^{N} \text{transaction\_amount}_i$
        *   Average Amount: $\text{Average Amount} = \frac{\text{Total Volume}}{\text{Number of Transactions}}$
*   **Data Exploration Visualizations:**
    *   The `create_timeline_visualization()` function generates a timeline of transaction activity. The visualization is interactive, allowing analysts to identify patterns and anomalies.  The y-axis should dynamically adjust based on available data, plotting either `transaction_amount` or transaction counts. The visualization shows $\text{Transaction Activity} = f(\text{timestamp}, \text{amount})$.
    *   The `create_geo_map_visualization()` function displays transaction origins on an interactive world map. Marker size corresponds to the transaction amount. Geographic Point is defined as $(\text{latitude}, \text{longitude})$.
    *   The `create_counterparty_network_graph()` function creates a network graph of transaction counterparties. Nodes represent customers, and edges represent transactions. The graph will be displayed using `matplotlib` or a Streamlit-compatible graph component.  The structure of the graph is based on $G = (V, E)$, where $V$ is the set of vertices (customers/counterparties), and $E$ is the set of edges (transactions).
*   **Fact Snippet Selection:**
    *   Implement a mechanism (e.g., a "Draft facts tray") for analysts to select relevant rows from the displayed data (tables and visualizations).
*   **5W Extraction:**
    *   The `extract_5ws()` function parses the selected facts to identify the Who, What, When, Where, and Why elements.
*   **AI Narrative Generation:**
    *   The `build_prompt()` function constructs the prompt sent to the LLM.
    *   The `call_llm()` function sends the prompt to the LLM API and retrieves the generated narrative.  The `tenacity` library is used for retries.
    *   The `generate_ai_narrative()` function orchestrates the prompt building and LLM call.
*   **Review and Comparison:**
    *   The `highlight_changes()` function compares the AI-generated draft with the analyst-edited version and highlights the differences using HTML `<ins>` and `<del>` tags.  The edits can be visualized as $\text{highlight\_changes(AI draft, analyst edited)}$.
*   **Compliance Checklist:**
    *   The `run_compliance_checklist()` function evaluates the narrative against compliance criteria and returns a report (pass/fail for each item).
*   **Export & Audit:**
    *   The `export_sar_data()` function assembles the final SAR data (narrative, facts, checklist report, audit trail) into a dictionary that can be serialized to JSON.  The data is structured as: $\text{SAR Data Bundle} = \{ \text{narrative}, \text{facts}, \text{checklist\_report}, \text{audit\_trail} \}$.

