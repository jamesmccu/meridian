"""Tests for the meridian-detect CLI scaffold."""

import json

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


def test_validate_vertical_slice_matches_deny_flow(capsys):
    exit_code = main(["validate"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "guest-to-internal-denied" in output
    assert "D2" in output


def test_report_command_writes_detection_report(tmp_path, capsys):
    output_path = tmp_path / "report.md"

    exit_code = main(["report", "--output", str(output_path)])

    output = capsys.readouterr().out
    report = output_path.read_text(encoding="utf-8")
    assert exit_code == 0
    assert "wrote report" in output
    assert "Guest To Internal Access Detection Report" in report
    assert "evt-denied-guest-access-001" in report
    assert "D2" in report


def test_validate_fails_when_event_does_not_match_deny_rule(tmp_path, capsys):
    event = json.loads(
        open(
            "detection-engineering/sample-events/denied-guest-access.json",
            encoding="utf-8",
        ).read()
    )
    event["destination_zone"] = "cloud-public-app"
    event_path = tmp_path / "event.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")

    exit_code = main(["validate", "--event", str(event_path)])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "does not match a deny flow" in output


def test_allowed_event_does_not_trigger_denied_access_detection(tmp_path, capsys):
    event = json.loads(
        open(
            "detection-engineering/sample-events/denied-guest-access.json",
            encoding="utf-8",
        ).read()
    )
    event.update(
        {
            "event_id": "evt-allowed-employee-access-001",
            "source_zone": "branch-employee-client",
            "destination_zone": "branch-local-service",
            "source_service": "branch-employee-client",
            "destination_service": "branch-local-service",
            "port": 80,
            "action": "allow",
            "service": "HTTP or TCP health endpoint",
            "rationale": "Employees need approved access to a local branch service.",
            "flow_id": "A1",
            "severity": "informational",
        }
    )
    event_path = tmp_path / "allowed-event.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")

    exit_code = main(["validate", "--event", str(event_path)])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "does not match a deny flow" in output


def test_schema_invalid_event_fails_cleanly(tmp_path, capsys):
    event = json.loads(
        open(
            "detection-engineering/sample-events/denied-guest-access.json",
            encoding="utf-8",
        ).read()
    )
    del event["event_type"]
    event_path = tmp_path / "malformed-event.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")

    exit_code = main(["validate", "--event", str(event_path)])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "event missing required fields" in output
    assert "event_type" in output
