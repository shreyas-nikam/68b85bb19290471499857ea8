
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx
import spacy
import io

# Removed nlp loading from here, as it's handled in utils.py

st.set_page_config(page_title="QuLab - Drafting AML SARs", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Drafting AML Suspicious Activity Reports")
st.divider()
st.markdown("""
Welcome to the QuLab for Drafting AML Suspicious Activity Reports!

In this lab, we explore how Artificial Intelligence, specifically Large Language Models (LLMs), can augment the crucial work of Anti-Money Laundering (AML) analysts. Our focus is on streamlining the initial phases of Suspicious Activity Report (SAR) generation, a task traditionally intensive in manual data synthesis and narrative drafting.

### Learning Goals:

*   **Automate First-Draft SAR Narratives**: Learn how to leverage a direct LLM call to generate a preliminary SAR narrative, adhering to regulatory guidance. This approach emphasizes strict compliance without relying on Retrieval-Augmented Generation (RAG), focusing instead on structured input from extracted case data.
*   **Extract Key Information (The 5Ws)**: Understand the criticality of extracting the "Who, What, When, Where, Why" from raw case data. This information is paramount for effectively steering the LLM to produce a focused, fact-based, and compliant narrative, forming the foundation of a robust SAR.
*   **Human-in-the-Loop Review**: Practice the essential human-in-the-loop paradigm for reviewing and refining AI-generated drafts. This involves performing crucial compliance checks and ensuring the narrative's accuracy, completeness, and adherence to regulatory standards before finalization.
*   **Auditability and Compliance Guardrails**: See how audit trails, versioning, and compliance checklists are integrated into the workflow to maintain transparency, accountability, and regulatory adherence throughout the SAR drafting process.

This application provides a multi-page workflow designed to guide you through the process, from case intake and data exploration to SAR drafting, review, compliance, and final export.
""")

# About / Controls Panel
st.sidebar.header("About / Controls")
with st.sidebar.expander("Regulatory Guidance & Risks"):
    st.markdown("""
    ### BSA/FinCEN SAR Requirements
    *   **Purpose**: To detect and deter money laundering and terrorist financing.
    *   **Content**: Must be factual, thorough, and chronological.
    *   **Timeliness**: Filed within 30-60 days of initial detection.

    ### FinCEN Narrative Guidance
    *   **The 5Ws**: Who, What, When, Where, Why (and How).
    *   **Avoid Speculation**: Stick to facts and observed behavior.
    *   **Chronological Order**: Present events clearly over time.

    ### OCC/SR 11-7 Model Risk Management
    *   **Model Validation**: Ensure models (including LLMs) are accurate and reliable.
    *   **Governance**: Establish clear policies for model development, implementation, and use.
    *   **Monitoring**: Continuously monitor model performance.

    ### MITRE AI Assurance Cues
    *   **Transparency**: Understand how the AI works.
    *   **Explainability**: Justify AI decisions.
    *   **Robustness**: Resilience to adversarial attacks.
    *   **Fairness**: Mitigate bias in outputs.
    *   **Accountability**: Define responsibilities for AI outcomes.
    """)

st.sidebar.divider()

# Initialize session state for data
if 'case_data' not in st.session_state:
    st.session_state.case_data = None
if 'transactions' not in st.session_state:
    st.session_state.transactions = None
if 'customers' not in st.session_state:
    st.session_state.customers = None
if 'alerts' not in st.session_state:
    st.session_state.alerts = None
if 'notes' not in st.session_state:
    st.session_state.notes = None
if 'extracted_5ws' not in st.session_state:
    st.session_state.extracted_5ws = None
if 'ai_draft_narrative' not in st.session_state:
    st.session_state.ai_draft_narrative = ""
if 'analyst_edited_narrative' not in st.session_state:
    st.session_state.analyst_edited_narrative = ""
if 'draft_facts_tray' not in st.session_state:
    st.session_state.draft_facts_tray = []
if 'compliance_checklist_results' not in st.session_state:
    st.session_state.compliance_checklist_results = {}
if 'audit_trail' not in st.session_state:
    st.session_state.audit_trail = []


if 'sar_signed_off' not in st.session_state:
    st.session_state.sar_signed_off = False


# Navigation
page = st.sidebar.selectbox(
    label="Navigation",
    options=["Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", "Export & Audit"]
)


if page == "Case Intake":
    from application_pages.page_case_intake import run_page_case_intake
    run_page_case_intake()
elif page == "Explore Data":
    from application_pages.page_explore_data import run_page_explore_data
    run_page_explore_data()
elif page == "Draft SAR":
    from application_pages.page_draft_sar import run_page_draft_sar
    run_page_draft_sar()
elif page == "Review & Compare":
    from application_pages.page_review_compare import run_page_review_compare
    run_page_review_compare()
elif page == "Compliance Checklist & Sign-off":
    from application_pages.page_compliance_signoff import run_page_compliance_signoff
    run_page_compliance_signoff()
elif page == "Export & Audit":
    from application_pages.page_export_audit import run_page_export_audit
    run_page_export_audit()
