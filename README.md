# Polymarket Advisor

API FastAPI + Postgres (SQLAlchemy async + Alembic) pour signaux, actualités et recommandations advisor.

## Structure

- `src/polymarket_advisor/` — package principal
  - `core/` — config, logging, time, utils
  - `integrations/` — polymarket (Gamma/CLOB), news
  - `db/` — session, base, models, repos
  - `domain/` — scoring, advisor (rules, selector, composer)
  - `services/` — refresh (markets, prices, signals, news), advisor
  - `api/` — FastAPI app, router, deps, routes, schemas
  - `chat/` — orchestrator, prompts, explain
  - `scheduler/` — runner, state
  - `ml/` — features, modeling, backtesting

## Lancer en local

```bash
# Créer l’environnement
python -m venv .venv && source .venv/bin/activate  # ou Windows: .venv\Scripts\activate
pip install -e .

# Variables d’environnement
cp .env.example .env
# Éditer .env (DATABASE_URL, etc.)

# Migrations
alembic upgrade head

# Démarrer l’API
uvicorn polymarket_advisor.api.app:app --reload --host 0.0.0.0 --port 8000
```

## Migrations

```bash
# Créer une nouvelle révision
alembic revision --autogenerate -m "description"

# Appliquer
alembic upgrade head
```

## Tests

```bash
pytest
```

## Docker

```bash
docker-compose up -d
```

---

## Checklist après refactor

- **Lancer en local**  
  `cp .env.example .env` puis `uvicorn polymarket_advisor.api.app:app --reload --host 0.0.0.0 --port 8000`  
  (depuis la racine du repo avec `PYTHONPATH=src` si besoin, ou après `pip install -e .`.)

- **Migrations**  
  Avec Postgres démarré et `DATABASE_URL` dans `.env` :  
  `alembic revision --autogenerate -m "message"` puis `alembic upgrade head`.  
  Alembic utilise `polymarket_advisor.db.base.Base` et `polymarket_advisor.db.models` (voir `alembic/env.py`).

- **Tests**  
  `pytest` (depuis la racine, avec `PYTHONPATH=src` ou après `pip install -e .`).  
  Pour les tests complets des routes `/signals`, `/news`, `/advisor`, une base Postgres doit être disponible (ou les tests qui touchent à la DB peuvent échouer / être skippés).
