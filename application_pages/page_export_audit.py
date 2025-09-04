import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.doctemplate import BaseDocTemplate
from io import BytesIO


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


def generate_pdf_from_json(json_data, title="SAR for the AML Case Study"):
    """Converts JSON data to a formatted PDF document."""
    buffer = BytesIO()
    
    # Create custom document with footer
    class FooterDocTemplate(BaseDocTemplate):
        def __init__(self, filename, **kwargs):
            BaseDocTemplate.__init__(self, filename, **kwargs)
            
        def afterPage(self):
            """Add footer to each page"""
            self.canv.saveState()
            
            # Get current year
            current_year = datetime.now().year
            
            # Footer content
            footer_left = f"©QuantUniversity, {current_year}"
            footer_center = "Contact info@qusandbox.com for more details"
            footer_right = f"Page {self.canv.getPageNumber()}"
            
            # Footer positioning
            footer_y = 0.2 * inch
            page_width = letter[0]
            
            # Set font for footer
            self.canv.setFont("Helvetica", 9)
            
            # Draw footer elements
            self.canv.drawString(72, footer_y, footer_left)  # Left margin
            
            # Center text
            center_width = self.canv.stringWidth(footer_center, "Helvetica", 9)
            center_x = (page_width - center_width) / 2
            self.canv.drawString(center_x, footer_y, footer_center)
            
            # Right-aligned text
            right_width = self.canv.stringWidth(footer_right, "Helvetica", 9)
            right_x = page_width - 72 - right_width  # Right margin
            self.canv.drawString(right_x, footer_y, footer_right)
            
            self.canv.restoreState()
    
    # Create document with custom template
    doc = FooterDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=36)
    
    # Create frame for content (leaving space for footer)
    frame = Frame(72, 50, letter[0]-144, letter[1]-122, 
                  leftPadding=0, bottomPadding=0, 
                  rightPadding=0, topPadding=0)
    
    # Create page template with frame
    template = PageTemplate(id='normal', frames=[frame])
    doc.addPageTemplates([template])
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#026caa')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#026caa')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.HexColor('#026caa')
    )
    
    # Add logo and header section
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logo', 'image.png')
    
    if os.path.exists(logo_path):
        # Add centered logo at the top
        logo_img = Image(logo_path, width=2.1 * inch, height=1.2*inch)
        logo_img.hAlign = 'CENTER'
        elements.append(logo_img)
        elements.append(Spacer(1, 15))
        
        # Add centered title below logo
        title_para = Paragraph(title, title_style)
        elements.append(title_para)
    else:
        # Fallback if logo not found
        title_para = Paragraph(title, title_style)
        elements.append(title_para)
    
    elements.append(Spacer(1, 10))
    
    
    # Process each section of the JSON data
    for key, value in json_data.items():
        # Add section header
        section_header = Paragraph(key.replace('_', ' ').title(), heading_style)
        elements.append(section_header)
        
        if key == 'narrative':
            # Handle narrative specially
            content_para = Paragraph(value, styles['Normal'])
            elements.append(content_para)
            
        elif key == 'facts':
            # Handle facts with better formatting
            for i, fact in enumerate(value, 1):
                if isinstance(fact, dict):
                    fact_header = Paragraph(f"<b>Fact {i}: {fact.get('type', 'Unknown')}</b>", subheading_style)
                    elements.append(fact_header)
                    
                    # Format each field in the fact
                    for fact_key, fact_value in fact.items():
                        if fact_key != 'type':  # Skip type as it's already in header
                            formatted_key = fact_key.replace('_', ' ').title()
                            formatted_value = str(fact_value)
                            # Format timestamps nicely
                            if 'timestamp' in fact_key.lower() and hasattr(fact_value, 'strftime'):
                                formatted_value = fact_value.strftime("%Y-%m-%d %H:%M:%S")
                            # Format large numbers
                            elif isinstance(fact_value, (int, float)) and fact_value > 1000:
                                if 'amount' in fact_key.lower():
                                    formatted_value = f"${fact_value:,.2f}"
                                else:
                                    formatted_value = f"{fact_value:,.4f}"
                            
                            fact_para = Paragraph(f"• <b>{formatted_key}:</b> {formatted_value}", styles['Normal'])
                            elements.append(fact_para)
                else:
                    # Handle simple string facts
                    fact_para = Paragraph(f"• {str(fact)}", styles['Normal'])
                    elements.append(fact_para)
                
                elements.append(Spacer(1, 8))
                    
        elif key == 'checklist_report':
            # Handle checklist report with better formatting
            if isinstance(value, dict):
                # Overall status first
                overall_status = "PASS" if value.get('overall', False) else "FAIL"
                status_color = colors.green if value.get('overall', False) else colors.red
                overall_para = Paragraph(f"<b>Overall Status:</b> <font color='{status_color}'>{overall_status}</font>", styles['Normal'])
                elements.append(overall_para)
                elements.append(Spacer(1, 8))
                
                # Other summary fields
                for report_key, report_value in value.items():
                    if report_key not in ['overall', 'items']:  # Handle items separately
                        formatted_key = report_key.replace('_', ' ').title()
                        if isinstance(report_value, dict):
                            # Handle nested dictionaries
                            sub_para = Paragraph(f"<b>{formatted_key}:</b>", styles['Normal'])
                            elements.append(sub_para)
                            for sub_key, sub_value in report_value.items():
                                sub_formatted = f"  • {sub_key.replace('_', ' ').title()}: {sub_value}"
                                sub_detail_para = Paragraph(sub_formatted, styles['Normal'])
                                elements.append(sub_detail_para)
                        else:
                            report_para = Paragraph(f"<b>{formatted_key}:</b> {str(report_value)}", styles['Normal'])
                            elements.append(report_para)
                
                # Handle checklist items
                if 'items' in value and isinstance(value['items'], list):
                    elements.append(Spacer(1, 10))
                    items_header = Paragraph("<b>Checklist Items:</b>", subheading_style)
                    elements.append(items_header)
                    
                    for item in value['items']:
                        if isinstance(item, dict):
                            status = "✓ PASS" if item.get('passed', False) else "✗ FAIL"
                            status_color = colors.green if item.get('passed', False) else colors.red
                            label = item.get('label', 'Unknown item')
                            
                            item_para = Paragraph(f"<font color='{status_color}'>{status}</font> - {label}", styles['Normal'])
                            elements.append(item_para)
                            
                            # Add remediation if present and failed
                            if not item.get('passed', False) and item.get('remediation'):
                                remediation_para = Paragraph(f"  <i>Remediation: {item['remediation']}</i>", styles['Normal'])
                                elements.append(remediation_para)
                            
                            elements.append(Spacer(1, 4))
                
        elif key == 'audit_trail':
            # Handle audit trail as a table
            if value and isinstance(value[0], dict):
                # Create table for audit trail
                headers = ['Timestamp', 'Event', 'Details']
                table_data = [headers]
                
                for item in value:
                    timestamp = item.get('timestamp', '')
                    event = item.get('event', '')
                    
                    # Combine other fields as details
                    details = []
                    for detail_key, detail_value in item.items():
                        if detail_key not in ['timestamp', 'event']:
                            details.append(f"{detail_key}: {detail_value}")
                    details_str = ", ".join(details) if details else ""
                    
                    row = [timestamp, event, details_str]
                    table_data.append(row)
                
                table = Table(table_data, colWidths=[2*inch, 2.5*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#026caa')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                elements.append(table)
        
        elements.append(Spacer(1, 15))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

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
        st.session_state.audit_trail = audit_trail
        # Build bundle + bytes once and persist in session
        bundle = export_sar_data(human_edited_narrative, selected_facts, compliance_checklist_results, audit_trail)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        json_bytes = json.dumps(bundle, indent=2, default=str).encode("utf-8")
        csv_bytes = pd.DataFrame(audit_trail).to_csv(index=False).encode("utf-8")
        txt_bytes = human_edited_narrative.encode("utf-8")
        
        # Generate PDF from JSON data
        try:
            pdf_bytes = generate_pdf_from_json(bundle)
            st.session_state.pdf_generation_success = True
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            pdf_bytes = b""
            st.session_state.pdf_generation_success = False

        st.session_state.export_files = {
            "stamp": stamp,
            "json_bytes": json_bytes,
            "csv_bytes": csv_bytes,
            "txt_bytes": txt_bytes,
            "pdf_bytes": pdf_bytes,
        }
        if 'export_ready' not in st.session_state:
            st.session_state.export_ready = True
        st.success("Export bundle prepared. Use the download buttons below.")

 

    st.divider()

    # --- Always render download buttons if we have prepared bytes in session ---
    if 'export_ready' in st.session_state:
        stamp = st.session_state.export_files["stamp"]
        
        st.markdown("### Final Narrative")
        st.markdown(human_edited_narrative)
        st.download_button(
            label="⬇️ Download Final Narrative (TXT)",
            data=st.session_state.export_files["txt_bytes"],
            file_name=f"SAR_narrative_{stamp}.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"dl_txt_{stamp}",
        )

        st.markdown("### Audit Trail")
        st.dataframe(pd.DataFrame(st.session_state.audit_trail))
        st.download_button(
            label="⬇️ Download Audit Trail (CSV)",
            data=st.session_state.export_files["csv_bytes"],
            file_name=f"SAR_audit_trail_{stamp}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"dl_csv_{stamp}",
        )

        st.markdown("### Full SAR Export")

        # Display PDF preview (only show if PDF generation was successful)
        if st.session_state.get("pdf_generation_success", False):
            st.markdown("### Report Preview")
            
            # Use base64 encoding to display PDF
            import base64
            base64_pdf = base64.b64encode(st.session_state.export_files["pdf_bytes"]).decode('utf-8')
            pdf_display = f'''
            <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                        width="70%" 
                        height="800" 
                        type="application/pdf"
                        style="border: 1px solid #ccc; border-radius: 5px; margin-bottom: 30px;">
                </iframe>
            </div>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)

        
        
        st.download_button(
            label="⬇️ Download Full SAR Export (JSON)",
            data=st.session_state.export_files["json_bytes"],
            file_name=f"SAR_export_{stamp}.json",
            mime="application/json",
            use_container_width=True,
            key=f"dl_json_{stamp}",
        )
        
        # Show warning if PDF generation failed
        if not st.session_state.get("pdf_generation_success", False):
            st.warning("PDF generation failed. Please try preparing the export bundle again.")
        
    else:
        st.info("Click **Prepare Export Bundle** to generate the downloadable files.")