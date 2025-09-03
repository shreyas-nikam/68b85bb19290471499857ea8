id: 68b85bb19290471499857ea8_documentation
summary: Drafting AML Suspicious Activity Reports Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AML SAR Drafting Assistant Codelab

This codelab guides you through QuLab, an AI-driven application designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). You will learn how to leverage Large Language Models (LLMs) to generate initial SAR narratives, summarize transaction timelines, and suggest typologies, all while adhering to regulatory guidelines and maintaining human oversight. This tool is intended to streamline the SAR workflow, improve efficiency, and ensure compliance.  You will explore concepts like direct LLM calls for narrative generation, information extraction for prompt engineering, and the importance of human-in-the-loop review.

## Setting Up the Environment

Duration: 00:05

Before diving into the application, ensure you have the following:

*   **Python Environment:** A Python 3.7+ environment is required.
*   **Streamlit:** Install Streamlit using `pip install streamlit`.
*   **Dependencies:** The application uses `pandas` and `plotly`. Install them using `pip install pandas plotly`.

## Running the Application

Duration: 00:02

1.  Save the provided code into separate `.py` files, maintaining the directory structure (e.g., `app.py`, `application_pages/page_case_intake.py`, etc.).

2.  Navigate to the directory containing `app.py` in your terminal.

3.  Run the application using the command: `streamlit run app.py`.

4.  Streamlit will automatically open the application in your web browser.

## Exploring the Application Pages

Duration: 00:05

The application consists of several pages accessible through the sidebar navigation. Let's briefly introduce each page:

*   **Case Intake:** This page allows you to upload case data or load synthetic data for testing.
*   **Explore Data:** This page provides tools to visualize and explore the loaded case data.
*   **Draft SAR:** This is the core page where the AI-powered narrative generation takes place.
*   **Review & Compare:** This page facilitates the review and comparison of different narrative versions.
*   **Compliance Checklist & Sign-off:** This page guides you through a compliance checklist and allows for final sign-off.
*   **Export & Audit:** This page enables the export of the final SAR and provides an audit trail.

## Case Intake

Duration: 00:10

This page focuses on loading data into the application.

1.  **Uploading Data:** The page provides a file uploader where you can upload case bundles in CSV or Excel format. This functionality is currently a placeholder and assumes that uploaded files contain transaction data. The application attempts to read the CSV file, displays the head of the dataframe, and calculates summary KPIs.

2.  **Loading Synthetic Data:** If you don't have a case bundle available, you can use the "Load Synthetic Data" button.  This will load a sample dataset into the application.  The synthetic data includes `customers`, `transactions`, `alerts`, and `notes` dataframes.  The transactions dataframe is used to generate and display summary KPIs.

3.  **KPIs Display:** After loading data, the page calculates and displays summary KPIs such as the total number of transactions, total transaction volume, and average transaction amount.

4.  **Possible Typologies:**  This section is a placeholder for suggesting potential typologies based on the loaded data.

```python
import streamlit as st
import pandas as pd


def load_synthetic_data():
    # Placeholder for synthetic data loading/generation function
    data = {
        "customers": pd.DataFrame({"customer_id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]}),
        "transactions": pd.DataFrame({"transaction_id": [101, 102, 103], "customer_id": [1, 2, 3], "amount": [100, 200, 150], "timestamp": pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])}),
        "alerts": pd.DataFrame({"alert_id": [1001, 1002], "customer_id": [1, 2], "description": ["Unusual transaction", "High-value transfer"]}),
        "notes": pd.DataFrame({"note_id": [1, 2], "customer_id": [1, 2], "text": ["Customer inquiry", "Follow-up call"]})
    }
    return data


def calculate_summary_kpis(transactions):
    # Placeholder for KPI calculation function
    kpis = {
        "total_transactions": len(transactions),
        "total_volume": transactions["amount"].sum(),
        "average_amount": transactions["amount"].mean()
    }
    return kpis


def run_page():
    st.header("Case Intake")

    # File uploader for case bundles (replace with actual implementation)
    uploaded_file = st.file_uploader("Upload Case Bundle (e.g., CSV, Excel)")

    if uploaded_file is not None:
        # Placeholder: Load data from the uploaded file
        try:
            case_data = pd.read_csv(uploaded_file)
            st.session_state.case_data = case_data  # Store in session state

            # Basic display of loaded data
            st.subheader("Uploaded Data Preview")
            st.dataframe(case_data.head())

            # Calculate and display summary KPIs
            kpis = calculate_summary_kpis(case_data)
            st.session_state.kpis = kpis
            st.subheader("Summary KPIs")
            st.write(f"Total Transactions: {kpis['total_transactions']}")
            st.write(f"Total Transaction Volume: {kpis['total_volume']}")
            st.write(f"Average Transaction Amount: {kpis['average_amount']}")

        except Exception as e:
            st.error(f"Error loading data: {e}")

    else:
        st.info("Please upload a case bundle to proceed.")

        # Option to load synthetic data if no file is uploaded
        if st.button("Load Synthetic Data"): # Using a button for demonstration
            synthetic_data = load_synthetic_data()
            st.session_state.case_data = synthetic_data

            # Calculate and display summary KPIs
            transactions = synthetic_data['transactions']
            kpis = calculate_summary_kpis(transactions)
            st.session_state.kpis = kpis

            st.subheader("Synthetic Data Loaded")
            st.write("Preview of synthetic transaction data:")
            st.dataframe(transactions.head())

            st.subheader("Summary KPIs (Synthetic Data)")
            st.write(f"Total Transactions: {kpis['total_transactions']}")
            st.write(f"Total Transaction Volume: {kpis['total_volume']}")
            st.write(f"Average Transaction Amount: {kpis['average_amount']}")


    # Display quick stats if case data is available (either uploaded or synthetic)
    if st.session_state.case_data is not None:
        st.subheader("Quick Stats")
        if isinstance(st.session_state.case_data, dict):
            num_transactions = len(st.session_state.case_data['transactions'])
            total_in = st.session_state.case_data['transactions']['amount'].sum()

            st.write(f"Number of Transactions: {num_transactions}")
            st.write(f"Total Transaction Volume: ${total_in:,.2f}")
        elif isinstance(st.session_state.case_data, pd.DataFrame):
            num_transactions = len(st.session_state.case_data)
            total_in = st.session_state.case_data['amount'].sum()
            st.write(f"Number of Transactions: {num_transactions}")
            st.write(f"Total Transaction Volume: ${total_in:,.2f}")

        st.subheader("Possible Typologies")
        # Placeholder for typology suggestions based on loaded data
        st.write("Typologies will be suggested here based on the loaded case data.")

if __name__ == "__main__":
    run_page()
```

## Explore Data

Duration: 00:05

This page is designed to help you visualize and explore the case data that was loaded in the "Case Intake" page. Currently, it includes a placeholder for a timeline visualization.

1.  **Timeline Visualization:**  The core functionality of this page is intended to be a timeline visualization of transactions.  This visualization would ideally use a library like Plotly to create an interactive chart.

```python
import streamlit as st
import pandas as pd
import plotly.express as px


def create_timeline_visualization(transactions):
    # Placeholder for timeline visualization function
    # Replace with actual implementation using Plotly
    fig = px.line(transactions, x="timestamp", y="amount", title="Transaction Timeline")
    st.plotly_chart(fig)


def run_page():
    st.header("Explore Data")

    if st.session_state.case_data is None:
        st.info("Please load case data first in the 'Case Intake' page.")
    else:
        # Ensure that st.session_state.case_data['transactions'] exists and is a DataFrame
        if isinstance(st.session_state.case_data, dict) and 'transactions' in st.session_state.case_data:
            transactions = st.session_state.case_data['transactions']
        elif isinstance(st.session_state.case_data, pd.DataFrame):
            transactions = st.session_state.case_data
        else:
            st.error("Invalid case data format.  Please ensure the 'case_data' object is accessible and 'transactions' data available in correct format.")
            return  # Exit the function early if data is invalid

        st.subheader("Transaction Timeline")
        create_timeline_visualization(transactions)  # Pass transaction data to the function

if __name__ == "__main__":
    run_page()

```

## Draft SAR

Duration: 00:15

This page is the heart of the application, where the AI-powered SAR narrative generation takes place.

1.  **5Ws Extraction:**  The application first attempts to extract the 5Ws (Who, What, When, Where, Why) from the loaded case data.  This is a crucial step for creating a focused and compliant prompt for the LLM. Currently, the extraction is implemented as a placeholder, returning hardcoded values.

2.  **Prompt Building:**  A prompt is constructed based on the case data and the extracted 5Ws. This prompt is designed to guide the LLM in generating a SAR narrative that adheres to FinCEN guidelines.  Currently, the prompt building process is minimal and mainly focuses on including the case data.

3.  **LLM Call:**  The constructed prompt is then passed to a Large Language Model (LLM) to generate the initial SAR narrative.  This step is currently implemented as a placeholder, returning a sample narrative. In a real-world application, this would involve an API call to an LLM service.

4.  **AI Narrative Display:**  The generated AI narrative is displayed to the user.  A disclaimer is added to emphasize the need for human review and compliance checks.

```python
import streamlit as st


def extract_5ws(case_data):
    # Placeholder for 5Ws extraction function
    fives_ws = {
        "who": "John Doe",
        "what": "Suspicious transaction",
        "when": "2024-01-05",
        "where": "Offshore account",
        "why": "Unexplained source of funds"
    }
    return fives_ws


def build_prompt(case_data, extracted_5ws):
    # Placeholder for prompt building function
    prompt = f"""Based on the following case data: {case_data}\n"""
    return prompt


def call_llm(prompt):
    # Placeholder for LLM call function
    narrative = "This is a sample AI-generated narrative. Needs human review!"
    return narrative


def generate_ai_narrative(case_data, extracted_5ws):
    # Placeholder for AI narrative generation
    prompt = build_prompt(case_data, extracted_5ws)
    ai_narrative = call_llm(prompt)
    ai_narrative += "\n\nAI-assisted draft. Requires human review and compliance checks."
    return ai_narrative


def run_page():
    st.header("Draft SAR")

    if st.session_state.case_data is None:
        st.info("Please load case data first in the 'Case Intake' page.")
        return

    st.subheader("AI-Generated Draft Narrative")

    # Generate AI narrative if it doesn't exist
    if not st.session_state.ai_draft_narrative:
        extracted_5ws = extract_5ws(st.session_state.case_data)
        st.session_state.extracted_5ws = extracted_5ws
        st.session_state.ai_draft_narrative = generate_ai_narrative(st.session_state.case_data, extracted_5ws)

    st.write(st.session_state.ai_draft_narrative)


if __name__ == "__main__":
    run_page()
```

## Review & Compare

Duration: 00:05

This page provides a space for analysts to review the AI-generated narrative, make edits, and compare different versions. The current implementation includes a text area for editing the narrative, but version control and comparison features are placeholders.

1.  **Analyst Edits:** Allows the analyst to review and edit the AI-generated narrative in a text area.

2.  **Save Version:** A button to save the current edited narrative as a new version. This functionality is a placeholder.

3.  **Version Comparison:** Intended to allow users to compare different versions of the narrative side-by-side. This is currently a placeholder.

```python
import streamlit as st

def run_page():
    st.header("Review & Compare")

    if st.session_state.ai_draft_narrative == "":
        st.info("Please generate an AI draft narrative first in the 'Draft SAR' page.")
    else:
        st.subheader("AI-Generated Draft Narrative")
        st.write(st.session_state.ai_draft_narrative)

        st.subheader("Analyst Review & Edits")
        analyst_edited_narrative = st.text_area("Edit the narrative:", st.session_state.ai_draft_narrative, height=300)

        if st.button("Save Edited Version"):
            st.session_state.analyst_edited_narrative = analyst_edited_narrative  # Store the edited narrative
            st.success("Edited version saved!")  # Provide feedback

        if st.session_state.analyst_edited_narrative:  # Show the stored narrative
            st.subheader("Saved Edited Narrative:")
            st.write(st.session_state.analyst_edited_narrative)

if __name__ == "__main__":
    run_page()
```

## Compliance Checklist & Sign-off

Duration: 00:05

This page guides the analyst through a compliance checklist and allows for final sign-off of the SAR.

1.  **Compliance Checklist:** A series of checkboxes representing compliance checks.  These are currently hardcoded.

2.  **Sign-off Details:** Fields for entering sign-off details, such as the analyst's name and date.

3.  **Sign-off Confirmation:**  A button to confirm the sign-off.

```python
import streamlit as st

def run_page():
    st.header("Compliance Checklist & Sign-off")

    if st.session_state.ai_draft_narrative == "":
        st.info("Please generate an AI draft narrative first in the 'Draft SAR' page.")
    else:
        st.subheader("Compliance Checklist")
        # Example compliance checks
        check1 = st.checkbox("Narrative is clear and concise")
        check2 = st.checkbox("Narrative answers the 5Ws")
        check3 = st.checkbox("Narrative avoids speculation")
        check4 = st.checkbox("All transactions are accurately described")

        st.subheader("Sign-off Details")
        analyst_name = st.text_input("Analyst Name")
        sign_off_date = st.date_input("Date")

        if st.button("Sign-off"):
            # Store the sign-off details in session state
            st.session_state.sign_off_details = {
                "analyst_name": analyst_name,
                "sign_off_date": sign_off_date,
                "compliance_checks": [check1, check2, check3, check4]
            }
            st.success("SAR signed off!")

if __name__ == "__main__":
    run_page()
```

## Export & Audit

Duration: 00:05

This page enables the export of the final SAR and provides an audit trail.  The current implementation features placeholder functionality.

1.  **Export SAR:** A button to export the final SAR in a desired format (e.g., PDF, Word). This is currently a placeholder.

2.  **Audit Trail:** Displays an audit trail of all actions performed within the application, including narrative versions, compliance checks, and sign-off details.  This is currently a placeholder.

```python
import streamlit as st

def run_page():
    st.header("Export & Audit")

    if st.session_state.sign_off_details == {}:
        st.info("Please complete the Compliance Checklist & Sign-off first.")
    else:
        st.subheader("Export SAR")
        if st.button("Export SAR"):
            st.write("SAR Exported") # Placeholder for SAR export function

        st.subheader("Audit Trail")
        st.write("Placeholder: Audit trail will be displayed here, including all actions taken, versions of the narrative, compliance checks, and sign-off details.")

if __name__ == "__main__":
    run_page()
```

## Enhancements and Next Steps

Duration: 00:10

This codelab provides a basic framework for an AI-powered SAR drafting assistant.  Here are some potential enhancements and next steps:

*   **Implement Real LLM Integration:** Replace the placeholder LLM call with an actual API call to a language model service like OpenAI, Google Cloud AI Platform, or Azure AI.
*   **Improve 5Ws Extraction:** Develop a more robust 5Ws extraction module using techniques like Named Entity Recognition (NER) and relationship extraction.
*   **Refine Prompt Engineering:** Experiment with different prompt templates and strategies to optimize the LLM's narrative generation capabilities.
*   **Implement Version Control:** Implement version control for the SAR narratives, allowing users to easily compare and revert to previous versions.
*   **Develop Compliance Checklist Logic:**  Connect the compliance checklist to specific aspects of the SAR narrative and provide guidance to analysts.
*   **Implement Export Functionality:**  Implement the export functionality to generate SARs in various formats.
*   **Enhance Audit Trail:**  Develop a comprehensive audit trail that captures all user actions, data changes, and system events.
*   **Integrate with Existing AML Systems:** Explore integration with existing AML systems to streamline data input and output.
*   **Implement RAG (Retrieval-Augmented Generation):**  Consider using RAG to retrieve relevant information from internal databases and external sources to enhance the LLM's knowledge base.

<aside class="positive">
Remember to always prioritize human oversight, auditability, and compliance when deploying AI in critical functions like SAR drafting.
</aside>

This codelab provided a walkthrough of QuLab: AML SAR Drafting Assistant application. You explored different functionalities of the application and understood how it can be used to assist AML analysts in drafting Suspicious Activity Reports (SARs).
