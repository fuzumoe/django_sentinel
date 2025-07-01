FROM python:3.11-slim

# avoid .pyc files, unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# install system build tools
RUN apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# install uv itself
RUN pip install --upgrade pip uv

# copy only your lock & project spec
COPY pyproject.toml uv.lock /app/

# sync all deps (including dev – e.g. mypy) and export a requirements.txt
RUN uv export --format requirements-txt > requirements.txt

# copy the rest of your Django code
COPY . /app/

# install dependencies from the generated requirements.txt
RUN pip install -r requirements.txt

# at runtime use uv to run uvicorn to serve the ASGI app
CMD [ "uvicorn", "pydj_auth.asgi:application", "--host", "0.0.0.0", "--port", "8000"]