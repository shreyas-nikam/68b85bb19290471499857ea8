
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

    st.markdown("---")

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

    st.markdown("---")

    st.subheader("Possible Typologies")
    # Simple heuristic for typologies based on alert reasons
    possible_typologies = alerts['reason'].unique().tolist()
    if possible_typologies:
        st.write("Based on available alert data, possible typologies include:")
        for typology in possible_typologies:
            st.success(f"\# {typology}")
    else:
        st.info("No specific typologies identified from alert data yet. Further investigation needed.")

    st.markdown("---")

    st.subheader("Raw Data Preview")
    st.write("Customers Data:")
    st.dataframe(customers.head())
    st.write("Transactions Data:")
    st.dataframe(transactions.head())
    st.write("Alerts Data:")
    st.dataframe(alerts.head())
    st.write("Notes Data:")
    st.dataframe(notes.head())
