"""import streamlit as st
st.set_page_config(page_title=\"QuLab\", layout=\"wide\")
st.sidebar.image(\"https://www.quantuniversity.com/assets/img/logo5.jpg\")
st.sidebar.divider()
st.title(\"QuLab\")
st.divider()
st.markdown("""
In this lab, we will be building a multi-page Streamlit application for drafting AML Suspicious Activity Reports (SARs). This application is designed to assist AML analysts by generating first-draft SAR narratives, summarizing transaction timelines, and suggesting typologies. It emphasizes human review, auditability, and compliance guardrails.

This application will guide you through the process of:

*   **Case Intake:** Uploading and reviewing case data.
*   **Explore Data:** Interactively exploring transaction data using visualizations.
*   **Draft SAR:** Generating an initial SAR draft using AI.
*   **Review & Compare:** Reviewing and editing the AI-generated draft.
*   **Compliance Checklist & Sign-off:** Ensuring the SAR meets compliance requirements.
*   **Export & Audit:** Exporting the final SAR and audit trail.

We will use Plotly for visualizations and Streamlit's session state to manage data across pages.
"""")
# Your code starts here
page = st.sidebar.selectbox(label=\"Navigation\", options=[\"Case Intake\", \"Explore Data\", \"Draft SAR\", \"Review & Compare\", \"Compliance Checklist & Sign-off\", \"Export & Audit\"])

if page == \"Case Intake\":
    from application_pages.case_intake import run_case_intake
    run_case_intake()
elif page == \"Explore Data\":
    from application_pages.explore_data import run_explore_data
    run_explore_data()
elif page == \"Draft SAR\":
    from application_pages.draft_sar import run_draft_sar
    run_draft_sar()
elif page == \"Review & Compare\":
    from application_pages.review_compare import run_review_compare
    run_review_compare()
elif page == \"Compliance Checklist & Sign-off\":
    from application_pages.compliance_checklist import run_compliance_checklist
    run_compliance_checklist()
elif page == \"Export & Audit\":
    from application_pages.export_audit import run_export_audit
    run_export_audit()
# Your code ends
"""))
```