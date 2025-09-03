
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
