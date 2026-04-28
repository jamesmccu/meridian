"""Tests for the meridian-detect CLI scaffold."""

from meridian_detect.cli import main


def test_help_returns_success(capsys):
    exit_code = main([])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Detection engineering CLI scaffold" in output
    assert "validate" in output


def test_config_command_returns_current_config(capsys):
    exit_code = main(["config"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "quickwit_url" in output


def test_placeholder_command_is_explicit(capsys):
    exit_code = main(["validate"])

    output = capsys.readouterr().out
    assert exit_code == 2
    assert "placeholder only" in output
