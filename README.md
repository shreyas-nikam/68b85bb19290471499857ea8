# QuLab: AI-Powered SAR Drafting Assistant

## Project Description

QuLab is a Streamlit application designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). This application leverages Artificial Intelligence (AI) to automate the generation of first-draft SAR narratives, summarize transaction timelines, and suggest potential typologies.  It is designed with a focus on *human-in-the-loop review*, ensuring auditability, and adherence to strict compliance guardrails. The primary goal is to streamline the initial SAR drafting process, *not* to replace human judgment.

## Features

*   **Automated SAR Narrative Generation:** Uses Large Language Models (LLMs) to generate initial SAR narratives based on case data, without relying on Retrieval-Augmented Generation (RAG) initially.
*   **Key Information Extraction (5Ws):** Extracts essential information ("Who, What, When, Where, Why") from case data to guide the LLM in producing accurate and compliant narratives.
*   **Human-in-the-Loop Review:** Provides a workflow for analysts to review, edit, and perform compliance checks on AI-generated narratives.
*   **Compliance Checklist and Audit Trail:** Implements a compliance checklist and tracks all actions taken during the SAR drafting process for auditability.
*   **Data Exploration Tools:** Offers tools to explore and visualize transaction data to identify potential suspicious activity.
*   **Case Intake Module:** Allows users to input and manage case information efficiently.
*   **Review and Comparison:** Enables users to compare the AI-generated draft with the original case data and manually adjusted narratives.
*   **Export and Audit:** Provides functionality to export the final SAR narrative and associated audit trail.

## Getting Started

### Prerequisites

Before running QuLab, ensure you have the following installed:

*   **Python 3.7 or higher:**  Download Python from [python.org](https://www.python.org/).
*   **Poetry (recommended):** For dependency management.  Install with: `pip install poetry`
*   Alternatively: **pip:**  If you prefer using `pip` directly.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```

2.  **Install dependencies using Poetry (recommended):**
    ```bash
    poetry install
    ```

    or **Install dependencies using pip:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note:  A requirements.txt file will need to be manually created containing the list of necessary libraries for the application.  These are libraries such as: streamlit, pandas, etc.*

## Usage

1.  **Activate the Poetry environment (if using Poetry):**
    ```bash
    poetry shell
    ```

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the application:** Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

**Basic Usage:**

*   **Navigation:** Use the sidebar on the left to navigate between different sections of the application: "Case Intake", "Explore Data", "Draft SAR", "Review & Compare", "Compliance Checklist & Sign-off", and "Export & Audit".
*   **Case Intake:** Enter or upload case data. This data will be used by the AI to generate SAR narratives.
*   **Explore Data:** Use the data exploration tools to visualize and analyze transaction data.
*   **Draft SAR:** Generate an initial SAR narrative using the LLM.  Review and edit the generated text.
*   **Review & Compare:** Compare the AI-generated draft with the original case data and manually edited versions.
*   **Compliance Checklist & Sign-off:** Complete the compliance checklist to ensure the SAR meets regulatory requirements.  Sign off on the SAR.
*   **Export & Audit:** Export the final SAR narrative and audit trail for submission.

## Project Structure

```
QuLab/
├── app.py                    # Main Streamlit application file
├── application_pages/        # Directory containing code for each page of the application
│   ├── page_case_intake.py    # Case Intake page
│   ├── page_explore_data.py   # Explore Data page
│   ├── page_draft_sar.py      # Draft SAR page
│   ├── page_review_compare.py # Review & Compare page
│   ├── page_compliance_checklist.py # Compliance Checklist page
│   └── page_export_audit.py    # Export & Audit page
├── static/                   # Directory for static assets (e.g., images, data files)
│   └── ...
├── README.md                 # This file
└── requirements.txt           # List of Python dependencies (if using pip)
```

## Technology Stack

*   **Python:** Programming language
*   **Streamlit:** Web framework for building interactive data applications
*   **Pandas:** Data analysis and manipulation library
*   **Large Language Model (LLM):** For generating SAR narratives (specific LLM not specified in code, but would need to be integrated.  Examples: OpenAI's GPT, Google's Gemini, or other models.)
*   **Other libraries:** (Likely includes libraries for data visualization, API interaction with the LLM, and compliance checking)

## Contributing

We welcome contributions to QuLab! Please follow these guidelines:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix.
3.  **Make your changes** and write tests to ensure they work correctly.
4.  **Submit a pull request** with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details. *(Note: You'll need to create a LICENSE file if you plan to use the MIT License or another open-source license).*

## Contact

If you have any questions or suggestions, please contact:

*   [Your Name/Organization Name]
*   [Your Email Address]
*   [Link to your GitHub repository] (optional)
