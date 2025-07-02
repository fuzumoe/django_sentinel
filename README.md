# Django Sentinel

A robust Django project with PostgreSQL, Docker Compose integration, and comprehensive development tooling.

## 🚀 Features

- **Django 5.2.3** - Latest Django framework
- **PostgreSQL** - Production-ready database with Docker Compose
- **uv** - Fast Python package manager and virtual environment
- **VS Code Integration** - Complete development environment setup
- **Docker Compose Management** - Unified Django management commands
- **Development Tooling** - Debugging, testing, and database management

## 📋 Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose
- VS Code (recommended)

## 🛠️ Quick Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd django_sentinel
./setup_project.sh
```

The setup script will:
- Install uv if not present
- Create and activate virtual environment
- Install all dependencies
- Set up environment variables
- Run initial migrations

### 2. Start Development Environment

```bash
# Start PostgreSQL database
uv run python manage.py docker_compose up

# Run Django development server
uv run python manage.py runserver
```

Or use VS Code launch configurations (press F5):
- **🐳 Docker Compose Up** - Start database
- **Django: Debug Server** - Start Django with debugging

## 🐳 Docker Compose Management

This project includes a unified Django management command for all Docker Compose operations.

### Available Commands

```bash
# Show help
uv run python manage.py docker_compose --help

# Start services (detached mode)
uv run python manage.py docker_compose up

# Start services with logs (attached mode)
uv run python manage.py docker_compose up --logs

# Stop services
uv run python manage.py docker_compose down

# Stop services and remove volumes
uv run python manage.py docker_compose down --volumes

# Restart services
uv run python manage.py docker_compose restart

# View logs (following by default)
uv run python manage.py docker_compose logs

# View logs for specific service
uv run python manage.py docker_compose logs db

# Check service status
uv run python manage.py docker_compose status
```

### VS Code Launch Configurations

Press `F5` or use Command Palette → "Debug: Select and Start Debugging":

- **🐳 Docker Compose Up** - Start services in detached mode
- **🐳 Docker Compose Up (with logs)** - Start services with log output
- **🛑 Docker Compose Down** - Stop all services
- **🔄 Docker Compose Restart** - Restart all services
- **📊 Docker Compose Status** - Check service status
- **📋 Docker Compose Logs** - View service logs

### VS Code Tasks

Press `Ctrl+Shift+P` / `Cmd+Shift+P` → "Tasks: Run Task":

- **Django: Run Server** - Start Django development server
- **Django: Make Migrations** - Create database migrations
- **Django: Migrate** - Apply database migrations
- **Django: Test** - Run test suite
- **Docker: Compose Up/Down/Restart** - Docker operations

## 🗄️ Database Configuration

### PostgreSQL via Docker

The project uses PostgreSQL running in Docker. Configure your environment variables:

```bash
# Create .env file from example
cp .env.example .env
```

Example `.env` configuration:
```env
# Database Configuration
POSTGRES_DB=auth_db
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_secret
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Services

The `docker-compose.yml` includes:
- **PostgreSQL 16** - Main database server
- **Persistent Volume** - Data persistence across container restarts
- **Port Mapping** - Accessible on localhost:5432

## 🔧 Development Workflow

### 1. Project Setup
```bash
./setup_project.sh  # One-time setup
```

### 2. Daily Development
```bash
# Start database
uv run python manage.py docker_compose up

# Create/apply migrations (if needed)
uv run python manage.py makemigrations
uv run python manage.py migrate

# Start development server
uv run python manage.py runserver
```

### 3. Using VS Code
1. Open project in VS Code
2. Extensions will be recommended automatically
3. Use F5 to start debugging configurations
4. Use Ctrl+Shift+P → "Tasks: Run Task" for common operations

## 🧪 Testing

```bash
# Run all tests
uv run python manage.py test

# Run with coverage (if installed)
uv run coverage run --source='.' manage.py test
uv run coverage report
```

Via VS Code:
- **Django: Test** launch configuration
- **Django: Test** task

## 📁 Project Structure

```
django_sentinel/
├── .vscode/                    # VS Code configuration
│   ├── extensions.json         # Recommended extensions
│   ├── launch.json             # Debug configurations
│   ├── settings.json           # Editor settings
│   └── tasks.json              # Task definitions
├── scripts/                    # Utility scripts
│   ├── setup_project.sh        # Setup automation
│   ├── ruff.sh                 # Ruff CLI wrapper
│   └── mypy.sh                 # MyPy CLI wrapper
├── pydj_auth/                  # Main Django application
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── docker_compose.py  # Unified Docker Compose management command
│   ├── migrations/             # Database migrations
│   │   └── 0001_initial.py
│   ├── models/                 # Django models
│   │   └── auth.py
│   └── tests/                  # Unit and E2E tests
│       ├── conftest.py
│       ├── unit/
│       │   ├── test_docker_compose_py_unit.py
│       │   └── test_docker_compose_unit.py
│       └── e2e/
│           └── test_docker_compose_e2e.py
├── .pylintrc                   # Pylint configuration
├── .pre-commit-config.yaml     # Pre-commit hooks configuration 
├── docker-compose.yml          # Docker service definitions
├── Dockerfile                  # Docker image build configuration
├── main.py                     # Entry point (if used)
├── manage.py                   # Django management utility
├── pyproject.toml              # Project dependencies and settings (uv)
├── requirements.txt            # Pip fallback requirements
├── ruff.toml                   # Ruff configuration
├── mypy.ini                    # MyPy configuration
├── uv.lock                     # uv lockfile
├── .env                        # Environment variables (from .env.example)
└── README.md                   # Project documentation
```

## 🔌 VS Code Extensions

The project includes recommended extensions for optimal development:

### Core Development
- **Python** - Python language support
- **Python Debugger** - Debugging capabilities
- **Django** - Django-specific features

### Database & Docker
- **PostgreSQL** - Database management
- **Docker** - Container management
- **YAML** - Docker Compose file support

### Productivity
- **Error Lens** - Inline error display
- **TODO Highlight** - Task management

## 🛠️ Pre-commit Hooks

We use `pre-commit` to enforce code quality and catch issues early. Hooks run automatically before each commit:
- **ruff-fix**: Automatic linting and fixes via Ruff
- **ruff-format**: Code formatting via Ruff
- **mypy**: Static type checking via MyPy
- **pytest-all**: Run all tests in `pydj_auth/tests` with verbose output

Install and run manually:
```bash
pre-commit install
pre-commit run --all-files
```

## 🚀 VS Code Launch Configurations

The `.vscode/launch.json` includes debugger launchers for:
- **Django: Debug Server** – Run the development server with debugging
- **Debug All Tests** – Run pytest on all tests (unit and E2E)
- **Debug Unit Tests** – Run pytest on `pydj_auth/tests/unit`
- **Debug E2E Tests** – Run pytest on `pydj_auth/tests/e2e`
- **Docker Compose Up/Down/Restart** – Manage services via the `docker_compose` command

Use **F5** or select from the Run and Debug panel in VS Code to start any configuration.

## 🔑 Key Features

### 1. Unified Docker Management
- Single Django command for all Docker operations
- Consistent interface across terminal, VS Code launches, and tasks
- Proper error handling and user feedback

### 2. Complete VS Code Integration
- Debug configurations for Django, testing, and Docker
- Task definitions for common operations
- Recommended extensions for full-stack development

### 3. Production-Ready Setup
- PostgreSQL database with proper configuration
- Environment variable management
- Docker containerization ready

### 4. Developer Experience
- Fast setup with automation scripts
- Comprehensive tooling integration
- Clear documentation and workflows

## 🚀 Deployment

The project is configured for easy deployment:

1. **Environment Variables** - Managed via `.env` files
2. **Docker Support** - Ready for containerized deployment
3. **Database Migrations** - Automated via Django
4. **Static Files** - Django configuration ready

 

 

---

## 🔧 Troubleshooting

### Common Issues

**Database Connection Issues:**
```bash
# Check if PostgreSQL is running
uv run python manage.py docker_compose status

# Restart database
uv run python manage.py docker_compose restart
```

**Migration Issues:**
```bash
# Reset migrations (development only)
uv run python manage.py migrate --fake-initial

# Create new migrations
uv run python manage.py makemigrations
```

**VS Code Issues:**
- Ensure Python interpreter is set to `.venv/bin/python`
- Reload window after extension installation
- Check that all recommended extensions are installed

### Support

For additional help:
1. Check the VS Code Output panel for error details
2. Use Django's built-in error pages in DEBUG mode
3. Check Docker logs: `uv run python manage.py docker_compose logs`

---

## 🙏 Thanks

Special thanks to the Unicode Consortium and Emojipedia contributors for the emoji icons used throughout this project:

- 🚀 **[Rocket](https://emojipedia.org/rocket)** (U+1F680) - Launch/Start operations
- 🐳 **[Whale](https://emojipedia.org/whale)** (U+1F433) - Docker operations
- 🛑 **[Stop Sign](https://emojipedia.org/stop-sign)** (U+1F6D1) - Stop/Down operations
- 🔄 **[Counterclockwise Arrows](https://emojipedia.org/counterclockwise-arrows-button)** (U+1F504) - Restart operations
- 📊 **[Bar Chart](https://emojipedia.org/bar-chart)** (U+1F4CA) - Status/Monitoring
- 📋 **[Clipboard](https://emojipedia.org/clipboard)** (U+1F4CB) - Logs/Documentation
- 🧪 **[Test Tube](https://emojipedia.org/test-tube)** (U+1F9EA) - Testing operations
- 🐍 **[Snake](https://emojipedia.org/snake)** (U+1F40D) - Python/Django shell
- 🗄️ **[File Cabinet](https://emojipedia.org/file-cabinet)** (U+1F5C4) - Database operations
- 🔧 **[Wrench](https://emojipedia.org/wrench)** (U+1F527) - Configuration/Setup
- 🔌 **[Electric Plug](https://emojipedia.org/electric-plug)** (U+1F50C) - Extensions/Plugins
- � **[Key](https://emojipedia.org/key)** (U+1F511) - Key Features
- 🤝 **[Handshake](https://emojipedia.org/handshake)** (U+1F91D) - Contributing
- � **[Memo](https://emojipedia.org/memo)** (U+1F4DD) - Documentation
- � **[Folded Hands](https://emojipedia.org/folded-hands)** (U+1F64F) - Acknowledgments

*Emoji icons sourced from [Unicode Emoji Standards](https://unicode.org/emoji/) and displayed via system fonts.*

---

**Happy Coding! 🚀**
