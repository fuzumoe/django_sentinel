import subprocess
import time

import pytest


@pytest.fixture(scope="module")
def compose_services():
    """Start all services via Django management command and tear down after tests."""
    # Start services detached
    subprocess.run(
        ["uv", "run", "python", "manage.py", "docker_compose", "up", "-d"], check=True
    )
    # Wait for containers to initialize
    time.sleep(5)
    yield
    # Tear down services
    subprocess.run(
        ["uv", "run", "python", "manage.py", "docker_compose", "down"], check=True
    )


def test_up_and_db_running(compose_services):
    """E2E: Ensure 'up' command starts the database container."""
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=postgres_db", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "postgres_db" in result.stdout


def test_status(compose_services):
    """E2E: Ensure 'status' command shows running database container."""
    result = subprocess.run(
        ["uv", "run", "python", "manage.py", "docker_compose", "status"],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout
    assert "postgres_db" in output
    assert "Up" in output


def test_down_stops_services(compose_services):
    """E2E: Ensure 'down' command stops and removes the database container."""
    # Stop services
    subprocess.run(
        ["uv", "run", "python", "manage.py", "docker_compose", "down"], check=True
    )
    # Ensure container is no longer running
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=postgres_db", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == ""
