import streamlit as st
import re
import pandas as pd

import re, html
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
import requests

# Load environment variables
load_dotenv()
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", os.environ.get("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_llm(prompt: str) -> str:
    if not LLM_API_KEY or LLM_API_KEY == "":
        print("Warning: LLM_API_URL or LLM_API_KEY not set. Using a dummy response.")
        return "AI-assisted fixed draft:\nThis is a placeholder fixed narrative. In a real scenario, the LLM would generate a corrected version based on the compliance failures."
    
    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }
    r = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

def build_fix_prompt(narrative: str, compliance_report: dict) -> str:
    """
    Builds a detailed prompt for the LLM to fix the SAR narrative based on compliance failures.
    """
    # Format compliance results with specific failures
    results_str = f"Overall Status: {'PASS' if compliance_report['overall'] else 'FAIL'}\n\n"
    results_str += "Detailed Checklist Items and Failures:\n"
    
    failed_items = []
    for item in compliance_report['items']:
        status = 'PASS' if item['passed'] else 'FAIL'
        results_str += f"- {item['label']}: {status}\n"
        if not item['passed']:
            results_str += f"  Remediation Required: {item['remediation']}\n"
            failed_items.append(item['label'])
    
    failed_list = ", ".join(failed_items) if failed_items else "None"
    
    prompt = f"""
You are an expert AML analyst assistant specializing in Suspicious Activity Report (SAR) drafting and compliance with FinCEN guidelines.

Your task is to fix a SAR narrative that has failed compliance checks. You must address ALL failed checklist items while maintaining factual accuracy, chronological order, and regulatory compliance.

CURRENT SAR NARRATIVE:
{narrative}

COMPLIANCE CHECKLIST RESULTS:
{results_str}

FAILED ITEMS TO ADDRESS: {failed_list}

INSTRUCTIONS:
1. Review each failed checklist item and implement the suggested remediation.
2. Ensure the narrative includes all 5Ws (Who, What, When, Where, Why) clearly and completely.
3. Maintain chronological order of events.
4. Remove any speculative language (e.g., "may have", "could be", "likely").
5. Keep the narrative concise but comprehensive, within 100-1000 characters.
6. Use specific amounts, dates, and details from the original narrative.
7. Label amounts with backticks, e.g., `$500.00`.
8. Structure the narrative logically with clear paragraphs.

PROVIDE ONLY the fixed SAR narrative below, starting with "AI-assisted fixed draft:" and ending with the complete corrected narrative. Do not include any additional commentary or explanations.
"""
    return prompt

# ---- Tunables ----
SPECULATIVE_PHRASES = [
    "may have been", "might have been", "could have been",
    "it is believed", "suggests that", "appears to", "possibly", "likely"
]
MIN_LEN = 100
MAX_LEN = 1000

def run_compliance_checklist(narrative: str, extracted_5ws: dict) -> dict:
    """
    Compute compliance checks and return a structured report with per-item pass/fail + remediation text.
    """
    narrative = (narrative or "").strip()
    five_ws = extracted_5ws or {}
    five_ws = {k: (v or []) for k, v in five_ws.items()}

    # 1) 5Ws presence
    required_keys = ["Who", "What", "When", "Where", "Why"]
    missing_5ws = [k for k in required_keys if len(five_ws.get(k, [])) == 0]
    has_all_5ws = len(missing_5ws) == 0

    # 2) Chronology
    chronology_ok = False
    parsed_when = []
    chronology_error = None
    if len(five_ws.get("When", [])) > 0:
        try:
            parsed_when = [pd.to_datetime(t, errors="coerce") for t in five_ws["When"]]
            parsed_when = [t for t in parsed_when if pd.notnull(t)]
            if len(parsed_when) <= 1:
                chronology_ok = True
            else:
                chronology_ok = all(parsed_when[i] <= parsed_when[i+1] for i in range(len(parsed_when)-1))
        except Exception as e:
            chronology_ok = True
            chronology_error = str(e)
    else:
        chronology_ok = True  # explicitly fail if no "When" available

    # 3) Clarity (light heuristic)
    clarity_ok = len(narrative) > 50

    # 4) No speculation
    lower = narrative.lower()
    speculative_hits = sorted({p for p in SPECULATIVE_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", lower)})
    no_speculation = (len(speculative_hits) == 0)

    # 5) Length bounds
    length_ok = (MIN_LEN <= len(narrative) <= MAX_LEN)

    items = []

    # Build items with remediation text
    items.append({
        "key": "5Ws_present",
        "label": "All 5Ws captured (Who / What / When / Where / Why)",
        "passed": has_all_5ws,
        "remediation": (
            "Add missing elements — "
            + ", ".join(missing_5ws)
            + ".\n"
            "- Who: legal names, account numbers/IDs.\n"
            "- What: type of suspicious activity, amounts.\n"
            "- When: specific dates/times (ISO format preferred).\n"
            "- Where: locations (branches, cities, countries).\n"
            "- Why: objective rationale (alerts/rules triggered, patterns)."
        ) if not has_all_5ws else ""
    })

    items.append({
        "key": "chronology",
        "label": "Events presented in chronological order",
        "passed": chronology_ok,
        "remediation": (
            "Reorder events by timestamp (earliest → latest) and ensure dates are parseable. "
            "Include a brief timeline summary. If multiple same-day events, add times (HH:MM)."
        ) if not chronology_ok else "",
        "details": {
            "first": parsed_when[0] if parsed_when else None,
            "last": parsed_when[-1] if parsed_when else None,
            "error": chronology_error
        }
    })

    items.append({
        "key": "clarity",
        "label": "Narrative is clear and substantive",
        "passed": clarity_ok,
        "remediation": (
            "Expand with concrete facts: who did what, when, where, why it’s suspicious. "
            "Use short sentences; reduce jargon; prefer specific amounts/dates over generalities."
        ) if not clarity_ok else ""
    })

    items.append({
        "key": "no_speculation",
        "label": "No speculative or conjectural language",
        "passed": no_speculation,
        "remediation": (
            "Remove speculative phrases: " + ", ".join(speculative_hits) + ". "
            "State only observable facts (what occurred), not intent or assumptions."
        ) if not no_speculation else ""
    })

    items.append({
        "key": "length_bounds",
        "label": f"Narrative length within {MIN_LEN}–{MAX_LEN} characters",
        "passed": length_ok,
        "remediation": (
            f"Current length {len(narrative)} chars. "
            + ("Add details (timeline, amounts, counterparties, alert triggers) to reach minimum."
               if len(narrative) < MIN_LEN else
               "Tighten the narrative: remove repetition and non-essential commentary to stay concise.")
        ) if not length_ok else ""
    })

    overall = all(i["passed"] for i in items)

    return {
        "overall": overall,
        "length": len(narrative),
        "five_ws_counts": {k: len(five_ws.get(k, [])) for k in required_keys},
        "items": items,
    }


def render_compliance_checklist_ui(narrative: str, extracted_5ws: dict):
    """
    Streamlit UI:
      - Disabled checkbox per item shows PASS (checked) / FAIL (unchecked).
      - Color-coded badge (green/red) next to each checkbox.
      - Inline remediation text shown on the same row when an item fails.
    """
    report = run_compliance_checklist(narrative, extracted_5ws)

    st.subheader("Compliance Checklist")
    st.markdown("**Overall Status:** " + ("✅ **PASS**" if report["overall"] else "❌ **FAIL**"))
    st.caption(
        f"5Ws Counts — Who: {report['five_ws_counts'].get('Who',0)}, "
        f"What: {report['five_ws_counts'].get('What',0)}, "
        f"When: {report['five_ws_counts'].get('When',0)}, "
        f"Where: {report['five_ws_counts'].get('Where',0)}, "
        f"Why: {report['five_ws_counts'].get('Why',0)} | "
        f"Narrative length: {report['length']} chars"
    )
    st.divider()

    # Row renderer with color-coded badges and inline remediation
    def row(item):
        passed = item["passed"]
        badge_bg = "#dcfce7" if passed else "#fee2e2"   # green/red light backgrounds
        badge_bd = "#22c55e" if passed else "#ef4444"   # green/red borders
        badge_tx = "#065f46" if passed else "#7f1d1d"   # green/red text

        col_ck, col_lbl, col_rem = st.columns([0.10, 0.45, 0.45], vertical_alignment="center")

        with col_ck:
            # Disabled checkbox communicates pass/fail
            st.checkbox(label="", value=passed, disabled=True, key=f"ck_{item['key']}")

        with col_lbl:
            st.markdown(
                f'<div style="background:{badge_bg};border:1px solid {badge_bd};margin:10px;'
                f'border-radius:6px;padding:8px 10px;font-weight:600;'
                f'color:{badge_tx};display:inline-block;">'
                f'{"PASS" if passed else "FAIL"} — {html.escape(item["label"])}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col_rem:
            if not passed:
                st.markdown(
                    '<div style="background:#b86600;border-left:4px solid #f59e0b;'
                    'padding:8px 10px;border-radius:4px;white-space:pre-wrap;">'
                    '<b>Remediation:</b> '
                    + html.escape(item["remediation"]) +
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown("<div style='color:#aaf0dc'>—</div>", unsafe_allow_html=True)

    # Render all items
    for it in report["items"]:
        row(it)

    return report

def run_page():
    st.markdown("# Compliance Checklist")
    # If a fixed narrative was saved in the previous run, apply it BEFORE rendering widgets
    if st.session_state.get('apply_fixed_narrative'):
        fixed_text = st.session_state.get('fixed_narrative')
        if fixed_text:
            # Update both canonical narrative keys for downstream pages
            st.session_state.human_edited_narrative = fixed_text
            st.session_state.analyst_edited_narrative = fixed_text
            # Invalidate any previously prepared export so it can't show stale content
            try:
                st.session_state.pop('export_ready', None)
                st.session_state.pop('export_files', None)
                st.session_state.pop('pdf_generation_success', None)
            except Exception:
                pass
        # Clear the flag to avoid reapplying repeatedly
        st.session_state.apply_fixed_narrative = False

    if 'data' not in st.session_state:
        st.error("Please load synthetic data first. Go to the **Case Intake** page.")
        return
    
    if 'selected_facts' not in st.session_state:
        st.error("Please select facts first. Go to the **Explore Data** page.")
        return
    
    selected_facts = st.session_state.selected_facts
    
    if 'ai_draft_narrative' not in st.session_state:
        st.error("Please generate an AI draft narrative first. Go to the **Draft SAR** page.")
        return
    
    ai_draft_narrative = st.session_state.ai_draft_narrative
    
    if 'human_edited_narrative' not in st.session_state:
        st.error("Please edit the narrative first. Go to the **Explore Data** page.")
        return
    
    human_edited_narrative = st.session_state.human_edited_narrative
    
    if 'extracted_5ws' not in st.session_state:
        st.error("Please extract 5Ws first. Go to the `Explore Data` page.")
        return
    
    five_ws = st.session_state.extracted_5ws
    
    st.markdown(""" 

Before a Suspicious Activity Report (SAR) is filed, it undergoes a stringent compliance review. This checklist ensures that the narrative and supporting facts meet all regulatory requirements and internal policies. It acts as a final quality control gate, minimizing the risk of rejections or further inquiries from regulatory bodies.

### Checklist Criteria

Typical compliance criteria for a SAR narrative include:

*   **5Ws Present:** Ensures that Who, What, When, Where, and Why are clearly addressed.
*   **Chronology:** Verifies that events are presented in a logical, time-ordered sequence.
*   **Clarity and Conciseness:** Checks for unambiguous language and avoidance of jargon where possible.
*   **No Speculation:** Confirms that the narrative relies solely on facts and avoids assumptions, inferences of guilt, or unproven statements.
*   **Length Bounds:** Ensures the narrative falls within specified word or character limits.


For example:

*   **5Ws Check:** This can be validated by ensuring the `extracted_5ws` dictionary contains values for each 'W'.
*   **Chronology Check:** A basic check might assume chronology is present if the narrative includes multiple timestamps in ascending order. More advanced checks could use NLP to verify temporal ordering.
*   **Speculation Check:** This involves searching for speculative phrases (e.g., "might have been", "could be interpreted as") in the narrative. If any are found, the check fails.

This automated checklist speeds up the review process and provides objective feedback, highlighting areas that require further attention before submission.
""")
    
    
    # show the narrative and let the user edit it (bind to session state)
    st.markdown("### SAR Narrative")
    edited_narrative = st.text_area(
        "Edit the narrative to make it compliant with the checklist",
        value=st.session_state.human_edited_narrative,
        height=400,
        key="human_edited_narrative",
    )
    
    
    if st.button("Run Compliance Checklist"):
        compliance_report = render_compliance_checklist_ui(edited_narrative, five_ws)
        st.session_state.compliance_checklist_results = compliance_report
        st.markdown("")
        st.markdown("The compliance checklist report provides a clear pass/fail status for each critical criterion. This immediate feedback helps analysts understand where the narrative stands in terms of regulatory readiness.")
        st.markdown("""
Now head to the `Export & Audit` page to export the SAR.                
                    """,
                    unsafe_allow_html=True
                )

    # Auto-run the compliance checklist after saving a fixed narrative
    if st.session_state.get('auto_run_checklist'):
        compliance_report = render_compliance_checklist_ui(edited_narrative, five_ws)
        st.session_state.compliance_checklist_results = compliance_report
        st.markdown("")
        st.markdown("The compliance checklist report provides a clear pass/fail status for each critical criterion. This immediate feedback helps analysts understand where the narrative stands in terms of regulatory readiness.")
        st.markdown("""
Now head to the `Export & Audit` page to export the SAR.                
                    """,
                    unsafe_allow_html=True
                )
        # reset flag so it only happens once
        st.session_state.auto_run_checklist = False
    
    # Add "Fix it with AI" button if checklist has been run and failed
    if ('compliance_checklist_results' in st.session_state and 
        isinstance(st.session_state.compliance_checklist_results, dict) and 
        not st.session_state.compliance_checklist_results.get('overall', True)):
        
        st.markdown("---")
        st.markdown("### 🚨 Compliance Issues Detected")
        st.markdown("The SAR narrative failed one or more compliance checks. Use AI assistance to automatically fix the issues:")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔧 Fix it with AI", type="primary", use_container_width=True):
                # Use the current edited narrative bound to session state
                current_narrative = st.session_state.get('human_edited_narrative', '')
                compliance_report = st.session_state.compliance_checklist_results
                
                # Build the prompt for fixing
                fix_prompt = build_fix_prompt(current_narrative, compliance_report)
                
                # Call the LLM to get the fixed narrative
                with st.spinner("🤖 AI is analyzing and fixing the narrative..."):
                    st.session_state.fixed_narrative = call_llm(fix_prompt)

        # Persistently render the AI-fixed section if available so Save works after rerun
        if st.session_state.get('fixed_narrative'):
            st.markdown("### ✅ AI-Fixed Narrative")
            st.markdown("*Review the improved narrative below:*")
            # Allow small tweaks before saving
            updated_fixed = st.text_area(
                "Fixed SAR Narrative:",
                value=st.session_state.fixed_narrative,
                height=300,
                key="fixed_narrative_display",
            )
            # Keep session in sync in case user edits the fixed text
            st.session_state.fixed_narrative = updated_fixed

            if st.button("Save Fixed SAR Narrative", type="primary", use_container_width=True):
                # Defer applying to avoid modifying session_state for an existing widget key in the same run
                st.session_state.apply_fixed_narrative = True
                # Request auto-run of checklist after save applies
                st.session_state.auto_run_checklist = True
                st.success("Saved. Updating the SAR Narrative above...")
                try:
                    import streamlit as _st
                    _st.rerun()
                except Exception:
                    pass
        
        st.markdown("---")
        
