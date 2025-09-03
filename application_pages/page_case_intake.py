import streamlit as st
import pandas as pd
import numpy as np
from application_pages.utils import load_synthetic_data, calculate_summary_kpis

def run_page_case_intake():
    st.header("1. Case Intake")
    st.markdown("""
    This page allows you to load case bundles, either by uploading files or by generating synthetic data.
    Once loaded, a quick summary of key metrics and potential typologies will be displayed.
    """)

    st.subheader("Load Case Data")

    # File uploader/selector for case bundles (placeholder for real implementation)
    uploaded_file = st.file_uploader("Upload Case Bundle (e.g., CSV, JSON)", type=["csv", "json"])

    if uploaded_file is not None:
        st.info("File upload functionality is a placeholder. Using synthetic data for demonstration.")
        # In a real app, parse uploaded_file and populate st.session_state.case_data
        # For now, we'll proceed with synthetic data generation.

    if st.button("Generate Synthetic Case Data"):
        with st.spinner("Generating synthetic data..."):
            synthetic_data = load_synthetic_data()
            st.session_state.customers = synthetic_data['customers']
            st.session_state.transactions = synthetic_data['transactions']
            st.session_state.alerts = synthetic_data['alerts']
            st.session_state.notes = synthetic_data['notes']
            st.session_state.case_data = synthetic_data # Store all dfs

            st.success("Synthetic data loaded successfully!")
            st.dataframe(st.session_state.transactions.head())
    
    st.divider()

    if st.session_state.transactions is not None and not st.session_state.transactions.empty:
        st.subheader("Quick Stats Display")
        kpis = calculate_summary_kpis(st.session_state.transactions)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="# Transactions", value=kpis['total_transactions'])
            st.metric(label="Total Inflow", value=f"${kpis['total_inflow']:,.2f}")
        with col2:
            st.metric(label="Total Outflow", value=f"${kpis['total_outflow']:,.2f}")
            st.metric(label="Avg Transaction Amount", value=f"${kpis['avg_transaction_amount']:,.2f}")
        with col3:
            st.metric(label="# Customers Involved", value=kpis['num_customers_involved'])
            st.metric(label="# Branches Involved", value=kpis['num_branches_involved'])

        st.markdown(f"**Time Window:** {kpis['time_window_start']} to {kpis['time_window_end']}")

        st.subheader("Possible Typologies")
        if kpis['possible_typologies']:
            for typology in kpis['possible_typologies']:
                st.info(typology)
        else:
            st.info("No specific typologies suggested based on current data.")
    else:
        st.info("No case data loaded yet. Please upload a file or generate synthetic data.")

    # Always ensure extracted_5ws is updated when data changes
    if st.session_state.case_data and st.button("Extract 5Ws from Loaded Data"):
        from application_pages.utils import extract_5ws
        st.session_state.extracted_5ws = extract_5ws(st.session_state.case_data)
        st.success("5Ws extracted and stored in session state.")
        st.json(st.session_state.extracted_5ws)
