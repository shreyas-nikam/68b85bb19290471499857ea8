import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta


def export_sar_data(narrative, facts, checklist_report, audit_trail):
    """Exports SAR data to a structured format (dict)."""
    if not isinstance(narrative, str):
        raise AttributeError("Narrative must be a string")
    if not isinstance(facts, list):
        raise AttributeError("Facts must be a list")
    if not isinstance(checklist_report, dict):
        raise AttributeError("Checklist report must be a dictionary")
    if not isinstance(audit_trail, list):
        raise AttributeError("Audit trail must be a list")

    

    sar_data = {
        "narrative": narrative,
        "facts": facts,
        "checklist_report": checklist_report,
        "audit_trail": audit_trail
    }
    return sar_data

def run_page():
    # --- Resolve session dependencies with graceful fallbacks ---
    st.markdown("# Export & Audit")
    
    data = st.session_state.get("data") or st.session_state.get("case_data")
    if not data:
        st.error("Please load synthetic data first. Go to the **Case Intake** page.")
        return

    # selected facts may be stored at top-level or inside case_data
    selected_facts = (
        st.session_state.get("selected_facts")
        or (data.get("selected_facts") if isinstance(data, dict) else None)
    )
    if not selected_facts:
        st.error("Please select facts first. Go to the **Explore Data** page.")
        return

    ai_draft_narrative = st.session_state.get("ai_draft_narrative")
    if ai_draft_narrative is None:
        st.error("Please generate an AI draft narrative first. Go to the **Draft SAR** page.")
        return

    # Support either key name
    human_edited_narrative = (
        st.session_state.get("human_edited_narrative")
        or st.session_state.get("analyst_edited_narrative")
    )
    if human_edited_narrative is None:
        st.error("Please edit the narrative first. Go to the **Review & Compare** page.")
        return

    extracted_5ws = st.session_state.get("extracted_5ws")
    if extracted_5ws is None:
        st.error("Please extract 5Ws first. Go to the **Explore Data** page.")
        return

    compliance_checklist_results = st.session_state.get("compliance_checklist_results")
    if compliance_checklist_results is None:
        st.error("Please run the compliance checklist first. Go to the **Compliance Checklist & Sign-off** page.")
        return

    st.markdown("""

The final step in the SAR process is to export all relevant data in a structured and auditable format. This typically includes the final SAR narrative, supporting facts, the compliance checklist report, and a detailed audit trail of the entire investigation. This consolidated export package is essential for regulatory filings, internal record-keeping, and demonstrating adherence to AML procedures.

### Export Bundle Contents and Regulatory Utility

The export bundle serves multiple critical purposes:

*   **Regulatory Filing:** Provides all required information for submission to financial intelligence units (like FinCEN in the U.S.).
*   **Auditability:** Creates an immutable record of the investigation, including AI-generated drafts, human edits, and compliance checks, which is crucial for internal and external audits.
*   **Evidence Retention:** Ensures that all evidence supporting the SAR narrative is preserved and easily retrievable.
*   **Decision Rationale:** The audit trail captures the 'why' behind decisions made during the investigation, including the use of AI assistance.

""")

    # Helper for timestamps
    def ts_minus(minutes: int = 0) -> str:
        return (datetime.now() - timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")

    # Prepare / rebuild buttons
    col_a, col_b = st.columns([0.5, 0.5])
    with col_a:
        if st.button("📦 Prepare Export Bundle", type="primary", use_container_width=True):
            # Build audit trail entries (examples)
            audit_trail = [
                {"timestamp": ts_minus(10), "event": "AI draft generated", "model": "OPENAI", "temperature": 0.2},
                {"timestamp": ts_minus(5),  "event": "Analyst review started", "analyst_id": "AML_Analyst_001"},
                {"timestamp": ts_minus(2),  "event": "Narrative edited and changes highlighted", "analyst_id": "AML_Analyst_001"},
                {
                    "timestamp": ts_minus(1),
                    "event": "Compliance checklist run",
                    "status": "PASS" if compliance_checklist_results.get("overall") else "FAIL",
                },
                {"timestamp": ts_minus(0),  "event": "Final export prepared", "analyst_id": "AML_Analyst_001"},
            ]

            # Build bundle + bytes once and persist in session
            bundle = export_sar_data(human_edited_narrative, selected_facts, compliance_checklist_results, audit_trail)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            json_bytes = json.dumps(bundle, indent=2, default=str).encode("utf-8")
            csv_bytes = pd.DataFrame(audit_trail).to_csv(index=False).encode("utf-8")
            txt_bytes = human_edited_narrative.encode("utf-8")

            st.session_state.export_files = {
                "stamp": stamp,
                "json_bytes": json_bytes,
                "csv_bytes": csv_bytes,
                "txt_bytes": txt_bytes,
            }
            if 'export_ready' not in st.session_state:
                st.session_state.export_ready = True
            st.success("Export bundle prepared. Use the download buttons below.")

    with col_b:
        if st.button("🧹 Clear Prepared Bundle", use_container_width=True):
            st.session_state.export_files = {}
            if 'export_ready' in st.session_state:
                st.session_state.export_ready = False
            st.info("Export bundle cleared.")

    st.divider()

    # --- Always render download buttons if we have prepared bytes in session ---
    if 'export_ready' in st.session_state and st.session_state.export_ready and 'export_files' in st.session_state and st.session_state.export_files:
        stamp = st.session_state.export_files["stamp"]

        st.download_button(
            label="⬇️ Download Full SAR Export (JSON)",
            data=st.session_state.export_files["json_bytes"],
            file_name=f"SAR_export_{stamp}.json",
            mime="application/json",
            use_container_width=True,
            key=f"dl_json_{stamp}",
        )
        st.download_button(
            label="⬇️ Download Audit Trail (CSV)",
            data=st.session_state.export_files["csv_bytes"],
            file_name=f"SAR_audit_trail_{stamp}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"dl_csv_{stamp}",
        )
        st.download_button(
            label="⬇️ Download Final Narrative (TXT)",
            data=st.session_state.export_files["txt_bytes"],
            file_name=f"SAR_narrative_{stamp}.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"dl_txt_{stamp}",
        )
    else:
        st.info("Click **Prepare Export Bundle** to generate the downloadable files.")