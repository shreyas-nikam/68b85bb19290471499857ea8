id: 68b85bb19290471499857ea8_documentation
summary: Drafting AML Suspicious Activity Reports Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AML SAR Drafting Assistant Codelab

This codelab guides you through the development and functionalities of QuLab, a Streamlit application designed to assist AML analysts in drafting Suspicious Activity Reports (SARs). You'll learn how the application uses AI to streamline the SAR generation process, while maintaining human oversight and ensuring compliance.

## Introduction
Duration: 00:05

The application provides a structured workflow for analysts, starting from case intake and data exploration to SAR drafting, review, compliance checks, and export. It leverages AI to automate the initial SAR narrative generation and extracts key information from case data, thus enhancing efficiency and accuracy.

Key concepts covered in this codelab include:

*   Direct Large Language Model (LLM) call for SAR narrative generation.
*   Extraction of key information (the 5Ws: Who, What, When, Where, and Why).
*   Implementation of human-in-the-loop review processes.
*   Auditability and compliance guardrails.

## Setting up the Environment

This application assumes you have Python 3.7+ installed and packages like Streamlit, Pandas, NumPy, Plotly, Networkx and python-dotenv.

1.  Create a new directory for your project:

    ```console
    mkdir qulab_sar_drafting
    cd qulab_sar_drafting
    ```

2.  Create a virtual environment:

    ```console
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the required packages:

    ```console
    pip install streamlit pandas numpy plotly networkx python-dotenv
    ```

## Understanding the Application Structure
Duration: 00:10

The application consists of the main script `app.py` and a directory named `application_pages` which contains the code for individual pages of the application.

*   `app.py`: This is the main entry point of the Streamlit application. It handles navigation, session state initialization, and the overall structure of the application.
*   `application_pages/`: This directory contains separate Python files, each responsible for rendering a specific page of the application. These pages include "Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", and "Export & Audit".

## Examining `app.py`
Duration: 00:15

Let's break down the `app.py` file:

```python
import streamlit as st
import pandas as pd
import numpy as np

# Optional: Load environment variables from a .env file for local development
# For production, secrets should be managed securely (e.g., Kubernetes secrets, AWS Secrets Manager)
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="QuLab - AML SAR Drafting", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AML SAR Drafting Assistant")
st.divider()
st.markdown("""
In this lab, we explore the creation of an AI-assisted Streamlit application designed to streamline the **Drafting of AML Suspicious Activity Reports (SARs)**. This tool is built to enhance the efficiency and accuracy of AML analysts by providing intelligent assistance throughout the SAR generation process.

### Learning Goals:

*   **Automate First-Draft SAR Narratives**: Learn how to leverage a direct Large Language Model (LLM) call to generate initial SAR narratives, adhering strictly to regulatory guidance (e.g., FinCEN). This approach focuses on direct LLM interaction without relying on Retrieval-Augmented Generation (RAG) for narrative generation.
*   **Extract Key Information (The 5Ws)**: Understand the critical process of extracting **Who, What, When, Where, and Why** from complex case data. These fundamental elements are crucial for guiding the LLM to produce focused, compliant, and contextually relevant narratives.
*   **Human-in-the-Loop Review**: Practice implementing and performing human-in-the-loop review and compliance checks on the AI-generated narratives. This ensures accuracy, regulatory adherence, and maintains the essential role of human expertise in the final SAR submission.
*   **Auditability and Compliance Guardrails**: Implement features that ensure every step of the SAR drafting process is auditable, transparent, and aligned with compliance requirements, including versioning, audit logging, and sign-off mechanisms.

### Business Logic Overview:

The application guides the analyst through a structured workflow:

1.  **Case Intake**: Upload and get a preliminary overview of the case data.
2.  **Explore Data**: Interactively analyze transactions, customer relationships, and geographic patterns using advanced visualizations.
3.  **Draft SAR**: Generate an initial SAR narrative using an LLM, steered by extracted key facts.
4.  **Review & Compare**: Allow analysts to review, edit, and compare the AI-generated draft with their final version.
5.  **Compliance Checklist & Sign-off**: Validate the narrative against a compliance checklist and facilitate formal sign-off.
6.  **Export & Audit**: Export the final SAR package, including the narrative, facts, checklist report, and a detailed audit trail.

This structured approach ensures that while AI assists in drafting, human oversight and compliance remain central to the process.
""")

# Initialize session state for data if not already present
if "data" not in st.session_state:
    @st.cache_data(show_spinner=False)
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
    
    np.random.seed(42)
    st.session_state["data"] = load_synthetic_data()
    st.session_state["data"]["transactions"] = st.session_state["data"]["transactions"].rename(columns={'amount': 'transaction_amount'})
    


# About / Controls Panel
st.sidebar.header("About / Controls")
st.sidebar.markdown("""
- **BSA/FinCEN SAR Requirements**: [Link to FinCEN Guidance](https://www.fincen.gov/resources/statutes-regulations/guidance)
- **FinCEN Narrative Guidance**: Best practices for SAR narratives.
- **OCC/SR 11-7 Model Risk**: Principles for sound model risk management.
- **MITRE AI Assurance Cues**: Guidelines for AI system trustworthiness.
""")


# Navigation
page = st.sidebar.selectbox(
    label="Navigation", 
    options=["Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", "Export & Audit"]
)

if page == "Case Intake":
    from application_pages.page1_case_intake import run_page1
    run_page1()
elif page == "Explore Data":
    from application_pages.page2_explore_data import run_page2
    run_page2()
elif page == "Draft SAR":
    from application_pages.page3_draft_sar import run_page3
    run_page3()
elif page == "Review & Compare":
    from application_pages.page4_review_compare import run_page4
    run_page4()
elif page == "Compliance Checklist & Sign-off":
    from application_pages.page5_compliance_signoff import run_page5
    run_page5()
elif page == "Export & Audit":
    from application_pages.page6_export_audit import run_page6
    run_page6()
```

Key components of `app.py`:

*   **Import Statements:** Imports necessary libraries like Streamlit, Pandas, NumPy, and dotenv.
*   **Page Configuration:** Configures the Streamlit page title and layout using `st.set_page_config`.
*   **Sidebar:** Sets up the sidebar with the application logo, divider, and helpful links.
*   **Session State Initialization:** Initializes the `data` key in Streamlit's session state. If the data doesn't exist, it calls the `load_synthetic_data()` function to create sample data for the application. The `@st.cache_data` decorator caches the output of `load_synthetic_data()` to improve performance.
*   **Navigation:** Creates a selectbox in the sidebar for navigation between different pages of the application.
*   **Page Routing:** Based on the selected page, it imports and runs the corresponding function from the `application_pages` directory.

## Understanding the `load_synthetic_data()` Function
Duration: 00:10

The `load_synthetic_data()` function generates synthetic data for the AML analysis. It creates four Pandas DataFrames:

*   `customers_df`: Contains customer information, including customer ID, name, country, and risk score.
*   `transactions_df`: Contains transaction data, including transaction ID, customer ID, amount, timestamp, and location data.
*   `alerts_df`: Contains alert data, including alert ID, customer ID, reason, and timestamp.
*   `notes_df`: Contains notes data, including note ID, customer ID, note content, and timestamp.

The data is designed to simulate real-world AML scenarios, allowing you to test the application's functionality without needing actual financial data.

## Examining `application_pages/page1_case_intake.py`
Duration: 00:15

This page provides an initial overview of the case data.

```python
import streamlit as st
import pandas as pd
import numpy as np

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

def run_page1():
    st.header("Case Intake")
    st.markdown("""
    Upload your case bundle here or proceed with the pre-loaded synthetic data.
    This section provides an initial overview of the case, highlighting key statistics and potential AML typologies.

    ### Data Loading and Overview
    The application uses a `load_synthetic_data()` function to populate initial case data. This function generates:
    - `customers_df`: Contains synthetic customer information.
    - `transactions_df`: Details individual financial transactions.
    - `alerts_df`: Records of system-generated alerts.
    - `notes_df`: Analyst notes related to customers or cases.

    The mathematical operation for calculating total transaction volume is:
    $$\text{Total Volume} = \sum_{i=1}^{N} \text{transaction\_amount}_i$$

    The average transaction amount is calculated as:
    $$\text{Average Amount} = \frac{\text{Total Volume}}{\text{Number of Transactions}}$$
    """)

    # Use synthetic data from session state
    data = st.session_state["data"]
    customers = data["customers"]
    transactions = data["transactions"]
    alerts = data["alerts"]
    notes = data["notes"]

    st.subheader("Uploaded Case Data Overview")
    st.write("Below are the shapes of the loaded dataframes:")
    st.write(f"Customers DataFrame shape: {customers.shape}")
    st.write(f"Transactions DataFrame shape: {transactions.shape}")
    st.write(f"Alerts DataFrame shape: {alerts.shape}")
    st.write(f"Notes DataFrame shape: {notes.shape}")

    st.markdown("")

    st.subheader("Quick Stats")

    kpis = calculate_summary_kpis(transactions)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="# Total Transactions", value=len(transactions))
        st.metric(label="Total Transaction Volume", value=f"${kpis['total_transaction_volume']:, .2f}")
    with col2:
        st.metric(label="Average Transaction Amount", value=f"${kpis['average_transaction_amount']:, .2f}")
        if not transactions.empty:
            st.metric(label="Time Window", value=f"{transactions['timestamp'].min().strftime('%Y-%m-%d')} to {transactions['timestamp'].max().strftime('%Y-%m-%d')}")
        else:
            st.metric(label="Time Window", value="N/A")

    with col3:
        st.metric(label="# Unique Customers", value=len(customers['customer_id'].unique()))
        st.metric(label="# Total Alerts", value=len(alerts))

    st.markdown("")

    st.subheader("Possible Typologies")
    # Simple heuristic for typologies based on alert reasons
    possible_typologies = alerts['reason'].unique().tolist()
    if possible_typologies:
        st.write("Based on available alert data, possible typologies include:")
        for typology in possible_typologies:
            st.success(f"\# {typology}")
    else:
        st.info("No specific typologies identified from alert data yet. Further investigation needed.")

    st.markdown("")

    st.subheader("Raw Data Preview")
    st.write("Customers Data:")
    st.dataframe(customers.head())
    st.write("Transactions Data:")
    st.dataframe(transactions.head())
    st.write("Alerts Data:")
    st.dataframe(alerts.head())
    st.write("Notes Data:")
    st.dataframe(notes.head())
```

Key functionalities:

*   **KPI Calculation:** The `calculate_summary_kpis` function calculates key performance indicators such as total transaction volume and average transaction amount.
*   **Data Overview:** Displays the shapes of the loaded DataFrames to give the user an overview of the data size.
*   **Quick Stats:** Presents key statistics about the data using Streamlit's `st.metric` component.
*   **Possible Typologies:** Identifies potential AML typologies based on the reasons for the alerts.
*   **Raw Data Preview:** Displays the first few rows of each DataFrame to allow the user to preview the data.

## Examining `application_pages/page2_explore_data.py`
Duration: 00:20

This page provides tools to interactively analyze the case data using visualizations.

```python
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
```

This code shows three key visualization functions:

*   **`create_timeline_visualization(transactions)`**: Creates a timeline visualization of transaction data using Plotly.  It visualizes the trend of transaction amounts over time.
*   **`create_geo_map_visualization(transactions)`**: Generates a geographic map visualization of transaction origins and destinations using Plotly.  The size of the markers on the map corresponds to the transaction amount.
*   **`create_counterparty_network_graph(transactions)`**: Creates a network graph of transaction counterparties using NetworkX. This helps visualize relationships between different entities involved in transactions.

<aside class="negative">
Ensure that your data includes the necessary columns (`timestamp`, `transaction_amount`, `origin_latitude`, `origin_longitude`, `destination_latitude`, `destination_longitude`, `Source`, `Target`) for these visualizations to function correctly.  The application uses dummy data, so you might need to adapt the column names to match your data.
</aside>

## Next Steps

The codelab will continue with the implementation of the `Draft SAR`, `Review & Compare`, `Compliance Checklist & Sign-off`, and `Export & Audit` pages and corresponding functionalities.
