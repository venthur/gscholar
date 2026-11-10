"""test gscholar's output format validation."""

from unittest import mock

import pytest
from _pytest.capture import CaptureFixture

from gscholar import __main__ as cli


def test_invalid_output_format_exits_cleanly(
    capsys: CaptureFixture[str],
) -> None:
    """Invalid --outputformat exits 2 with a clean error, no traceback."""
    argv = ["gscholar", "-f", "bogus", "some query"]
    with mock.patch("sys.argv", argv):
        with pytest.raises(SystemExit) as exc:
            cli.main()
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err
