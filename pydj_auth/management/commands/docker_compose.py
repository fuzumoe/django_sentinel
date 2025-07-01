"""
Django management command for Docker Compose operations.

This module provides a unified interface for managing Docker Compose services
through Django's management command system. It supports all common Docker
Compose operations including starting, stopping, restarting services, viewing
logs, and checking service status.

Usage:
    python manage.py docker_compose <subcommand> [options]

Available subcommands:
    - up: Start services (with optional --logs flag)
    - down: Stop services (with optional --volumes flag)
    - restart: Restart all services
    - logs: View service logs (with optional service name and --follow flag)
    - status: Show current service status

Examples:
    python manage.py docker_compose up
    python manage.py docker_compose up --logs
    python manage.py docker_compose down --volumes
    python manage.py docker_compose logs db
    python manage.py docker_compose status
"""

import subprocess
from typing import Any

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Django management command for Docker Compose operations."""

    help = "Manage Docker Compose services"

    def add_arguments(self, parser: Any) -> None:
        """Define command line arguments for Docker Compose subcommands."""
        subparsers = parser.add_subparsers(
            dest="action", help="Docker Compose actions", required=True
        )

        # Up command
        up_parser = subparsers.add_parser("up", help="Start services")
        up_parser.add_argument(
            "--logs",
            action="store_true",
            help="Start with logs (not detached)",
        )

        # Down command
        down_parser = subparsers.add_parser("down", help="Stop services")
        down_parser.add_argument(
            "--volumes",
            action="store_true",
            help="Remove volumes as well",
        )

        # Restart command
        subparsers.add_parser("restart", help="Restart services")

        # Logs command
        logs_parser = subparsers.add_parser("logs", help="View logs")
        logs_parser.add_argument(
            "--follow",
            "-f",
            action="store_true",
            help="Follow log output",
            default=True,
        )
        logs_parser.add_argument(
            "service",
            nargs="?",
            help="Show logs for specific service only",
        )

        # Status command
        subparsers.add_parser("status", help="Show service status")

    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the Docker Compose command execution."""
        action = options["action"]

        if action == "up":
            self._handle_up(options)
        elif action == "down":
            self._handle_down(options)
        elif action == "restart":
            self._handle_restart()
        elif action == "logs":
            self._handle_logs(options)
        elif action == "status":
            self._handle_status(options)

    def _handle_up(self, options: dict[str, Any]) -> None:
        """Handle the 'up' subcommand to start Docker Compose services."""
        if options["logs"]:
            cmd = ["docker-compose", "up"]
            self.stdout.write("🐳 Starting Docker Compose with logs...")
        else:
            cmd = ["docker-compose", "up", "-d"]
            self.stdout.write("🐳 Starting Docker Compose in detached mode...")

        self._run_command(cmd, "✅ Docker Compose started successfully!")

    def _handle_down(self, options: dict[str, Any]) -> None:
        """Handle the 'down' subcommand to stop Docker Compose services."""
        cmd = ["docker-compose", "down"]
        if options["volumes"]:
            cmd.append("-v")
            msg = "🛑 Stopping Docker Compose and removing volumes..."
            self.stdout.write(msg)
        else:
            self.stdout.write("🛑 Stopping Docker Compose...")

        self._run_command(cmd, "✅ Docker Compose stopped successfully!")

    def _handle_restart(self) -> None:
        """Handle the 'restart' subcommand to restart services."""
        self.stdout.write("🔄 Restarting Docker Compose services...")
        self._run_command(
            ["docker-compose", "restart"],
            "✅ Docker Compose restarted successfully!"
        )

    def _handle_logs(self, options: dict[str, Any]) -> None:
        """Handle the 'logs' subcommand to view service logs."""
        cmd = ["docker-compose", "logs"]

        if options["follow"]:
            cmd.append("-f")

        if options["service"]:
            cmd.append(options["service"])
            msg = f"📋 Viewing logs for {options['service']}..."
            self.stdout.write(msg)
        else:
            self.stdout.write("📋 Viewing Docker Compose logs...")

        self._run_command(cmd)

    def _handle_status(self, options: dict[str, Any]) -> None:
        """Handle the 'status' subcommand to show service status."""
        self.stdout.write("📊 Docker Compose service status:")
        self._run_command(["docker-compose", "ps"])

    def _run_command(
        self, cmd: list[str], success_msg: str | None = None
    ) -> None:
        """Execute a Docker Compose command with error handling."""
        try:
            subprocess.run(cmd, check=True)
            if success_msg:
                # pylint: disable=no-member
                self.stdout.write(self.style.SUCCESS(success_msg))
        except subprocess.CalledProcessError as e:
            raise CommandError(f"❌ Docker Compose failed: {e}") from e
        except FileNotFoundError as exc:
            msg = "❌ docker-compose not found. Make sure Docker is installed."
            raise CommandError(msg) from exc
