import pytest
from definition_64bab8bcd99f42b28a0f9802121bd8a8 import generate_ai_narrative
from unittest.mock import patch

@pytest.fixture
def mock_build_prompt():
    with patch('definition_64bab8bcd99f42b28a0f9802121bd8a8.build_prompt') as mock:
        yield mock

@pytest.fixture
def mock_call_llm():
    with patch('definition_64bab8bcd99f42b28a0f9802121bd8a8.call_llm') as mock:
        yield mock

def test_generate_ai_narrative_success(mock_build_prompt, mock_call_llm):
    case_data = "Some case data"
    extracted_5ws = {"who": "John Doe", "what": "Suspicious transaction"}
    mock_build_prompt.return_value = "Test prompt"
    mock_call_llm.return_value = "This is an AI-assisted narrative."
    
    narrative = generate_ai_narrative(case_data, extracted_5ws)
    
    assert "AI-assisted" in narrative
    assert narrative == "This is an AI-assisted narrative."
    mock_build_prompt.assert_called_once_with(case_data, extracted_5ws)
    mock_call_llm.assert_called_once_with("Test prompt")

def test_generate_ai_narrative_no_ai_assisted(mock_build_prompt, mock_call_llm):
    case_data = "Some case data"
    extracted_5ws = {"who": "John Doe", "what": "Suspicious transaction"}
    mock_build_prompt.return_value = "Test prompt"
    mock_call_llm.return_value = "This is a narrative."
    
    narrative = generate_ai_narrative(case_data, extracted_5ws)
    
    assert "AI-assisted" in narrative
    assert narrative == "AI-assisted draft:\nThis is a narrative."
    mock_build_prompt.assert_called_once_with(case_data, extracted_5ws)
    mock_call_llm.assert_called_once_with("Test prompt")

def test_generate_ai_narrative_empty_case_data(mock_build_prompt, mock_call_llm):
    case_data = ""
    extracted_5ws = {"who": "John Doe", "what": "Suspicious transaction"}
    mock_build_prompt.return_value = "Test prompt"
    mock_call_llm.return_value = "This is an AI-assisted narrative."
    
    narrative = generate_ai_narrative(case_data, extracted_5ws)
    
    assert "AI-assisted" in narrative
    mock_build_prompt.assert_called_once_with(case_data, extracted_5ws)
    mock_call_llm.assert_called_once_with("Test prompt")

def test_generate_ai_narrative_empty_5ws(mock_build_prompt, mock_call_llm):
    case_data = "Some case data"
    extracted_5ws = {}
    mock_build_prompt.return_value = "Test prompt"
    mock_call_llm.return_value = "This is an AI-assisted narrative."
    
    narrative = generate_ai_narrative(case_data, extracted_5ws)
    
    assert "AI-assisted" in narrative
    mock_build_prompt.assert_called_once_with(case_data, extracted_5ws)
    mock_call_llm.assert_called_once_with("Test prompt")

def test_generate_ai_narrative_both_empty(mock_build_prompt, mock_call_llm):
    case_data = ""
    extracted_5ws = {}
    mock_build_prompt.return_value = "Test prompt"
    mock_call_llm.return_value = "This is an AI-assisted narrative."
    
    narrative = generate_ai_narrative(case_data, extracted_5ws)
    
    assert "AI-assisted" in narrative
    mock_build_prompt.assert_called_once_with(case_data, extracted_5ws)
    mock_call_llm.assert_called_once_with("Test prompt")
