#!/bin/bash
# Project setup script - initializes .venv and creates .env file

echo "🚀 Setting up Django Sentinel project..."

# Create .venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found, skipping dependency installation"
fi

# Install additional dependencies with uv
echo "📦 Installing additional dependencies..."
uv add psycopg2-binary python-dotenv

# Set up uv environment variables
export UV_PROJECT_ENVIRONMENT=.venv
export VIRTUAL_ENV="$(pwd)/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Create .env file with PostgreSQL configuration
echo "📝 Creating .env file with database configuration..."
cat > .env << EOF
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_secret
POSTGRES_DB=auth_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EOF

echo "✅ Project setup complete!"
echo "📋 Next steps:"
echo "   • Use: uv run python manage.py [command]"
echo "   • Or: uv add [package] to install packages"
echo "   • Database configured in .env file"
echo "   • Virtual environment activated"
