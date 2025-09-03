import streamlit as st
import json
import pandas as pd
from application_pages.utils import export_sar_data
import hashlib

def run_page_export_audit():
    st.header("6. Export & Audit")
    st.markdown("""
    This final page allows you to export the completed SAR narrative, supporting facts,
    the compliance checklist report, and a detailed audit trail.
    """)

    if not st.session_state.get('sar_signed_off', False):
        st.warning("SAR must be signed off on the 'Compliance Checklist & Sign-off' page before export.")
        return

    st.subheader("Export Final SAR Package")

    if st.session_state.analyst_edited_narrative:
        # Prepare data for export
        final_narrative = st.session_state.analyst_edited_narrative
        supporting_facts = st.session_state.draft_facts_tray
        checklist_report = st.session_state.compliance_checklist_results
        audit_trail = st.session_state.audit_trail

        export_package = export_sar_data(final_narrative, supporting_facts, checklist_report, audit_trail)
        export_json_string = json.dumps(export_package, indent=4)

        st.download_button(
            label="Download Final SAR Package (JSON)",
            data=export_json_string,
            file_name="final_sar_package.json",
            mime="application/json"
        )
        st.success("SAR package ready for download.")
    else:
        st.info("No final narrative available for export.")

    st.divider()

    st.subheader("Audit Trail")
    st.markdown("""
    The audit trail records significant actions and changes throughout the SAR drafting process,
    providing a complete history for accountability and compliance.
    """)

    if st.session_state.audit_trail:
        audit_df = pd.DataFrame(st.session_state.audit_trail)
        st.dataframe(audit_df)

        st.download_button(
            label="Download Audit Trail (CSV)",
            data=audit_df.to_csv(index=False).encode('utf-8'),
            file_name="sar_audit_trail.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download Audit Trail (JSON)",
            data=json.dumps(st.session_state.audit_trail, indent=4),
            file_name="sar_audit_trail.json",
            mime="application/json"
        )
    else:
        st.info("No audit trail entries yet.")

    st.divider()

    st.subheader("Content Immutability Verification")
    st.markdown("""
    The final content hash provides an immutable record of the SAR narrative at the time of sign-off.
    This can be used to verify that the exported narrative matches the approved version.
    """)
    if st.session_state.get('sar_signed_off', False) and st.session_state.analyst_edited_narrative:
        final_hash_value = hashlib.sha256(st.session_state.analyst_edited_narrative.encode('utf-8')).hexdigest()
        st.write(f"**Final Narrative SHA256 Hash:** `{final_hash_value}`")
        st.info("This hash ensures the integrity of the signed-off narrative.")
    else:
        st.info("Sign off the SAR to generate a final content hash.")
