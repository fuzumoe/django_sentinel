import subprocess

import pytest

from pydj_auth.management.commands.docker_compose import Command, CommandError


def test_parser_and_help():
    """Parser includes all subcommands and help text is correct."""
    cmd = Command()
    parser = cmd.create_parser("manage.py", "docker_compose")
    help_text = parser.format_help()
    for action in ("up", "down", "restart", "logs", "status"):
        assert action in help_text
    assert cmd.help == "Manage Docker Compose services"


@pytest.mark.parametrize(
    ("logs_flag", "expected_cmd", "expected_msg"),
    [
        (False, ["docker-compose", "up", "-d"], "detached mode"),
        (True, ["docker-compose", "up"], "with logs"),
    ],
)
def test_handle_up(monkeypatch, capsys, logs_flag, expected_cmd, expected_msg):
    """_handle_up starts services with correct flags and output."""

    def fake_run(cmd_args, check):
        assert cmd_args == expected_cmd
        assert check is True

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_run
    )
    cmd = Command()
    cmd._handle_up({"logs": logs_flag})
    captured = capsys.readouterr()
    assert expected_msg in captured.out


def test_handle_down(monkeypatch, capsys):
    """_handle_down stops services, optionally removing volumes."""

    # without volumes
    def fake_no_vol(cmd_args, check):
        assert cmd_args == ["docker-compose", "down"]

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_no_vol
    )
    cmd = Command()
    cmd._handle_down({"volumes": False})
    captured = capsys.readouterr()
    assert "Stopping Docker Compose..." in captured.out

    # with volumes
    def fake_with_vol(cmd_args, check):
        assert cmd_args == ["docker-compose", "down", "-v"]

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_with_vol
    )
    cmd = Command()
    cmd._handle_down({"volumes": True})
    captured = capsys.readouterr()
    assert "removing volumes" in captured.out


def test_handle_restart(monkeypatch, capsys):
    """_handle_restart calls subprocess and prints restart message."""

    def fake_run(cmd_args, check):
        assert cmd_args == ["docker-compose", "restart"]

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_run
    )
    cmd = Command()
    cmd._handle_restart()
    captured = capsys.readouterr()
    assert "Restarting Docker Compose services" in captured.out


@pytest.mark.parametrize(
    ("service", "expected_cmd", "expected_msg"),
    [
        (None, ["docker-compose", "logs", "-f"], "Viewing Docker Compose logs"),
        ("web", ["docker-compose", "logs", "-f", "web"], "Viewing logs for web"),
    ],
)
def test_handle_logs(monkeypatch, capsys, service, expected_cmd, expected_msg):
    """_handle_logs follows logs for all or a specific service."""

    def fake_run(cmd_args, check):
        assert cmd_args == expected_cmd

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_run
    )
    cmd = Command()
    cmd._handle_logs({"follow": True, "service": service})
    captured = capsys.readouterr()
    assert expected_msg in captured.out


def test_handle_status(monkeypatch, capsys):
    """_handle_status prints status header and calls subprocess."""

    def fake_run(cmd_args, check):
        assert cmd_args == ["docker-compose", "ps"]

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_run
    )
    cmd = Command()
    cmd._handle_status()
    captured = capsys.readouterr()
    assert "service status" in captured.out


def test_run_command_exceptions(monkeypatch):
    """_run_command raises CommandError on subprocess errors."""

    # CalledProcessError
    def fake_error(cmd_args, check):
        raise subprocess.CalledProcessError(1, cmd_args)

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_error
    )
    cmd = Command()
    with pytest.raises(CommandError):
        cmd._run_command(["fail"])

    # FileNotFoundError
    def fake_missing(cmd_args, check):
        raise FileNotFoundError()

    monkeypatch.setattr(
        "pydj_auth.management.commands.docker_compose.subprocess.run", fake_missing
    )
    cmd = Command()
    with pytest.raises(CommandError) as exc_info:
        cmd._run_command(["missing"])
    assert "docker-compose not found" in str(exc_info.value)
