"""test gscholar's version."""

import gscholar


def test_version() -> None:
    """Test version."""
    assert isinstance(gscholar.__VERSION__, str)
