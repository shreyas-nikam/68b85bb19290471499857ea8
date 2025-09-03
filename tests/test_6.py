import pytest
from definition_ac6292bf34244babb0aa2f525772bc53 import build_prompt

@pytest.mark.parametrize("case_data, extracted_5ws, expected", [
    ("Transaction of $1000 on 2024-01-01.", {"who": "John Doe", "what": "Suspicious transaction", "when": "2024-01-01", "where": "New York", "why": "Unexplained source of funds"}, 
     "\nYou are assisting an AML analyst to draft a SAR narrative.\nFollow FinCEN guidance: be clear, concise, chronological; avoid speculation.\nInclude Who/What/When/Where/Why and key facts only.\nLabel the output as 'AI-assisted draft'.\n\n5Ws:\n{'who': 'John Doe', 'what': 'Suspicious transaction', 'when': '2024-01-01', 'where': 'New York', 'why': 'Unexplained source of funds'}\n\nFacts:\nTransaction of $1000 on 2024-01-01.\n\nProduce a single narrative paragraph set appropriate for a SAR filing.\n"),
    ("", {}, "\nYou are assisting an AML analyst to draft a SAR narrative.\nFollow FinCEN guidance: be clear, concise, chronological; avoid speculation.\nInclude Who/What/When/Where/Why and key facts only.\nLabel the output as 'AI-assisted draft'.\n\n5Ws:\n{}\n\nFacts:\n\nProduce a single narrative paragraph set appropriate for a SAR filing.\n"),
    ("Large cash deposit.", {"who": "", "what": "", "when": "", "where": "", "why": ""}, 
     "\nYou are assisting an AML analyst to draft a SAR narrative.\nFollow FinCEN guidance: be clear, concise, chronological; avoid speculation.\nInclude Who/What/When/Where/Why and key facts only.\nLabel the output as 'AI-assisted draft'.\n\n5Ws:\n{'who': '', 'what': '', 'when': '', 'where': '', 'why': ''}\n\nFacts:\nLarge cash deposit.\n\nProduce a single narrative paragraph set appropriate for a SAR filing.\n"),
    ("Transaction from a sanctioned country.", {"who": "ABC Corp", "what": "Transaction", "when": "2024-02-15", "where": "Sanctioned Country X", "why": "Potential sanctions violation"}, 
     "\nYou are assisting an AML analyst to draft a SAR narrative.\nFollow FinCEN guidance: be clear, concise, chronological; avoid speculation.\nInclude Who/What/When/Where/Why and key facts only.\nLabel the output as 'AI-assisted draft'.\n\n5Ws:\n{'who': 'ABC Corp', 'what': 'Transaction', 'when': '2024-02-15', 'where': 'Sanctioned Country X', 'why': 'Potential sanctions violation'}\n\nFacts:\nTransaction from a sanctioned country.\n\nProduce a single narrative paragraph set appropriate for a SAR filing.\n"),
    ("Transaction from a sanctioned country.", None, TypeError),
])

def test_build_prompt(case_data, extracted_5ws, expected):
    if expected == TypeError:
        with pytest.raises(TypeError):
            build_prompt(case_data, extracted_5ws)
    else:
        assert build_prompt(case_data, extracted_5ws) == expected
