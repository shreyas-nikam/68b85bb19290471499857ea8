id: 68b85bb19290471499857ea8_documentation
summary: Drafting AML Suspicious Activity Reports Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab Codelab: AI-Powered SAR Drafting Assistant

This codelab guides you through QuLab, an AI-powered tool designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). We'll explore its functionalities, focusing on how it automates the generation of first-draft SAR narratives, summarizes transaction timelines, and suggests potential typologies. Remember, this tool is designed to augment, not replace, human expertise.  Compliance, auditability, and human oversight remain paramount.

## Overview and Goals
Duration: 00:05

This application aims to significantly improve the efficiency of drafting SAR narratives, a crucial task for AML analysts. By leveraging Large Language Models (LLMs) and a structured workflow, QuLab streamlines the process while adhering to regulatory guidelines. This codelab will cover the following key concepts:

*   **AI-Assisted SAR Drafting:** Understanding how AI can automate the initial SAR narrative generation, focusing on compliance and accuracy.
*   **Key Information Extraction:**  Learning to identify and extract the "5Ws" (Who, What, When, Where, Why) from case data, which form the foundation of a strong SAR narrative.
*   **Human-in-the-Loop Approach:**  Emphasizing the importance of human review and compliance checks throughout the SAR drafting process.
*   **Compliance and Auditability:**  Implementing a compliance checklist and audit trail to ensure transparency and accountability.

## Setting up the Environment
Duration: 00:03

Before diving into the application, ensure you have the following prerequisites:

*   **Python 3.7+:** QuLab is built using Python.
*   **Streamlit:** Install Streamlit using `pip install streamlit`.
*   **Required Libraries:** The individual pages may have additional dependencies. Please install them using `pip install <library_name>`.
*   **Clone the Repository (If applicable):** If you have access to a repository containing the application, clone it to your local machine.

## Running the Application
Duration: 00:02

1.  Navigate to the directory containing the `app.py` file.
2.  Open your terminal and run the command: `streamlit run app.py`
3.  Streamlit will automatically open the application in your web browser. If it doesn't, you'll find the URL in the terminal output (usually `http://localhost:8501`).

## Case Intake
Duration: 00:05

The "Case Intake" page is where you'll input the initial information about the potential suspicious activity. This page will likely involve input fields for:

*   **Subject Information:** Details about the individual or entity under investigation (name, address, account number, etc.).
*   **Case Description:** A brief summary of the suspected activity.
*   **Supporting Documentation:**  Options to upload relevant documents (bank statements, transaction records, etc.).

This information serves as the foundation for the subsequent steps in the SAR drafting process.

## Explore Data
Duration: 00:10

This page provides tools to explore and analyze the data related to the case. Expect functionalities like:

*   **Data Visualization:** Charts and graphs to visualize transaction patterns, account activity, and other relevant data.
*   **Data Filtering and Sorting:** Tools to filter and sort transactions based on date, amount, type, etc.
*   **Timeline Generation:**  An automatically generated timeline of key events and transactions related to the suspicious activity.

This step is crucial for identifying patterns, anomalies, and red flags that will inform the SAR narrative.

## Draft SAR
Duration: 00:15

The heart of QuLab is the "Draft SAR" page, where the AI-powered SAR narrative generation takes place. This page likely uses a Large Language Model (LLM) to generate an initial draft narrative based on the information gathered in the previous steps.

Expect the following features:

1.  **5Ws Extraction:**
    *   The application will intelligently extract the 5Ws(Who, What, When, Where, Why) from the data available to the application.
    *   These 5Ws will be used to construct the SAR narrative.
2.  **AI-Generated Narrative:**
    *   The application will generate the SAR narrative from the extracted 5Ws.

Here's a conceptual architecture diagram:

```
++    ++    ++
|    Case Data       |    |    5Ws Extraction   |    |    LLM              |
| (Subject Info,     |>| (Who, What, When,   |>| (SAR Narrative      |
| Transactions, etc.)|    | Where, Why)         |    | Generation)         |
++    ++    ++
                                      |
                                      V
                         +-+
                         |    AI-Generated Narrative    |
                         +-+
```

**Important Considerations:**

*   **LLM Selection:** The specific LLM used (e.g., GPT-3, PaLM) will impact the quality and style of the generated narrative.
*   **Prompt Engineering:** The prompts used to guide the LLM are critical for ensuring the narrative is accurate, compliant, and focused.
*   **Customization:** Options to customize the AI-generated narrative (e.g., tone, level of detail) may be available.

<aside class="negative">
It's crucial to remember that the AI-generated narrative is a *draft*. It requires careful review and editing by a human analyst.
</aside>

## Review & Compare
Duration: 00:10

This page facilitates the review and comparison of the AI-generated narrative with the underlying data and relevant regulatory guidelines.

Expect features like:

*   **Side-by-Side Comparison:** Displaying the AI-generated narrative alongside the source data and key findings from the "Explore Data" page.
*   **Highlighting and Annotation:** Tools to highlight specific sections of the narrative and add annotations or comments.
*   **Version Control:**  Tracking changes made to the narrative over time.

This step ensures the accuracy, completeness, and compliance of the SAR narrative. It's where the "human-in-the-loop" approach is most critical.

## Compliance Checklist & Sign-off
Duration: 00:10

The "Compliance Checklist & Sign-off" page provides a structured checklist to ensure that the SAR narrative meets all relevant regulatory requirements.

The checklist might include items such as:

*   **Accuracy:** Verifying that all facts and figures are accurate and supported by the data.
*   **Completeness:** Ensuring that all relevant information is included in the narrative.
*   **Clarity:** Confirming that the narrative is clear, concise, and easy to understand.
*   **Compliance with FinCEN Guidance:**  Checking that the narrative adheres to FinCEN's guidance on SAR drafting.

Once the checklist is completed and all items are verified, a designated user (e.g., a compliance officer) can sign off on the SAR, indicating that it is ready for submission.

## Export & Audit
Duration: 00:05

The final step is to export the completed SAR narrative and generate an audit trail.

This page will provide options to:

*   **Export the SAR Narrative:** Export the final SAR narrative in a standard format (e.g., PDF, XML).
*   **Generate an Audit Trail:** Create a detailed audit trail documenting all steps taken in the SAR drafting process, including data sources, AI-generated drafts, human edits, and compliance checks.

The audit trail is essential for demonstrating compliance and providing accountability in case of regulatory scrutiny.

## Summary and Next Steps
Duration: 00:05

This codelab provided a comprehensive overview of QuLab, an AI-powered tool for assisting AML analysts in drafting SARs.  You learned how to use the application to automate the generation of first-draft narratives, extract key information, review and compare drafts, and ensure compliance.

Remember that AI is a powerful tool, but it should always be used in conjunction with human expertise and oversight. Continuous monitoring and validation are essential to ensure the accuracy, reliability, and compliance of AI-powered SAR drafting tools.
