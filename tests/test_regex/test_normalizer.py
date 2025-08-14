"""
Tests for regex normalizer.
"""

from src.regex.normalizer import normalize_regex


def test_normalize_regex_basic():
    """Test basic regex normalization."""
    assert normalize_regex("a b") == "ab"
    assert normalize_regex("  a|b  ") == "a|b"
    assert normalize_regex("a*+b") == "a*+b"


def test_normalize_regex_epsilon():
    """Test epsilon normalization."""
    assert normalize_regex("eps") == "ε"
    assert normalize_regex("EPSILON") == "ε"
    assert normalize_regex("epsilon") == "ε"
    assert normalize_regex("EPS") == "ε"
    assert normalize_regex("(e)") == "(ε)"


def test_normalize_regex_complex():
    """Test complex regex normalization."""
    input_regex = "  (a|eps)* + b  "
    expected = "(a|ε)*+b"
    assert normalize_regex(input_regex) == expected 