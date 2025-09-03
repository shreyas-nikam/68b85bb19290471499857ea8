import pytest
from definition_c14ae05e14444ee680fa6706b245aa47 import highlight_changes

@pytest.mark.parametrize("ai_draft, analyst_edited, expected", [
    ("The quick brown fox.", "The quick brown fox.", ""),
    ("The quick brown fox.", "The slow brown fox.", "quick <ins>slow</ins>"),
    ("The quick brown fox.", "The quick brown fox jumps.", " <ins>jumps</ins>"),
    ("The quick brown fox.", "The brown fox.", "The quick <del>quick </del>brown fox."),
    ("", "The brown fox.", "<ins>The brown fox.</ins>"),
])

def test_highlight_changes(ai_draft, analyst_edited, expected):
    # Simple string comparison and highlighting of changes
    if expected == "":
        assert highlight_changes(ai_draft, analyst_edited) == ""
    elif "<ins>" in expected or "<del>" in expected:
      #checking if any change exists
        assert expected in highlight_changes(ai_draft, analyst_edited)
    else:
        assert highlight_changes(ai_draft, analyst_edited) == expected
