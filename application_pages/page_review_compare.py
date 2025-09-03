import streamlit as st
import re, html
from difflib import SequenceMatcher

# ---------- helpers ----------
def _tokenize_with_ws(text: str):
    """Split into tokens that preserve whitespace segments (spaces, tabs, newlines)."""
    return re.findall(r'\s+|[^\s]+', text, flags=re.UNICODE)

def _inline_diff_preserve_ws(a: str, b: str) -> str:
    """Inline diff (token-level) that preserves whitespace/newlines."""
    a_tokens = _tokenize_with_ws(a)
    b_tokens = _tokenize_with_ws(b)
    sm = SequenceMatcher(None, a_tokens, b_tokens, autojunk=False)
    parts = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            seg = "".join(a_tokens[i1:i2])
            parts.append(html.escape(seg))
        elif tag == "delete":
            seg = "".join(a_tokens[i1:i2])
            parts.append(
                '<del style="background:#691111;border:1px solid #f1a4a4;'
                'border-radius:3px;text-decoration:none;">'
                + html.escape(seg) + '</del>'
            )
        elif tag == "insert":
            seg = "".join(b_tokens[j1:j2])
            parts.append(
                '<ins style="background:#094f02;border:1px solid #96e096;'
                'border-radius:3px;text-decoration:none;">'
                + html.escape(seg) + '</ins>'
            )
        elif tag == "replace":
            old = "".join(a_tokens[i1:i2])
            new = "".join(b_tokens[j1:j2])
            parts.append(
                '<del style="background:#691111;border:1px solid #f1a4a4;'
                'border-radius:3px;text-decoration:none;">'
                + html.escape(old) + '</del>'
            )
            parts.append(
                '<ins style="background:#094f02;border:1px solid #96e096;'
                'border-radius:3px;text-decoration:none;">'
                + html.escape(new) + '</ins>'
            )
    return "".join(parts)

def _split_paragraphs(text: str):
    """
    Split on blank lines into paragraphs.
    Keeps paragraph text as-is (no trailing separators).
    """
    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Split on one or more blank lines
    if not text.strip():
        return []
    return re.split(r'\n\s*\n+', text.strip('\n'))

# ---------- main ----------
def highlight_changes(ai_draft: str, analyst_edited: str, replace_inline_threshold: float = 0.60) -> str:
    """
    Paragraph-aware HTML diff:
      - Deleted paragraphs: full block with red background.
      - Inserted paragraphs: full block with green background.
      - Equal or similar (1:1) replaced paragraphs: inline diff preserving whitespace.
    """
    if ai_draft == analyst_edited:
        return "<p>No changes detected. The analyst's edited narrative is identical to the AI draft.</p>"

    a_pars = _split_paragraphs(ai_draft)
    b_pars = _split_paragraphs(analyst_edited)

    sm = SequenceMatcher(None, a_pars, b_pars, autojunk=False)
    out = []

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            # Same paragraph(s): render as-is (escaped)
            for k in range(i1, i2):
                out.append(
                    '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;">'
                    + html.escape(a_pars[k]) + '</div>'
                )

        elif tag == "delete":
            # Entire paragraphs removed
            for k in range(i1, i2):
                out.append(
                    '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                    'background:#6e0c0c;border:1px solid #f1a4a4;border-left:4px solid #f16b6b;'
                    'border-radius:4px;padding:0.5rem;">'
                    '<span style="font-size:0.85em;color:#b00000;font-weight:600;">Deleted paragraph</span><br>'
                    '<span style="text-decoration:none;">' + html.escape(a_pars[k]) + '</span>'
                    '</div>'
                )

        elif tag == "insert":
            # Entire paragraphs added
            for k in range(j1, j2):
                out.append(
                    '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                    'background:#0a3804;border:1px solid #96e096;border-left:4px solid #36b24a;'
                    'border-radius:4px;padding:0.5rem;">'
                    '<span style="font-size:0.85em;color:#0b5f16;font-weight:600;">Inserted paragraph</span><br>'
                    '<span style="text-decoration:none;">' + html.escape(b_pars[k]) + '</span>'
                    '</div>'
                )

        elif tag == "replace":
            # Paragraphs changed. If it's a one-to-one change and similar enough, do inline diff.
            a_block = "\n\n".join(a_pars[i1:i2])
            b_block = "\n\n".join(b_pars[j1:j2])

            if (i2 - i1 == 1) and (j2 - j1 == 1):
                # Single paragraph on both sides; decide inline vs block swap based on similarity
                sim = SequenceMatcher(None, a_pars[i1], b_pars[j1], autojunk=False).ratio()
                if sim >= replace_inline_threshold:
                    out.append(
                        '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                        'background:#a18700;border:1px solid #f0e6a6;border-left:4px solid #e5cf45;'
                        'border-radius:4px;padding:0.5rem;">'
                        '<span style="font-size:0.85em;color:#6b5d00;font-weight:600;">Edited paragraph</span><br>'
                        + _inline_diff_preserve_ws(a_pars[i1], b_pars[j1]) +
                        '</div>'
                    )
                else:
                    # Treat as delete + insert blocks
                    out.append(
                        '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                        'background:#6e0c0c;border:1px solid #f1a4a4;border-left:4px solid #f16b6b;'
                        'border-radius:4px;padding:0.5rem;">'
                        '<span style="font-size:0.85em;color:#b00000;font-weight:600;">Deleted paragraph</span><br>'
                        + html.escape(a_pars[i1]) + '</div>'
                    )
                    out.append(
                        '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                        'background:#0a3804;border:1px solid #96e096;border-left:4px solid #36b24a;'
                        'border-radius:4px;padding:0.5rem;">'
                        '<span style="font-size:0.85em;color:#0b5f16;font-weight:600;">Inserted paragraph</span><br>'
                        + html.escape(b_pars[j1]) + '</div>'
                    )
            else:
                # Many-to-many change: show the whole replaced block as delete + insert
                out.append(
                    '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                    'background:#6e0c0c;border:1px solid #f1a4a4;border-left:4px solid #f16b6b;'
                    'border-radius:4px;padding:0.5rem;">'
                    '<span style="font-size:0.85em;color:#b00000;font-weight:600;">Deleted block</span><br>'
                    + html.escape(a_block) + '</div>'
                )
                out.append(
                    '<div style="white-space:pre-wrap;line-height:1.6;margin:0 0 0.75rem 0;'
                    'background:#0a3804;border:1px solid #96e096;border-left:4px solid #36b24a;'
                    'border-radius:4px;padding:0.5rem;">'
                    '<span style="font-size:0.85em;color:#0b5f16;font-weight:600;">Inserted block</span><br>'
                    + html.escape(b_block) + '</div>'
                )

    return '<div style="white-space:pre-wrap;line-height:1.6">' + "".join(out) + "</div>"


def run_page():
    st.markdown("# Human Review")
    
    if 'data' not in st.session_state:
        st.error("Please load synthetic data first. Go to the **Case Intake** page.")
        return
    
    data = st.session_state.data
    
    if 'selected_facts' not in st.session_state:
        st.error("Please select facts first. Go to the **Explore Data** page.")
        return
    
    selected_facts = st.session_state.selected_facts
    
    if 'ai_draft_narrative' not in st.session_state:
        st.error("Please generate an AI draft narrative first. Go to the **Draft SAR** page.")
        return
    
    ai_draft_narrative = st.session_state.ai_draft_narrative
    
            
    st.markdown("""
Following the AI's initial draft, the human analyst takes over. This critical step involves reviewing the AI-generated narrative, making necessary edits, adding more context, or refining language to ensure absolute accuracy, clarity, and compliance. This **human-in-the-loop** process is non-negotiable for SAR filings.

### Human Edits and Rationale

Analysts bring their expertise to:

*   **Refine language:** Improve grammar, syntax, and overall readability.
*   **Add nuance:** Incorporate subtle details or investigative insights that even a well-prompted LLM might miss.
*   **Correct inaccuracies:** Rectify any factual errors or misinterpretations by the AI.
*   **Ensure compliance:** Verify that the narrative meets all FinCEN guidelines, especially concerning the avoidance of speculation and the strict adherence to facts.

Now you can edit the following narrative as an expert analyst would. For example, remove the `AI-assisted draft` label, add more context, or refine language to ensure absolute accuracy, clarity, and compliance from the below narrative.
                """,
                unsafe_allow_html=True
            )
    
    if "human_edited_narrative" not in st.session_state:
        st.session_state.human_edited_narrative = ai_draft_narrative
    
    edited_narrative = st.text_area("Human Edited Narrative", value=st.session_state.human_edited_narrative, height=300)
    
    if st.button("Save Human Edited Narrative"):
        st.session_state.human_edited_narrative = edited_narrative
        st.success("Human edited narrative saved successfully.")
    
    st.divider()
    
    # show the changes
    st.markdown("## Changes")

    highlighted_diff = highlight_changes(ai_draft_narrative, st.session_state.human_edited_narrative)
    

    st.markdown("### Highlighted Changes (AI Draft vs. Analyst Edited - deletions in red, insertions in green)")
    st.markdown(highlighted_diff, unsafe_allow_html=True)

    st.markdown("""               
#### Audit Implications

Tracking these changes is crucial for **auditability** and **governance**:

*   **Transparency:** Provides a clear record of how the AI's output was modified by human intervention.
*   **Accountability:** Establishes a clear audit trail, demonstrating that human analysts exercise judgment and control over AI-generated content.
*   **Training and Feedback:** Differences can inform future prompt engineering or model fine-tuning efforts, helping to improve the AI's initial drafting quality.

This diffing mechanism ensures that every SAR filing has a transparent history, reinforcing trust in the AI-assisted process and satisfying regulatory scrutiny.

Next, the narrative undergoes a compliance review to ensure it meets all regulatory requirements and internal policies.
Move to the `Compliance Checklist & Sign-off` page to review the narrative.
                """)
    
   