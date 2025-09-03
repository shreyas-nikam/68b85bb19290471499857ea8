import pytest
from definition_7263c9c83df9452e89ed1788ac749940 import call_llm
import requests
from unittest.mock import patch

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("LLM_API_URL", "https://test.llm/api")
    monkeypatch.setenv("LLM_API_KEY", "test_key")

@patch('requests.post')
def test_call_llm_success(mock_post, mock_env_vars):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "Test response"}}]}
    response = call_llm("Test prompt")
    assert response == "Test response"

@patch('requests.post')
def test_call_llm_api_error(mock_post, mock_env_vars):
    mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API Error")
    with pytest.raises(requests.exceptions.HTTPError):
        call_llm("Test prompt")

@patch('requests.post')
def test_call_llm_empty_prompt(mock_post, mock_env_vars):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"choices": [{"message": {"content": "Response to empty prompt"}}]}
    response = call_llm("")
    assert response == "Response to empty prompt"

@patch('requests.post')
def test_call_llm_timeout(mock_post, mock_env_vars):
    mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
    with pytest.raises(requests.exceptions.Timeout):
        call_llm("Test prompt")

@patch('requests.post')
def test_call_llm_no_content(mock_post, mock_env_vars):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"choices": [{"message": {"content": ""}}]}
    response = call_llm("Test prompt")
    assert response == ""
