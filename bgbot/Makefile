.PHONY: dev up down logs test setup deploy backup

dev:
docker compose -f infra/docker/docker-compose.yml up -d postgres redis
sleep 3
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000 &
PYTHONPATH=. celery -A worker.app.celery_app worker --loglevel=info &
cd frontend && npm run dev

up:
docker compose -f infra/docker/docker-compose.yml up -d --build

down:
docker compose -f infra/docker/docker-compose.yml down

logs:
docker compose -f infra/docker/docker-compose.yml logs -f

setup:
bash infra/scripts/setup.sh

deploy:
bash infra/scripts/deploy.sh

test:
PYTHONPATH=. pytest tests/ -v

backup:
bash infra/scripts/backup.sh
