id: 68b85bb19290471499857ea8_user_guide
summary: Drafting AML Suspicious Activity Reports User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AML SAR Drafting Assistant Codelab

This codelab guides you through using QuLab, an AI-driven application designed to assist Anti-Money Laundering (AML) analysts in drafting Suspicious Activity Reports (SARs). SARs are crucial documents financial institutions use to report suspicious activities to regulatory bodies like FinCEN. This application streamlines the SAR workflow by leveraging Large Language Models (LLMs) to generate first-draft narratives, summarize transaction timelines, and suggest typologies.  It's important to remember that the AI's output is a *draft* and requires thorough human review, auditability, and adherence to compliance guardrails.

The focus is on understanding how to use the application to effectively draft SARs, *not* on the underlying code. We'll explore how the application can help you extract key information, generate initial narratives, and ensure compliance. This codelab emphasizes the "human-in-the-loop" approach, where AI assists but humans retain control and responsibility.

## Case Intake
Duration: 00:05

The **Case Intake** page is where you begin your SAR drafting process. Here, you'll upload the data related to the suspicious activity you're investigating.  This could be in the form of a CSV or Excel file containing transaction details, customer information, alerts, and notes. If you don't have a file readily available, you can also load synthetic data for demonstration purposes.

<aside class="positive">
The application requires a structured dataset (like CSV or Excel) containing relevant transaction data. The more complete and accurate the data, the better the application can assist in drafting the SAR.
</aside>

1.  **Upload Case Bundle:** Use the file uploader to select a CSV or Excel file containing the case data.  The application will attempt to parse the data and display a preview.

2.  **Load Synthetic Data:** If you don't have a case file, click the "Load Synthetic Data" button. This will load a pre-populated dataset, allowing you to explore the application's features.

3.  **Review Data:**  The application will display a preview of the loaded data.  Take a moment to review the data to ensure it has been loaded correctly.

4.  **Summary KPIs:** The application calculates and displays key performance indicators (KPIs) based on the loaded transaction data, such as the total number of transactions, total transaction volume, and average transaction amount. This provides a quick overview of the case.

5.  **Possible Typologies:** Although implemented as a placeholder in this example, in a real-world scenario, the application would suggest possible typologies of suspicious activity based on the loaded data.

<aside class="negative">
Ensure that the uploaded data is properly formatted. Incorrectly formatted data may lead to errors during the KPI calculation and typology suggestion phases.
</aside>

## Explore Data
Duration: 00:03

The **Explore Data** page is intended to provide visualizations and tools for further analyzing the case data.
Currently this part of the application only has placeholder code. In a real world application, you would create timeline visualizations of transactions using libraries like Plotly to identify patterns and trends. These visualizations would help you understand the sequence of events and identify potential anomalies.

## Draft SAR
Duration: 00:10

The **Draft SAR** page is where the AI assistant comes into play. This page uses the loaded case data to generate a first-draft SAR narrative. The application extracts key information (the 5Ws: Who, What, When, Where, Why) and uses it to build a prompt for the LLM.

1.  **Automatic 5Ws Extraction (Placeholder):**  Currently, the application uses a placeholder for extracting the 5Ws.  In a real-world application, this step would involve analyzing the case data to automatically identify the key information needed for the SAR narrative (e.g., the subject of the suspicious activity, the nature of the suspicious activity, the timing of the activity, the location of the activity, and the reason for suspicion).

2.  **AI Narrative Generation:** The application uses the extracted 5Ws (or placeholder values) to build a prompt and calls the LLM to generate a draft narrative.

3.  **Review AI-Generated Narrative:** The generated narrative is displayed in a text area. **Critically review the narrative for accuracy, clarity, and completeness.** Remember, this is a *draft* and will likely require editing and refinement.

4.  **Human-in-the-Loop Editing:**  Edit the AI-generated narrative to correct any errors, add additional details, and ensure it meets all regulatory requirements and internal policies.

<aside class="positive">
Pay close attention to the AI-generated narrative. Look for inconsistencies, missing information, or areas where the AI's interpretation of the data may be inaccurate.
</aside>

<aside class="negative">
Never blindly trust the AI-generated narrative. Always perform thorough human review and validation to ensure accuracy and compliance.
</aside>

## Review & Compare
Duration: 00:05

The **Review & Compare** page (currently a placeholder) is designed to help you compare different versions of the SAR narrative. This can be useful for tracking changes made during the editing process and for comparing the original AI-generated narrative with the final, analyst-edited version.

In a real-world implementation, this page would:

1.  **Store Narrative Versions:** Automatically save different versions of the narrative as they are edited.
2.  **Side-by-Side Comparison:** Allow you to compare two versions of the narrative side-by-side, highlighting the differences between them.
3.  **Track Changes:**  Provide a visual representation of the changes made to the narrative over time.

## Compliance Checklist & Sign-off
Duration: 00:05

The **Compliance Checklist & Sign-off** page is a critical step in the SAR drafting process.  This page provides a checklist of items to review to ensure that the SAR meets all regulatory requirements and internal policies.

1.  **Compliance Checklist:** The application displays a checklist of items to review. This might include items such as:
    *   Ensuring all required fields are completed.
    *   Verifying the accuracy of all information.
    *   Confirming that the narrative is clear, concise, and factual.
    *   Documenting any discrepancies or red flags.

2.  **Analyst Sign-off:**  After completing the checklist, the analyst signs off on the SAR, certifying that it meets all compliance requirements.

3.  **Supervisor Review (Optional):** In some cases, a supervisor may be required to review and approve the SAR before it is submitted.

<aside class="negative">
The compliance checklist is essential for ensuring that the SAR is accurate, complete, and compliant with all applicable regulations.  Do not skip this step!
</aside>

## Export & Audit
Duration: 00:02

The **Export & Audit** page allows you to export the final SAR and generate an audit trail of the drafting process.

1.  **Export SAR:** The application allows you to export the SAR in a standard format (e.g., PDF, XML).

2.  **Generate Audit Trail:** The application generates an audit trail of the SAR drafting process, including:
    *   The date and time the SAR was created.
    *   The user who created the SAR.
    *   All changes made to the SAR narrative.
    *   The date and time the SAR was signed off.
    *   The user who signed off on the SAR.

3.  **Store Audit Trail:** The audit trail is stored securely for future reference.

<aside class="positive">
The audit trail provides a valuable record of the SAR drafting process, which can be useful for demonstrating compliance and responding to regulatory inquiries.
</aside>
