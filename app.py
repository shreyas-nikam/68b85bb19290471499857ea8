
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Drafting AML Suspicious Activity Reports")
st.divider()
st.markdown("""
In this lab, we explore how to leverage AI to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). The goal is to automate the generation of first-draft SAR narratives, summarize transaction timelines, and suggest potential typologies. It is crucial to remember that this tool is designed to **assist human analysts**, and all AI-generated outputs require **human review, auditability, and strict compliance with regulatory guidance**.

### Learning Goals:

*   **Automated First-Draft SAR Narratives**: Learn how a direct Large Language Model (LLM) call can generate initial SAR narratives, adhering to regulatory guidance without relying on Retrieval-Augmented Generation (RAG). This emphasizes the importance of carefully engineered prompts.
*   **Key Information Extraction (The 5Ws)**: Understand how to extract critical information (Who, What, When, Where, Why) from case data. This information is fundamental for guiding the LLM to produce focused and compliant narratives.
*   **Human-in-the-Loop Review**: Practice the essential human-in-the-loop process, performing compliance checks and refining the AI-generated narrative before final export to ensure accuracy and regulatory adherence.

### SAR Workflow Overview:

This application guides the user through a structured SAR workflow, mirroring the typical stages an AML analyst would follow:

1.  **Case Intake**: Upload and get an initial overview of case-related data.
2.  **Explore Data**: Deep dive into transactions and related activities with interactive visualizations and filters.
3.  **Draft SAR**: Generate a preliminary SAR narrative based on selected facts and extracted 5Ws using an LLM.
4.  **Review & Compare**: Compare the AI-generated draft with analyst edits, and refine the narrative.
5.  **Compliance Checklist & Sign-off**: Ensure the narrative meets all regulatory requirements and obtain official sign-off.
6.  **Export & Audit**: Finalize and export the SAR, along with an audit trail.

All data is managed using Streamlit's session state (`st.session_state`) to maintain consistency across pages.

### Mathematical Operations for KPIs:

Key Performance Indicators (KPIs) like Total Transaction Volume and Average Transaction Amount are calculated as follows:

*   **Total Volume**: $$ \text{Total Volume} = \sum_{i=1}^{N} \text{transaction\_amount}_i $$
*   **Average Amount**: $$ \text{Average Amount} = \frac{\text{Total Volume}}{\text{Number of Transactions}} $$


""")

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", "Export & Audit"])

# Initialize session state for data if not already present
if "data" not in st.session_state:
    st.session_state.data = {}
    # Placeholder for loading synthetic data or actual data
    # In a real application, this would involve loading data from a secure source
    # For this lab, we will use the load_synthetic_data function later.

if page == "Case Intake":
    from application_pages.page1 import run_page
    run_page()
elif page == "Explore Data":
    from application_pages.page2 import run_page
    run_page()
elif page == "Draft SAR":
    from application_pages.page3 import run_page
    run_page()
elif page == "Review & Compare":
    from application_pages.page4 import run_page
    run_page()
elif page == "Compliance Checklist & Sign-off":
    from application_pages.page5 import run_page
    run_page()
elif page == "Export & Audit":
    from application_pages.page6 import run_page
    run_page()
# Your code ends
