FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY alembic.ini ./
COPY alembic ./alembic
COPY src ./src

RUN pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "polymarket_advisor.api.app:app", "--host", "0.0.0.0", "--port", "8000"]