#!/bin/bash
# Project setup script - initializes .venv and creates .env file

echo "🚀 Setting up Django Sentinel project..."

# Install uv CLI via the official installer
echo "🛠️ Checking for uv installation..."
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv CLI tool..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Ensure uv is in PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✅ uv installed successfully!"
else
    echo "✅ uv already installed!"
fi

# Create or recreate .venv
echo "📦 Creating Python virtual environment with uv..."
if [ -d ".venv" ]; then
    echo "🔧 Removing existing virtual environment..."
    rm -rf .venv
fi
uv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install requirements with uv
 
echo "⚠️  No requirements.txt found, using pyproject.toml..."
uv pip sync -- --dev
 

# Install additional dependencies with uv if needed
echo "📦 Ensuring core dependencies are installed..."
uv pip install --no-deps psycopg2-binary python-dotenv gunicorn

# Set up uv environment variables
export UV_PROJECT_ENVIRONMENT=.venv
VIRTUAL_ENV="$(pwd)/.venv"
export VIRTUAL_ENV
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Create .env file with PostgreSQL configuration
echo "📝 Creating .env file with database configuration..."
cat > .env << EOF
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_secret
POSTGRES_DB=auth_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django Configuration
DEBUG=True
SECRET_KEY=django-insecure-development-key-replace-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_SETTINGS_MODULE=pydj_auth.settings
EOF

 
echo "🔧 Initializing pre-commit hooks..."
pre-commit install

echo "✅ Project setup complete!"
echo "📋 Next steps:"
echo "   • Use: uv run python manage.py [command]"
echo "   • Or: uv add [package] to install packages"
echo "   • Database configured in .env file"
echo "   • Virtual environment activated"
