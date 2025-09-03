
## Notebook Overview

This Jupyter Notebook demonstrates an AI-assisted Suspicious Activity Report (SAR) narrative generator for AML analysts. It covers the key stages of the SAR lifecycle, from case intake and data exploration to AI-powered drafting, review, compliance checks, and export.  The notebook highlights the importance of human oversight, auditability, and compliance in AI-assisted SAR drafting.

**Learning Goals:**

*   Understand how Generative AI can be leveraged to automate SAR drafting while adhering to regulatory guidelines.
*   Learn how to extract key information from case data to generate SAR narratives.
*   Explore the importance of human-in-the-loop review and compliance checks in AI-assisted SAR drafting.

## Code Requirements

**Libraries:**

*   pandas
*   numpy
*   matplotlib.pyplot
*   seaborn
*   sklearn (datasets, model selection, linear models, metrics)
*   nltk (natural language toolkit)
*   transformers (for LLM - a placeholder, as on-prem LLM is out of scope)
*   sentence-transformers (for embeddings - a placeholder for vector DB interactions)
*   plotly (express for interactive visualizations)

**Algorithms/Functions to be Implemented:**

*   `load_synthetic_data()`: Generates synthetic KYC, transaction, and alert data based on specified schemas.
*   `calculate_summary_kpis(transactions)`: Calculates key performance indicators for a case, such as total transactions, total amount, and time window.
*   `create_timeline_visualization(transactions)`: Creates an interactive timeline of transactions.
*   `create_geo_map_visualization(transactions)`: Generates a geo map showing transaction origins and destinations.
*   `create_counterparty_network_graph(transactions)`: Creates a network graph of counterparties.
*   `extract_5ws(case_data)`: Extracts the Who, What, When, Where, and Why from the case data.
*   `generate_ai_narrative(case_data, extracted_5ws, rag_corpus)`: Generates an AI-assisted SAR narrative based on the case data, extracted 5Ws, and retrieval-augmented generation from a local vector store (placeholder implementation).
*   `highlight_changes(ai_draft, analyst_edited)`: Highlights the differences between the AI-generated draft and the analyst-edited version.
*   `run_compliance_checklist(narrative, extracted_5ws)`: Performs a compliance checklist on the narrative.
*   `export_sar_data(narrative, facts, checklist_report, audit_trail)`: Exports the final narrative, facts, checklist report, and audit trail in JSON format.
*   `get_retrieved_guidance(vector_store, facts)`: Retrieves relevant guidance passages from a vector store based on the selected facts (placeholder implementation).

**Visualizations:**

*   Case summary KPIs (cards for #transactions, total in/out, #branches, #alerts, time window).
*   Interactive timeline of activity (event scatter or bars).
*   Geo map of branch locations and flows.
*   Counterparty network graph.
*   Side-by-side AI draft vs. analyst-edited final with inline highlights for insertions/deletions.
*   Checklist status widget with pass/fail indicators.

## Notebook Sections

1.  **Introduction**

    *   Markdown cell: Explains the purpose of the notebook and the overall SAR generation process. Introduces the learning goals.
    *   Code cell: Imports necessary libraries (pandas, numpy, matplotlib, seaborn, sklearn, nltk, transformers, sentence-transformers, plotly).
    *   Code cell: Sets a random seed for reproducibility using `numpy.random.seed(42)`.
    *   Markdown cell:  Explanation of the random seed that was set.
        Setting random seed helps reproduce the same output every time the code is executed.

2.  **Data Loading and Preparation**

    *   Markdown cell:  Explains the synthetic data generation process and the structure of the data. Mentions the schemas for customers, transactions, alerts, notes, and audit data.
    *   Code cell:  Defines the `load_synthetic_data()` function. This function generates synthetic data for customers, transactions, alerts, case notes, and related tables.
    *   Code cell: Executes the `load_synthetic_data()` function to create the dataframes: `customers`, `transactions`, `alerts`, and `notes`.
    *   Markdown cell:  Confirms the data loaded and its structure, specifying the number of rows and columns for each table loaded.

3.  **Case Intake and Summary KPIs**

    *   Markdown cell: Explains the case intake process and the importance of summarizing key information.
    *   Code cell: Defines the `calculate_summary_kpis(transactions)` function.
    *   Code cell: Executes the `calculate_summary_kpis()` function with the `transactions` dataframe and prints the KPIs (number of transactions, total amount, time window).
    *   Markdown cell: Explains the calculated KPIs and their significance in understanding the case.  For example, Total number of transactions $N_{transactions}$ can be used to check the amount of data to be inspected.

4.  **Data Exploration: Timeline Visualization**

    *   Markdown cell: Explains the importance of visualizing transaction timelines for identifying suspicious patterns.
    *   Code cell: Defines the `create_timeline_visualization(transactions)` function.
    *   Code cell: Executes the `create_timeline_visualization()` function with the `transactions` dataframe.
    *   Markdown cell:  Explains the insights gained from the timeline visualization, such as transaction frequency over time and potential clustering.

5.  **Data Exploration: Geo Map Visualization**

    *   Markdown cell: Explains the utility of visualizing transactions on a geo map for identifying suspicious geographic patterns.
    *   Code cell: Defines the `create_geo_map_visualization(transactions)` function.
    *   Code cell: Executes the `create_geo_map_visualization()` function with the `transactions` dataframe.
    *   Markdown cell: Explains the insights gained from the geo map visualization, such as identifying transactions to high-risk locations.

6.  **Data Exploration: Counterparty Network Graph**

    *   Markdown cell: Explains the purpose of creating a counterparty network graph to identify key players and relationships.
    *   Code cell: Defines the `create_counterparty_network_graph(transactions)` function.
    *   Code cell: Executes the `create_counterparty_network_graph()` function with the `transactions` dataframe.
    *   Markdown cell: Explains the insights gained from the network graph, such as identifying central nodes and suspicious connections.

7.  **Fact Snippet Selection (Simulated)**

    *   Markdown cell: Explains how analysts can select fact snippets from the visualizations to build a draft facts tray. Includes a note that this is a simulated step in this notebook.
    *   Code cell: Simulates fact snippet selection by manually creating a `selected_facts` dictionary or dataframe. This will contain a few relevant transactions, customer details, etc. For example:
        ```python
        selected_facts = {
            'customer_id': customers['customer_id'][0],
            'transaction_ids': transactions['txn_id'][:5].tolist()
        }
        ```
    *   Markdown cell: Prints the selected facts to confirm the simulation.  These are the facts that will drive the AI draft.

8.  **5W Extraction**

    *   Markdown cell: Explains the importance of extracting the Who, What, When, Where, and Why from the case data.
    *   Code cell: Defines the `extract_5ws(case_data)` function.
    *   Code cell: Executes the `extract_5ws()` function with the `selected_facts` data.
    *   Markdown cell: Prints the extracted 5Ws. Explains how these elements will be used to guide the AI narrative generation.

9.  **RAG Corpus Simulation**

    *   Markdown cell: Explains the concept of Retrieval Augmented Generation (RAG) and how FinCEN guidance is incorporated. Notes that a local vector store implementation is beyond the scope of the notebook and a simplified string-based retrieval is simulated.
    *   Code cell: Defines a placeholder for the RAG corpus as a dictionary of guidance snippets:
        ```python
        rag_corpus = {
            "guidance_1": "FinCEN recommends narratives to be clear, concise, and chronological.",
            "guidance_2": "Narratives should avoid speculation and focus on facts."
        }
        ```
    *   Code cell: Defines the function `get_retrieved_guidance(vector_store, facts)`. This function would normally interact with the vector store. In this simplified example, it returns a subset of the `rag_corpus` based on keywords in the `facts`.

10. **AI Narrative Generation**

    *   Markdown cell: Explains how the AI narrative is generated using a prompt template constrained to the selected facts and retrieved guidance.
    *   Code cell: Defines the `generate_ai_narrative(case_data, extracted_5ws, rag_corpus)` function. This function simulates the LLM by concatenating facts, 5Ws, and guidance in a template.  The function *must* include a disclaimer that the draft is "AI-assisted".
    *   Code cell: Executes the `generate_ai_narrative()` function with the case data, extracted 5Ws, and RAG corpus.
    *   Markdown cell: Prints the generated AI narrative. States clearly that this is a *simulated* AI-assisted draft.

11. **Review and Comparison (Simulated)**

    *   Markdown cell: Explains the review and comparison process and how analysts can edit the AI draft. Includes a note that this is a simulated step.
    *   Code cell: Simulates analyst edits by creating a modified version of the AI narrative (a simple string manipulation).
    *   Code cell: Defines the `highlight_changes(ai_draft, analyst_edited)` function.
    *   Code cell: Executes the `highlight_changes()` function to display the differences between the AI draft and the analyst-edited version.
    *   Markdown cell: Explains the highlighted changes and how they represent analyst input.  Points out how versioning would be handled in a real application (audit log).

12. **Compliance Checklist**

    *   Markdown cell: Explains the compliance checklist and its importance in ensuring regulatory compliance.
    *   Code cell: Defines the `run_compliance_checklist(narrative, extracted_5ws)` function.
    *   Code cell: Executes the `run_compliance_checklist()` function with the analyst-edited narrative and extracted 5Ws.
    *   Markdown cell: Prints the compliance checklist results (pass/fail indicators for each criterion).

13. **Export & Audit**

    *   Markdown cell: Explains the export and audit process, including the final narrative, facts, checklist report, and audit trail.
    *   Code cell: Defines the `export_sar_data(narrative, facts, checklist_report, audit_trail)` function.
    *   Code cell: Simulates the creation of an audit trail dictionary.
    *   Code cell: Executes the `export_sar_data()` function to export the data in JSON format (prints the JSON output to the console).
    *   Markdown cell: Explains the contents of the exported JSON data and how it can be used for regulatory reporting.

14. **Conclusion**

    *   Markdown cell: Summarizes the notebook's key takeaways and emphasizes the importance of human-in-the-loop AI for SAR generation. Reiterates the learning goals.

