
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we explore how Artificial Intelligence (AI) can assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). The primary goal is to **automate the generation of first-draft SAR narratives**, summarize transaction timelines, and suggest potential typologies. It is crucial to remember that **human review, auditability, and strict compliance guardrails are always paramount**.

### Learning Goals:

*   **Automate First-Draft SAR Narratives**: Learn to leverage direct Large Language Model (LLM) calls to generate initial SAR narratives that adhere to regulatory guidance, specifically without relying on Retrieval-Augmented Generation (RAG). This showcases how LLMs can streamline the initial drafting process while maintaining compliance standards.

*   **Extract Key Information (5Ws)**: Understand the importance of extracting the "5Ws" (Who, What, When, Where, Why) from case data. This foundational step is vital for guiding the LLM to produce focused, accurate, and compliant narratives, ensuring all critical aspects of a suspicious activity are covered.

*   **Human-in-the-Loop Review**: Practice the essential "human-in-the-loop" approach by reviewing and performing compliance checks on the AI-generated narrative. This step ensures accuracy, identifies any potential errors or omissions, and confirms adherence to all regulatory requirements before the final export.

*   **Compliance & Audit**: Learn how to implement and utilize a compliance checklist and audit trail. This ensures that every step of the SAR drafting process is traceable, transparent, and meets regulatory scrutiny, providing a robust framework for accountability.

### Formula Handling:

If you have formulae that use backslashes, either:
- Use `st.latex()` for standalone formulae, or
- Use the `r` prefix for raw strings within `st.markdown()` to prevent backslash interpretation issues.

For combinations of raw strings and f-strings, render them properly:
```python
st.markdown(r"$H_{\alpha}$ value:"
            f"{H_alpha_value}")
```

### BSA/FinCEN SAR Requirements Overview

The Bank Secrecy Act (BSA) requires financial institutions to assist U.S. government agencies in detecting and preventing money laundering. A key component of BSA compliance is the filing of Suspicious Activity Reports (SARs).

FinCEN provides detailed guidance for SAR narratives, emphasizing that they should be:

*   **Clear**: Easy to understand, free of jargon where possible.
*   **Concise**: To the point, including only relevant information.
*   **Chronological**: Events described in the order they occurred.
*   **Complete**: Containing all necessary details for law enforcement.
*   **Factual**: Based on evidence, avoiding speculation or conclusions.

**Key elements to include in a SAR narrative often revolve around the "5 Ws":**

*   **Who**: Individuals or entities involved (account holders, beneficiaries, counterparties).
*   **What**: The type of suspicious activity or transactions (e.g., structuring, wire transfers, deposits).
*   **When**: Dates and times of the suspicious activity.
*   **Where**: Locations involved (branches, geographic areas, virtual addresses).
*   **Why**: The reasons for suspicion (e.g., unusual activity, deviation from normal patterns, red flags).

### OCC/SR 11-7 Model Risk Management

For AI-powered tools like this SAR drafting assistant, it's important to consider OCC/SR 11-7 guidance on model risk management. This guidance emphasizes robust processes for model development, implementation, and use, including:

*   **Model Validation**: Independent review of model design, implementation, and outputs.
*   **Governance**: Clear roles and responsibilities, policies, and procedures.
*   **Documentation**: Comprehensive documentation of model design, assumptions, and limitations.
*   **Ongoing Monitoring**: Regular monitoring of model performance and data quality.

This application aims to support, not replace, human judgment, and therefore incorporates features like human-in-the-loop review and audit trails to align with these principles.

### MITRE AI Assurance Cues

MITRE's AI Assurance program provides a framework for evaluating the trustworthiness of AI systems. For this application, key assurance cues include:

*   **Transparency**: Clearly indicating when content is AI-generated and allowing for human modification.
*   **Explainability**: Providing context for AI suggestions, linking narratives to underlying data.
*   **Robustness**: Ensuring the AI performs reliably under varying inputs.
*   **Fairness**: Mitigating biases in data and model outputs.
*   **Security**: Protecting sensitive data used by the AI.

By incorporating these considerations, we aim to build a responsible and trustworthy AI assistant for AML analysts.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", "Export & Audit"])

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
    from application_pages.page_compliance_checklist import run_page_compliance_checklist
    run_page_compliance_checklist()
elif page == "Export & Audit":
    from application_pages.page_export_audit import run_page_export_audit
    run_page_export_audit()
# Your code ends
