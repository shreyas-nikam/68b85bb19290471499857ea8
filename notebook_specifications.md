# Notebook Overview

This Jupyter Notebook demonstrates an AI-assisted Suspicious Activity Report (SAR) **narrative generator** for AML analysts—covering case intake, data exploration, LLM-powered drafting, review, compliance checks, and export. Human oversight, auditability, and compliance remain central.

**Learning Goals**

* See how a **direct LLM call** can automate first-draft SAR narratives while following regulatory guidance (no RAG).
* Learn to **extract key information** (5Ws) from case data to steer the narrative.
* Practice **human-in-the-loop** review and compliance checks before export.

---

# Code Requirements

## Libraries

* `pandas`
* `numpy`
* `matplotlib.pyplot`
* `seaborn`
* `sklearn` (datasets, model selection, linear models, metrics)
* `nltk`
* `plotly` (e.g., `plotly.express`)
* **NEW (replace RAG/transformers deps):**

  * `requests` (HTTP call to your LLM endpoint)
  * `tenacity` (optional, for retry logic)
  * `python-dotenv` (optional, for loading `LLM_API_KEY` from `.env`)

> **Removed:** `transformers`, `sentence-transformers`.

## Algorithms / Functions to Implement

* `load_synthetic_data()`: Generate synthetic KYC, transaction, alert, and notes data.
* `calculate_summary_kpis(transactions)`
* `create_timeline_visualization(transactions)`
* `create_geo_map_visualization(transactions)`
* `create_counterparty_network_graph(transactions)`
* `extract_5ws(case_data)`
* **NEW (replaces RAG-based generation):**

  * `build_prompt(case_data, extracted_5ws)`: Compose a compliant, chronological, 5W-driven prompt.
  * `call_llm(prompt)`: Make an HTTP request to your chosen LLM endpoint (e.g., private gateway); return model text.
  * `generate_ai_narrative(case_data, extracted_5ws)`: Uses `build_prompt` → `call_llm`; guarantees “AI-assisted” disclaimer.
* `highlight_changes(ai_draft, analyst_edited)`
* `run_compliance_checklist(narrative, extracted_5ws)`
* `export_sar_data(narrative, facts, checklist_report, audit_trail)`

> **Removed functions:** `get_retrieved_guidance(...)` and any vector-store / retrieval helpers.
> **Changed signature:** `generate_ai_narrative(...)` no longer accepts `rag_corpus`.

**Minimal, provider-agnostic LLM call (reference snippet)**

```python
import os, requests
from tenacity import retry, stop_after_attempt, wait_exponential

LLM_API_URL = os.getenv("LLM_API_URL")      # e.g., https://llm.internal/v1/chat/completions
LLM_API_KEY = os.getenv("LLM_API_KEY")      # stored securely

def build_prompt(case_data, extracted_5ws):
    # Compose a chronological, fact-focused, speculative-free prompt.
    return f"""
You are assisting an AML analyst to draft a SAR narrative.
Follow FinCEN guidance: be clear, concise, chronological; avoid speculation.
Include Who/What/When/Where/Why and key facts only.
Label the output as 'AI-assisted draft'.

5Ws:
{extracted_5ws}

Facts:
{case_data}

Produce a single narrative paragraph set appropriate for a SAR filing.
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_llm(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "your-model-name",   # configure per your provider
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 600
    }
    r = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    # Adjust the path below to your provider’s response schema:
    return data["choices"][0]["message"]["content"].strip()

def generate_ai_narrative(case_data, extracted_5ws) -> str:
    prompt = build_prompt(case_data, extracted_5ws)
    narrative = call_llm(prompt)
    if "AI-assisted" not in narrative:
        narrative = "AI-assisted draft:\n" + narrative
    return narrative
```

---

# Visualizations (unchanged)

* Case summary KPI cards
* Interactive timeline (events per day/hour)
* Geo map (origins/destinations/flows)
* Counterparty network graph
* Side-by-side diff (AI draft vs analyst final)
* Checklist status widget (pass/fail)

---

# Updated Notebook Sections

1. **Introduction**

* **Markdown:** Purpose + learning goals (direct LLM, no RAG).
* **Code:** Import libraries (remove `transformers` / `sentence-transformers`; add `requests`, optional `tenacity`, `dotenv`).
* **Code:** `numpy.random.seed(42)`.
* **Markdown:** Why seeding matters.

2. **Data Loading and Preparation**

* **Markdown:** Synthetic data generation and schemas (customers, transactions, alerts, notes, audit).
* **Code:** `load_synthetic_data()` definition.
* **Code:** Execute loader → `customers`, `transactions`, `alerts`, `notes`.
* **Markdown:** Shapes / row counts confirmation.

3. **Case Intake and Summary KPIs**

* **Markdown:** Why summarize early.
* **Code:** `calculate_summary_kpis(transactions)` + print KPIs.
* **Markdown:** Interpret KPIs.

4. **Data Exploration: Timeline Visualization**

* **Markdown:** Timeline value.
* **Code:** `create_timeline_visualization(transactions)` + show.
* **Markdown:** Findings (frequency, bursts).

5. **Data Exploration: Geo Map Visualization**

* **Markdown:** Geographic risk cues.
* **Code:** `create_geo_map_visualization(transactions)` + show.
* **Markdown:** Findings (risky geos, clusters).

6. **Data Exploration: Counterparty Network Graph**

* **Markdown:** Relationships & hubs.
* **Code:** `create_counterparty_network_graph(transactions)` + show.
* **Markdown:** Findings (central nodes, anomalies).

7. **Fact Snippet Selection (Simulated)**

* **Markdown:** How analysts curate facts.
* **Code:** Build `selected_facts` (IDs, rows) to simulate a facts tray.
* **Markdown:** Confirm selected facts.

8. **5W Extraction**

* **Markdown:** Importance of 5Ws.
* **Code:** `extract_5ws(selected_facts)` + print.
* **Markdown:** How 5Ws guide the LLM draft.

9. **AI Narrative Generation (Direct LLM Call)**

* **Markdown:** Explain **no RAG**; narrative is generated from **selected facts + 5Ws** only. Note governance: low temperature, deterministic runs, explicit “AI-assisted” label.
* **Code:** `build_prompt(...)`, `call_llm(...)`, `generate_ai_narrative(...)` (as above).
* **Code:** Run `generate_ai_narrative(selected_facts, five_ws)`.
* **Markdown:** Show the narrative; reiterate that it’s an AI-assisted draft requiring human review.

10. **Review and Comparison (Simulated)**

* **Markdown:** Human edits + rationale.
* **Code:** Simulate edited narrative (simple tweaks).
* **Code:** `highlight_changes(ai_draft, analyst_edited)` to visualize diffs.
* **Markdown:** Explain edits & audit implications.

11. **Compliance Checklist**

* **Markdown:** Checklist criteria (5Ws present, chronology, clarity, no speculation, length bounds).
* **Code:** `run_compliance_checklist(analyst_edited, five_ws)` → pass/fail items.
* **Markdown:** Interpret results and remediation.

12. **Export & Audit**

* **Markdown:** Export bundle contents and regulatory utility.
* **Code:** `export_sar_data(narrative, facts, checklist_report, audit_trail)`; simulate `audit_trail`.
* **Code:** Print/serialize JSON output.
* **Markdown:** What’s in the JSON and why it matters.

13. **Conclusion**

* **Markdown:** Key takeaways; emphasize human-in-the-loop and controls with **direct LLM** (no retrieval).

---

# Additional Implementation Notes

* **Security/Privacy:** Only send **strictly necessary** structured facts to the LLM; consider redaction; prefer a **private LLM endpoint**.
* **Determinism:** Use `temperature≈0–0.3`; log prompts and responses (hash PII as needed).
* **Governance:** Persist prompt, model, parameters, and outputs to the audit log; tag drafts as **AI-assisted** until sign-off.
* **Fallbacks:** If `call_llm` fails, surface a clear error and keep the analyst in control (no silent failures).
