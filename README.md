# QuLab: AML SAR Drafting Assistant

## Project Title and Description

QuLab is a Streamlit application designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). This application streamlines the SAR workflow by leveraging Large Language Models (LLMs) to generate first-draft narratives, summarize transaction timelines, and suggest typologies.  It is designed to be a tool that assists in drafting, but **requires human review, auditability, and compliance guardrails**.

This project is part of a lab setting and is intended for educational and demonstrational purposes, showcasing the application of AI in AML compliance.

## Features

*   **Case Intake:** Upload case data (e.g., transaction data, customer information) in CSV or Excel format or load synthetic data for demonstration.
*   **Data Exploration:** Visualize transaction data using interactive charts and graphs to identify patterns and anomalies. (Currently placeholder)
*   **AI-Powered SAR Draft Generation:** Leverage LLMs to generate first-draft SAR narratives based on extracted case data and regulatory guidance.
*   **Human-in-the-Loop Review:**  Review and edit the AI-generated narrative within the application to ensure accuracy and compliance.
*   **Compliance Checklist:**  Evaluate the SAR draft against a compliance checklist to adhere to regulatory requirements.
*   **Version Control:** Track different versions of the SAR narrative throughout the drafting and review process. (Currently placeholder)
*   **Export and Audit:** Export the final SAR draft and maintain an audit trail of changes made during the process. (Currently placeholder)

## Getting Started

### Prerequisites

*   Python 3.7+
*   Streamlit
*   Pandas
*   Plotly (for data visualization - Currently placeholder)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install streamlit pandas plotly  # plotly is optional, for future data visualization implementations.
    ```

    If you plan on integrating an LLM for SAR generation, you'll need to install the corresponding library (e.g., `openai`, `transformers` depending on your LLM of choice).  **Note:** The current code contains placeholders for LLM functionality.

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Access the application in your browser:**

    Open your browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

3.  **Basic Usage Instructions:**

    *   **Case Intake:** Upload your case data using the file uploader or load synthetic data.  Review the displayed summary KPIs.
    *   **Explore Data:** (Placeholder) Use the interactive charts to visualize transaction patterns and identify anomalies.
    *   **Draft SAR:** Generate an initial SAR draft using the AI-powered narrative generator.  Review and edit the generated narrative.
    *   **Review & Compare:** (Placeholder) Compare different versions of the SAR narrative.
    *   **Compliance Checklist & Sign-off:**  Complete the compliance checklist to ensure regulatory adherence and sign off on the final draft.
    *   **Export & Audit:** (Placeholder) Export the final SAR draft and view the audit trail.

## Project Structure

```
QuLab/
├── app.py                    # Main Streamlit application file
├── application_pages/          # Directory containing individual page modules
│   ├── page_case_intake.py     # Case intake page
│   ├── page_explore_data.py   # Data exploration page (Placeholder)
│   ├── page_draft_sar.py      # SAR drafting page
│   ├── page_review_compare.py # Review and comparison page (Placeholder)
│   ├── page_compliance_checklist.py # Compliance checklist and sign-off page (Placeholder)
│   └── page_export_audit.py   # Export and audit page (Placeholder)
├── README.md                 # This README file
└── venv/                     # (Optional) Virtual environment directory
```

## Technology Stack

*   **Streamlit:**  For building the interactive web application.
*   **Pandas:**  For data manipulation and analysis.
*   **Plotly:** For data visualization. (Currently placeholder)
*   **Large Language Model (LLM):**  (Integration required) Used for generating SAR narratives. The current implementation uses placeholders for the LLM integration.  Example libraries include:
    *   `openai`:  For using OpenAI models.
    *   `transformers`: For using Hugging Face transformers.

## Contributing

Contributions are welcome!  Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write clear and concise code with appropriate comments.
4.  Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE). (If applicable. Add the LICENSE file to the repository).  If no license is explicitly stated, all rights are reserved.

## Contact

*   [Your Name/Organization]
*   [Your Email]
*   [Link to your website/portfolio]

---

**Disclaimer:** This application is intended for educational and demonstrational purposes only and should not be used for actual SAR filing without thorough human review and validation by qualified AML professionals.  The AI-generated narratives are provided as a starting point and require careful scrutiny to ensure accuracy, completeness, and compliance with all applicable regulations.  The use of this application is at your own risk.
