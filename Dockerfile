FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./

COPY packages ./packages

RUN uv sync --frozen --no-cache

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000
EXPOSE 8501

CMD ["echo", "Please specify a command"]