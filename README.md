# QuLab: Drafting AML Suspicious Activity Reports with AI

## Project Title and Description

QuLab is a Streamlit application designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). This tool leverages AI to generate first-draft SAR narratives, summarize transaction timelines, and suggest potential typologies, emphasizing human review, auditability, and compliance guardrails. The application provides a multi-page workflow that guides users through case intake, data exploration, SAR drafting, review, compliance checks, and final export, streamlining the initial SAR generation process.

## Features

*   **Case Intake:**
    *   Upload case data (e.g., CSV, JSON) or generate synthetic data for demonstration.
    *   Display summary KPIs, including total transactions, inflow, outflow, number of customers and branches involved, and the time window of the transactions.
    *   Suggest potential typologies based on the loaded data.
*   **Explore Data:**
    *   Interactive visualizations for exploring transaction data:
        *   Timeline of activity.
        *   Geographic map of transaction locations.
        *   Counterparty network graph.
        *   Heatmaps of transaction intensity by day of the week and hour of day, as well as alert density over time.
    *   Data filtering using date range, amount range, transaction channel, and branch.
    *   A "Draft Facts Tray" to collect important pieces of information for the narrative.
*   **Draft SAR:**
    *   AI-assisted generation of a first-draft SAR narrative using an LLM (Large Language Model) and the extracted 5Ws.
    *   Displays the AI-generated narrative in a read-only text area.
*   **Review & Compare:**
    *   Rich text editor for reviewing and editing the AI-generated SAR narrative.
    *   Version control and audit logging for tracking changes.
    *   Diff viewer for comparing the AI draft with the analyst-edited version, highlighting changes.
    *   (Conceptual) Explainability Panel that would link sentences in the narrative to the data that supports them.
*   **Compliance Checklist & Sign-off:**
    *   Compliance checklist to ensure the SAR meets regulatory requirements, including presence of 5Ws, chronology, clarity, avoidance of speculation, and adherence to length bounds.
    *   Sign-off section for formal approval by a Compliance Officer.
*   **Export & Audit:**
    *   Export the final SAR narrative, supporting facts, compliance checklist report, and audit trail in JSON format.
    *   Download the audit trail in CSV or JSON format.
    *   Content immutability verification using SHA256 hashing.

## Getting Started

### Prerequisites

*   Python 3.7 or higher
*   Streamlit
*   Pandas
*   Plotly
*   NetworkX
*   spaCy (and the `en_core_web_sm` model)
*   streamlit_richtext (for the richtext editor)
*   hashlib (for content verification)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install streamlit pandas plotly networkx spacy streamlit_richtext
    python -m spacy download en_core_web_sm
    ```

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Open the application in your browser:**

    The application should open automatically in your default web browser. If not, navigate to the address displayed in the terminal (usually `http://localhost:8501`).

3.  **Basic Usage:**

    *   **Case Intake:**
        *   Upload your case data or generate synthetic data using the button provided.
        *   Review the summary KPIs displayed.
    *   **Explore Data:**
        *   Use the interactive visualizations to analyze your transaction data.
        *   Apply filters to narrow down your focus.
        *   Add relevant facts to the "Draft Facts Tray."
    *   **Draft SAR:**
        *   Click the "Generate Draft Narrative" button to generate an AI-assisted SAR draft.
    *   **Review & Compare:**
        *   Review and edit the generated draft in the rich text editor.
        *   Save your changes and compare them with the original draft.
    *   **Compliance Checklist & Sign-off:**
        *   Run the compliance checks and ensure all items meet the requirements.
        *   Have the Compliance Officer sign off the SAR.
    *   **Export & Audit:**
        *   Export the completed SAR package, including the narrative, facts, checklist, and audit trail.

## Project Structure

```
QuLab/
├── app.py                          # Main Streamlit application file
├── application_pages/            # Directory containing individual page logic
│   ├── case_intake.py            # Logic for the Case Intake page (deprecated)
│   ├── explore_data.py           # Logic for the Explore Data page (deprecated)
│   ├── draft_sar.py              # Logic for the Draft SAR page (deprecated)
│   ├── review_compare.py         # Logic for the Review & Compare page (deprecated)
│   ├── compliance_checklist.py  # Logic for the Compliance Checklist & Sign-off page (deprecated)
│   ├── export_audit.py            # Logic for the Export & Audit page (deprecated)
│   ├── utils.py                   # Utility functions (data loading, visualization, etc.)
│   ├── page_case_intake.py            # Logic for the Case Intake page
│   ├── page_explore_data.py           # Logic for the Explore Data page
│   ├── page_draft_sar.py              # Logic for the Draft SAR page
│   ├── page_review_compare.py         # Logic for the Review & Compare page
│   ├── page_compliance_signoff.py  # Logic for the Compliance Checklist & Sign-off page
│   ├── page_export_audit.py            # Logic for the Export & Audit page
├── README.md                       # This README file
└── venv/                           # Virtual environment (optional)
```

## Technology Stack

*   **Streamlit:** For creating the interactive web application.
*   **Pandas:** For data manipulation and analysis.
*   **Plotly:** For creating visualizations.
*   **NetworkX:** For creating network graphs.
*   **spaCy:** For natural language processing (not actively used currently, but kept for potential future expansion).
*   **streamlit_richtext:** For an enhanced text editing experience in the Review & Compare page.
*   **hashlib:** for content verification of final SAR.

## Contributing

Contributions are welcome! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Test your changes thoroughly.
5.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or feedback, please contact:

*   [QuantUniversity](https://www.quantuniversity.com/)
*   [Your Name/Email]
