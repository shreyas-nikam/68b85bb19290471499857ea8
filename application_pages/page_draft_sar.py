import streamlit as st
import pandas as pd


import os, requests
from dotenv import load_dotenv
load_dotenv()
from tenacity import retry, stop_after_attempt, wait_exponential

LLM_API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")      # Placeholder URL
LLM_API_KEY = os.getenv("LLM_API_KEY", os.environ.get("OPENAI_API_KEY"))      # Placeholder Key

def build_prompt(case_data, extracted_5ws):
    # Compose a chronological, fact-focused, speculative-free prompt.
    # case_data is expected to be a string or readily stringifiable.
    # extracted_5ws is expected to be a dictionary.

    # Format 5Ws for the prompt
    five_ws_formatted = "\n".join([f"  - {k}: {', '.join(map(str, v))}" for k, v in extracted_5ws.items()])

    # Convert selected_facts into a more readable string representation for the prompt
    facts_formatted = "\n".join([str(fact) for fact in case_data]) if isinstance(case_data, list) else str(case_data)
    
    return f"""
You are assisting an AML analyst to draft a SAR narrative.
Follow FinCEN guidance: be clear, concise, chronological; avoid speculation.
Include Who/What/When/Where/Why and key facts only.
Label the output as 'AI-assisted draft'.

5Ws:
{five_ws_formatted}

Facts:
{facts_formatted}

Produce a detailed narrative appropriate for an SAR filing for the above case.
Make sure the amounts are included in backticks. For example, `$40`, `$232` and `$323`.
It should include details about the customer, their transactions, and the alert received. It should clearly state who, what, when, where, and why, based on the provided facts, and must avoid speculation.
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def call_llm(prompt: str) -> str:
    if not LLM_API_KEY or LLM_API_KEY == "":
        print("Warning: LLM_API_URL or LLM_API_KEY not set. Using a dummy response.")
        return "AI-assisted draft:\nThis is a dummy AI-assisted narrative because LLM API credentials were not configured. Please set LLM_API_URL and LLM_API_KEY environment variables for real LLM interaction. The narrative should include details about Customer 7, their transactions, and the alert received. It should clearly state who, what, when, where, and why, based on the provided facts, and must avoid speculation. The customer engaged in multiple transactions between 2023-01-01 and 2023-01-03, with an alert triggered on 2023-01-05 due to suspicious activity. Details about the transaction amounts and the origin/destination latitudes and longitudes were provided."

    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o",   # configure per your provider, e.g., "gpt-4o-mini", "gemini-pro"
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 600
    }
    r = requests.post(LLM_API_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    # Adjust the path below to your provider’s response schema:
    return data["choices"][0]["message"]["content"].strip()


def extract_5ws(case_data):
    """Extracts the 5Ws (Who, What, When, Where, Why) from the provided case data.

    Args:
        case_data (list of dict or pd.DataFrame): The curated facts for the case.

    Returns:
        dict: A dictionary containing the extracted 5Ws.
    """
    five_ws = {
        'Who': [],
        'What': [],
        'When': [],
        'Where': [],
        'Why': []
    }

    if not case_data:
        return five_ws

    if isinstance(case_data, pd.DataFrame):
        records = case_data.to_dict('records')
    elif isinstance(case_data, list):
        records = case_data
    else:
        raise TypeError("Unsupported data type for case_data. Expected list of dict or Pandas DataFrame.")

    for fact in records:
        # Extract Who
        if 'name' in fact and fact['name'] not in five_ws['Who']:
            five_ws['Who'].append(fact['name'])
        if 'customer_id' in fact and f"Customer ID {fact['customer_id']}" not in five_ws['Who']:
            five_ws['Who'].append(f"Customer ID {fact['customer_id']}")

        # Extract What
        if 'reason' in fact and fact['reason'] not in five_ws['What']:
            five_ws['What'].append(fact['reason'])
        if 'transaction_amount' in fact and f"Transaction amount of {fact['transaction_amount']:,.2f}" not in five_ws['What']:
            five_ws['What'].append(f"Transaction amount of {fact['transaction_amount']:,.2f}")

        # Extract When
        if 'timestamp' in fact:
            date_str = pd.to_datetime(fact['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            if date_str not in five_ws['When']:
                five_ws['When'].append(date_str)

        # Extract Where
        if 'country' in fact and fact['country'] not in five_ws['Where']:
            five_ws['Where'].append(fact['country'])
        if 'origin_latitude' in fact and 'origin_longitude' in fact and \
           f"Lat: {{fact['origin_latitude']:.2f}}, Lon: {fact['origin_longitude']:.2f}" not in five_ws['Where']:
            five_ws['Where'].append(f"Lat: {fact['origin_latitude']:.2f}, Lon: {fact['origin_longitude']:.2f}")

        # Extract Why (often inferred or directly from alert reasons/risk scores)
        if 'risk_score' in fact and fact['risk_score'] >= 70 and f"High risk score ({{fact['risk_score']}})" not in five_ws['Why']:
            five_ws['Why'].append(f"High risk score ({fact['risk_score']})")
        if 'reason' in fact and fact['reason'] not in five_ws['Why']:
            five_ws['Why'].append(fact['reason'])

    # Clean up empty lists
    return {k: v for k, v in five_ws.items() if v}


def run_page():
    st.markdown("# Draft SAR")
    
    if 'data' not in st.session_state:
        st.error("Please load synthetic data first. Go to the **Case Intake** page.")
        return
    
    if 'selected_facts' not in st.session_state:
        st.error("Please select facts first. Go to the **Explore Data** page.")
        return
    
    case_data = st.session_state.data
    selected_facts = st.session_state.selected_facts
    
    st.markdown("## 5Ws Extraction")
    
    st.markdown('''
For any Suspicious Activity Report (SAR), clearly articulating the **5Ws** (Who, What, When, Where, Why) is paramount. These elements form the bedrock of a compliant and informative narrative, providing regulators with a concise yet comprehensive summary of the suspicious activity.

### Importance of 5Ws

*   **Clarity and Conciseness:** The 5Ws distill complex case details into easily digestible facts.
*   **Regulatory Compliance:** FinCEN (Financial Crimes Enforcement Network) guidance emphasizes the inclusion of these key elements in SAR narratives.
*   **LLM Guidance:** Providing the LLM with explicitly extracted 5Ws acts as a strong steering mechanism, ensuring the generated narrative covers all essential aspects and adheres to a factual, investigative tone.

While a more sophisticated implementation might use NLP to infer these from unstructured notes, our current approach focuses on extracting them from structured or semi-structured facts. For example:

*   **Who:** `customer_id`, `name`
*   **What:** `reason` for alert, `transaction_amount`
*   **When:** `timestamp` from transactions/alerts
*   **Where:** `country`, `origin_latitude`, `origin_longitude` from customer/transaction data
*   **Why:** `reason` for alert, or inferred from high `risk_score`
''')
    
    
    five_ws = extract_5ws(selected_facts)
    st.session_state.extracted_5ws = five_ws
    st.markdown("### Extracted 5Ws:")
    markdown_string = """
```
"""
    for key, value in five_ws.items():
        markdown_string += f"  {key}: {', '.join(map(str, value))}\n"
    markdown_string += "```"
    st.markdown(markdown_string)

    st.markdown('''
### How 5Ws Guide the Draft
The explicitly extracted 5Ws serve as a critical guide for the Language Model (LLM) when generating the SAR narrative. By providing these structured facts upfront, we ensure that the LLM focuses on the most salient points of the investigation and adheres to regulatory requirements.

*   **Structured Input:** The LLM receives clear, categorized information, reducing the likelihood of omissions or misinterpretations.
*   **Factual Basis:** The 5Ws constrain the LLM to generate a narrative strictly based on the provided evidence, preventing speculation.
*   **Compliance:** Ensures the narrative includes all necessary elements for a compliant SAR, making the analyst's review process more efficient.
*   **Chronological Order:** When combined with well-ordered facts, the LLM is prompted to construct a chronological account, which is a key FinCEN guideline.

This step significantly enhances the quality and reliability of the AI-assisted draft, transforming raw data into a structured input that the LLM can effectively use to create a coherent and compliant narrative.
''')
    
    st.markdown('''
### Governance and Control

To ensure reliable and compliant output:

*   **Explicit "AI-assisted" Label:** Every generated narrative includes this disclaimer to emphasize human accountability.
*   **Security/Privacy:** Only strictly necessary, structured facts are sent to the LLM.


This structured approach minimizes risks associated with LLM usage in sensitive financial contexts while maximizing efficiency for AML analysts.''')
    
    
    st.markdown("## AI Narrative Generation")
    
    st.markdown("""
Now, let's generate the AI narrative for the selected facts and 5Ws.
""", unsafe_allow_html=True)
    prompt = build_prompt(selected_facts, five_ws)
    
    if st.button("Generate AI Narrative"):
        with st.spinner("Generating AI narrative..."):
            ai_draft_narrative = call_llm(prompt)
        if "AI-assisted" not in ai_draft_narrative:
            ai_draft_narrative = "AI-assisted draft:\n" + ai_draft_narrative
        st.session_state.ai_draft_narrative = ai_draft_narrative
        st.markdown("\n### AI-assisted Draft Narrative:")
        st.markdown(ai_draft_narrative)
        st.divider()
        st.markdown("""### Reiteration for Human Review

The output above presents the AI-assisted draft of the SAR narrative. This draft is generated by the LLM based on the carefully curated `selected_facts` and `extracted_5ws`, adhering to the strict prompting instructions for compliance and factual reporting.

**Crucially, this is a first draft and is explicitly labeled as `AI-assisted draft`.** This label serves as a constant reminder that the narrative **requires thorough human review and potential editing by an AML analyst.** The AI's role is to automate the initial drafting, saving significant time, but the ultimate responsibility for accuracy, completeness, and compliance rests with the human analyst.

The analyst must:

*   **Verify Facts:** Ensure all statements are accurately reflected from the source data.
*   **Check Chronology and Cohesion:** Confirm the narrative flows logically and chronologically.
*   **Eliminate Speculation:** Remove any language that implies intent or makes unproven assertions.
*   **Ensure Completeness:** Add any missing details or context that the LLM might have overlooked.
*   **Adhere to FinCEN Guidance:** Make sure all regulatory requirements are met.

This human-in-the-loop approach combines the efficiency of AI with the critical judgment and expertise of human AML professionals, ensuring high-quality and compliant SAR filings.

Now move on to the `Human Review` page to edit the narrative.
""",
            unsafe_allow_html=True
        )
        
        
        