# QuLab: AML SAR Drafting Assistant

## Project Title and Description

**QuLab: AML SAR Drafting Assistant** is a Streamlit application designed to streamline the drafting of Anti-Money Laundering (AML) Suspicious Activity Reports (SARs). This tool aims to enhance the efficiency and accuracy of AML analysts by providing AI-assisted features throughout the SAR generation process. The application guides analysts through a structured workflow, including case intake, data exploration, SAR draft generation (powered by a Large Language Model), review and comparison, compliance checks, and export/audit functionalities.

## Features

*   **Case Intake:** Upload and get a preliminary overview of case data. Displays key statistics and potential AML typologies.
*   **Explore Data:** Interactively analyze transactions, customer relationships, and geographic patterns using advanced visualizations (timeline, geo map, counterparty network graph).
*   **Draft SAR:** Generate an initial SAR narrative using an LLM, steered by extracted key facts.
*   **Review & Compare:** Review, edit, and compare the AI-generated draft with the analyst's final version.
*   **Compliance Checklist & Sign-off:** Validate the narrative against a compliance checklist and facilitate formal sign-off.
*   **Export & Audit:** Export the final SAR package, including the narrative, facts, checklist report, and a detailed audit trail.
*   **Synthetic Data Generation:** The application includes a synthetic data generation capability for demonstration and testing purposes.
*   **Direct LLM Integration:** Uses direct LLM calls for SAR narrative generation, focusing on regulatory compliance (e.g., FinCEN guidelines) without relying on Retrieval-Augmented Generation (RAG).
*   **Human-in-the-Loop Review:** Emphasizes the essential role of human expertise in reviewing and validating AI-generated narratives.
*   **Auditability and Compliance Guardrails:** Provides features that ensure every step of the SAR drafting process is auditable, transparent, and aligned with compliance requirements.

## Getting Started

### Prerequisites

*   **Python 3.8+:**  Ensure you have Python 3.8 or a later version installed.
*   **Poetry:** Installation and management of virtual environments.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd QuLab-SAR-Assistant  # Or whatever the repo is named locally.
    ```

2.  **Install Poetry:**

    ```bash
    pip install poetry
    ```

3.  **Create and activate a virtual environment using Poetry:**

    ```bash
    poetry install
    poetry shell
    ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt  # This is important if poetry install fails, it should not, but it's here as a fallback.
    ```

5.  **Environment Variables (Optional - Local Development):**

    *   Create a `.env` file in the root directory of the project.
    *   Add any required environment variables to the `.env` file.  (e.g., API Keys if needed to connect to LLMs.)

    ```
    # .env example (if an API key is needed)
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    ```

    **Important:** For production deployments, it's highly recommended to manage secrets securely using a dedicated secrets manager service (e.g., Kubernetes secrets, AWS Secrets Manager) instead of a `.env` file.

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2.  **Access the application:**

    Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

3.  **Navigate the Application:**

    Use the sidebar navigation to access different pages:

    *   **Case Intake:** Load and view case data.
    *   **Explore Data:** Interact with data visualizations.
    *   **Draft SAR:** Generate an initial SAR draft.
    *   **Review & Compare:** Review and edit the SAR draft.
    *   **Compliance Checklist & Sign-off:** Perform compliance checks and sign-off.
    *   **Export & Audit:** Export the SAR package.

## Project Structure

```
QuLab-SAR-Assistant/
├── app.py                    # Main Streamlit application script
├── application_pages/        # Directory containing individual page scripts
│   ├── page1_case_intake.py
│   ├── page2_explore_data.py
│   ├── page3_draft_sar.py
│   ├── page4_review_compare.py
│   ├── page5_compliance_signoff.py
│   └── page6_export_audit.py
├── .env                     # (Optional) Environment variables (for local development only)
├── README.md                 # This file
├── requirements.txt          # List of Python dependencies
└── poetry.lock             # Poetry lock file
└── pyproject.toml          # Poetry configuration
```

## Technology Stack

*   **Streamlit:**  For building the interactive web application.
*   **Pandas:**  For data manipulation and analysis.
*   **Numpy:**  For numerical operations.
*   **Plotly:**  For creating interactive visualizations.
*   **NetworkX:** For creating and manipulating network graphs.
*   **python-dotenv:** For loading environment variables from a `.env` file (optional, for local development).

## Contributing

Contributions are welcome! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, descriptive messages.
4.  Submit a pull request to the main branch.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or feedback, please contact:

*   [QuantUniversity](https://www.quantuniversity.com/)
