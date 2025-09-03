import streamlit as st
import pandas as pd # Added for session state initialization, if needed globally
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AML SAR Drafting Assistant")
st.divider()
st.markdown('''
In this lab, we explore an AI-driven approach to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). This application is designed to streamline the SAR workflow by leveraging Large Language Models (LLMs) to generate first-draft narratives, summarize transaction timelines, and suggest typologies.

**Learning Goals:**

*   Assist AML analysts by generating **first-draft SAR narratives**, summarizing transaction timelines, and suggesting typologies—**always** with human review, auditability, and compliance guardrails.
*   See how a **direct LLM call** can automate first-draft SAR narratives while strictly following regulatory guidance, without relying on Retrieval-Augmented Generation (RAG).
*   Learn to **extract key information** (the 5Ws: Who, What, When, Where, Why) from case data, which is crucial for steering the LLM in generating a focused and compliant narrative.
*   Practice **human-in-the-loop** review and perform compliance checks on the generated narrative before its final export, ensuring accuracy and regulatory adherence.

---

### About / Controls

This panel provides an overview of key regulatory and operational considerations for SAR drafting and AI assurance.

*   **BSA/FinCEN SAR Requirements:** The Bank Secrecy Act (BSA) requires financial institutions to report suspicious transactions to the Financial Crimes Enforcement Network (FinCEN). SARs are critical tools in combating money laundering and terrorist financing.
*   **FinCEN Narrative Guidance:** FinCEN provides specific guidance on writing SAR narratives, emphasizing clarity, conciseness, chronology, and factual accuracy. Narratives should answer the 5Ws (Who, What, When, Where, Why) without speculation.
*   **OCC/SR 11-7 Model Risk Management:** The Office of the Comptroller of the Currency (OCC) and the Federal Reserve (SR 11-7) provide guidance on model risk management, which is highly relevant when deploying AI models in critical functions like SAR drafting. This includes model validation, governance, and ongoing monitoring.
*   **MITRE AI Assurance Cues:** The MITRE ATLAS framework offers a knowledge base of adversary tactics and techniques for AI systems, helping to identify and mitigate risks associated with AI deployment, including fairness, transparency, and robustness.

''')
# Initialize session state for common variables
if "case_data" not in st.session_state:
    st.session_state.case_data = None
if "kpis" not in st.session_state:
    st.session_state.kpis = {}
if "extracted_5ws" not in st.session_state:
    st.session_state.extracted_5ws = {}
if "ai_draft_narrative" not in st.session_state:
    st.session_state.ai_draft_narrative = ""
if "analyst_edited_narrative" not in st.session_state:
    st.session_state.analyst_edited_narrative = ""
if "narrative_versions" not in st.session_state:
    st.session_state.narrative_versions = []
if "compliance_checklist_results" not in st.session_state:
    st.session_state.compliance_checklist_results = []
if "sign_off_details" not in st.session_state:
    st.session_state.sign_off_details = {}
if "audit_trail" not in st.session_state:
    st.session_state.audit_trail = []

page = st.sidebar.selectbox(label="Navigation", options=["Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", "Export & Audit"])
if page == "Case Intake":
    from application_pages.page_case_intake import run_page
    run_page()
elif page == "Explore Data":
    from application_pages.page_explore_data import run_page
    run_page()
elif page == "Draft SAR":
    from application_pages.page_draft_sar import run_page
    run_page()
elif page == "Review & Compare":
    from application_pages.page_review_compare import run_page
    run_page()
elif page == "Compliance Checklist & Sign-off":
    from application_pages.page_compliance_checklist import run_page
    run_page()
elif page == "Export & Audit":
    from application_pages.page_export_audit import run_page
    run_page()
