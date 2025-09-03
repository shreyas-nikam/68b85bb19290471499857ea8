id: 68b85bb19290471499857ea8_user_guide
summary: Drafting AML Suspicious Activity Reports User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AML SAR Drafting Assistant - Codelab User Guide

This codelab provides a comprehensive guide to using the QuLab AML SAR Drafting Assistant, a Streamlit application designed to streamline the creation of Suspicious Activity Reports (SARs). This tool enhances the efficiency and accuracy of AML analysts by providing intelligent assistance throughout the SAR generation process. The application's primary goal is to help analysts automate first-draft SAR narratives while maintaining human oversight and ensuring compliance.

## Understanding the Application's Importance

Duration: 00:05

SARs are critical for financial institutions to report suspicious activities to regulatory bodies. Drafting these reports is often time-consuming and requires meticulous attention to detail. The QuLab AML SAR Drafting Assistant aims to reduce the manual effort involved, improve the quality of SAR narratives, and ensure adherence to regulatory guidelines. By using this application, analysts can focus on critical thinking and decision-making, leaving the initial drafting and data processing to the AI-powered assistant. The application provides a structured approach that ensures AI assists in drafting, while human oversight and compliance remain central to the process.

## Navigating the Application

Duration: 00:02

The application features a sidebar for navigation, allowing you to access different sections of the SAR drafting process. These sections include:

*   **Case Intake**: Upload and get a preliminary overview of the case data.
*   **Explore Data**: Interactively analyze transactions, customer relationships, and geographic patterns using advanced visualizations.
*   **Draft SAR**: Generate an initial SAR narrative using an LLM, steered by extracted key facts.
*   **Review & Compare**: Review, edit, and compare the AI-generated draft with the final version.
*   **Compliance Checklist & Sign-off**: Validate the narrative against a compliance checklist and facilitate formal sign-off.
*   **Export & Audit**: Export the final SAR package, including the narrative, facts, checklist report, and a detailed audit trail.

Use the selectbox under the "Navigation" label in the sidebar to switch between pages.

## Case Intake

Duration: 00:10

The **Case Intake** page is the starting point for the SAR drafting process. Here, you can either upload your own case data or use the pre-loaded synthetic data provided by the application. The application provides an initial overview of the case, highlighting key statistics and potential AML typologies.

**Key Features:**

*   **Data Loading:** The application loads synthetic data for demonstration purposes. This data includes customer information, transaction details, alerts, and analyst notes.

*   **Data Overview:** The page displays the shapes of the loaded dataframes (Customers, Transactions, Alerts, Notes), giving you a quick understanding of the data volume.

*   **Quick Stats:** Key performance indicators (KPIs) such as total transactions, total transaction volume, average transaction amount, time window of transactions, number of unique customers, and total alerts are displayed. These KPIs provide a snapshot of the case.

*   **Possible Typologies:** The application analyzes alert data to suggest possible AML typologies. This helps analysts focus their investigation on relevant areas.

*   **Raw Data Preview:** The page displays the first few rows of each dataframe, allowing you to preview the data and verify its integrity.

**Important Considerations:**

*   The synthetic data is for demonstration purposes only. When using the application for real-world cases, you will need to upload your own data.
*   The possible typologies suggested by the application are based on simple heuristics. Analysts should use their own judgment and expertise to determine the actual typologies involved in the case.

## Explore Data

Duration: 00:15

The **Explore Data** page provides interactive visualizations to help you analyze the case data in more detail. This page allows you to identify patterns, trends, and anomalies that may indicate suspicious activity.

**Key Visualizations:**

*   **Transaction Timeline:** This visualization displays transaction amounts over time, allowing you to identify periods of unusual activity.
*   **Geographic Map:** This map visualizes the origins of transactions, highlighting geographic patterns that may be indicative of money laundering or other illicit activities. The size of the markers on the map corresponds to the transaction amount, making it easy to identify high-value transactions.
*   **Counterparty Network Graph:** This graph visualizes the relationships between customers involved in transactions. This helps you identify networks of individuals who may be collaborating to commit financial crimes.

**Using the Visualizations:**

*   Interact with the visualizations by hovering over data points to see more details.
*   Use the zoom and pan features to explore specific areas of the visualizations.
*   Use the filters and selection tools to focus on specific subsets of the data.

**Mathematical Considerations:**

The transaction timeline plots the transaction amount against time. The geographic map uses latitude and longitude coordinates to plot the origin of transactions. The size of the markers is scaled proportionally to the transaction amount.

## Draft SAR

Duration: 00:15

The **Draft SAR** page allows you to generate an initial SAR narrative using a Large Language Model (LLM). The application guides you through the process of extracting key information from the case data, which is then used to steer the LLM in generating a focused and compliant narrative.

**Key Steps:**

1.  **Key Information Extraction (The 5Ws):** Identify the **Who, What, When, Where, and Why** of the suspicious activity. This involves analyzing the case data and summarizing the key facts.
2.  **LLM Narrative Generation:** Use the extracted key information to generate an initial SAR narrative using the LLM.
3.  **Review and Edit:** Review the generated narrative and make any necessary edits to ensure accuracy, completeness, and compliance.

**Important Considerations:**

*   The quality of the generated narrative depends on the quality of the extracted key information. Take the time to carefully analyze the case data and identify the most important facts.
*   The LLM-generated narrative should be considered a draft. It is essential to review and edit the narrative to ensure accuracy, compliance, and clarity.
*   The application is designed to assist in drafting, but human oversight and compliance remain central to the process.

## Review & Compare

Duration: 00:10

The **Review & Compare** page allows you to review the LLM-generated draft against your final version of the SAR narrative. This page provides tools to compare the two versions side-by-side, making it easy to identify changes and ensure that all key information has been included.

**Key Features:**

*   **Side-by-Side Comparison:** The page displays the LLM-generated draft and your final version of the SAR narrative side-by-side.
*   **Highlighting Changes:** The application highlights the differences between the two versions, making it easy to identify changes.
*   **Editing Tools:** You can edit your final version of the SAR narrative directly on the page.

**Using the Review & Compare Page:**

1.  Carefully review the LLM-generated draft and your final version of the SAR narrative.
2.  Pay close attention to the highlighted changes, and ensure that all key information has been included in the final version.
3.  Use the editing tools to make any necessary changes to your final version of the SAR narrative.

## Compliance Checklist & Sign-off

Duration: 00:10

The **Compliance Checklist & Sign-off** page provides a compliance checklist to validate the narrative against regulatory requirements and facilitates formal sign-off. This ensures that the SAR meets all necessary standards before submission.

**Key Features:**

*   **Compliance Checklist:** A list of compliance requirements that must be met before the SAR can be submitted.
*   **Sign-off Mechanism:** A formal sign-off process to ensure that the SAR has been reviewed and approved by the appropriate personnel.

**Using the Compliance Checklist & Sign-off Page:**

1.  Review the compliance checklist and verify that the SAR meets all requirements.
2.  Address any compliance issues that are identified.
3.  Complete the sign-off process to formally approve the SAR.

## Export & Audit

Duration: 00:05

The **Export & Audit** page allows you to export the final SAR package, including the narrative, facts, checklist report, and a detailed audit trail. This ensures that every step of the SAR drafting process is auditable, transparent, and aligned with compliance requirements.

**Key Features:**

*   **Export SAR Package:** Export the final SAR package in a format suitable for submission to regulatory bodies.
*   **Generate Audit Trail:** Generate a detailed audit trail of the SAR drafting process, including versioning, audit logging, and sign-off mechanisms.

**Using the Export & Audit Page:**

1.  Export the final SAR package.
2.  Generate the audit trail and store it securely for future reference.
