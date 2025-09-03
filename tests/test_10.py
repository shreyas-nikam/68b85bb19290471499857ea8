import pytest
from definition_678df8a5972a41f5aacd1f958198333a import run_compliance_checklist

@pytest.mark.parametrize("narrative, extracted_5ws, expected", [
    ("The suspect transferred $10,000 on Monday at 2 PM in New York from account A to account B.", {"who": "suspect", "what": "transfer of $10,000", "when": "Monday at 2 PM", "where": "New York", "why": "unknown"}, {"5Ws": True, "chronology": True, "clarity": True, "length": True}),
    ("", {"who": "", "what": "", "when": "", "where": "", "why": ""}, {"5Ws": False, "chronology": True, "clarity": True, "length": True}),
    ("The events occurred in a confusing order", {"who": "suspect", "what": "transfer of $10,000", "when": "Monday at 2 PM", "where": "New York", "why": "unknown"}, {"5Ws": True, "chronology": False, "clarity": False, "length": True}),
    ("This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. This is a very long narrative exceeding the length constraints. ", {"who": "suspect", "what": "transfer of $10,000", "when": "Monday at 2 PM", "where": "New York", "why": "unknown"}, {"5Ws": True, "chronology": True, "clarity": True, "length": False}),
    ("Subject may have been involved in illegal activities.", {"who": "suspect", "what": "transfer of $10,000", "when": "Monday at 2 PM", "where": "New York", "why": "unknown"}, {"5Ws": True, "chronology": True, "clarity": True, "length": True, "speculation": False}),
])
def test_run_compliance_checklist(narrative, extracted_5ws, expected):
    report = run_compliance_checklist(narrative, extracted_5ws)
    # Basic check, the implementation should return a dictionary
    assert isinstance(report, dict)
    # check for the 5Ws key if it's there in the result.
    assert "5Ws" in report
    assert "chronology" in report
    assert "clarity" in report
    assert "length" in report
    if "speculation" in expected:
        assert "speculation" in report
        assert report["speculation"] == expected["speculation"]
    assert report["5Ws"] == expected["5Ws"]
    assert report["chronology"] == expected["chronology"]
    assert report["clarity"] == expected["clarity"]
    assert report["length"] == expected["length"]
