"""test gscholar."""

import pytest

from gscholar import gscholar as gs


@pytest.mark.xfail(reason="Google's rate limiter.")
def test_query() -> None:
    """Normal query with latin encoding should give non empty result."""
    result = gs.query("Albert Einstein", gs.FORMAT_BIBTEX)
    assert len(result) > 0


@pytest.mark.xfail(reason="Google's rate limiter.")
def test_query_utf8() -> None:
    """Normal query with utf8 encoding should give non empty result."""
    result = gs.query("Anders Jonas Ångström", gs.FORMAT_BIBTEX)
    assert len(result) > 0
