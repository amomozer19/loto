# Makefile - Automação de Tarefas Comuns

.PHONY: help install test lint format clean run dev-run docker-build docker-up docker-down

# Variáveis
PYTHON := python
PIP := pip
ENV_FILE := .env
VENV := .venv

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instalar dependências"
	@echo "  make test          - Executar testes com cobertura"
	@echo "  make test-unit     - Executar testes unitários"
	@echo "  make test-int      - Executar testes de integração"
	@echo "  make lint          - Análise de código (lint)"
	@echo "  make format        - Formatar código (black, isort)"
	@echo "  make clean         - Limpar arquivos temporários"
	@echo "  make run           - Executar aplicação"
	@echo "  make dev-run       - Executar em modo desenvolvimento"
	@echo "  make docker-build  - Build da imagem Docker"
	@echo "  make docker-up     - Iniciar containers with docker-compose"
	@echo "  make docker-down   - Parar containers"
	@echo "  make db-migrate    - Executar migrações de banco"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r config/requirements.txt

install-dev: install
	$(PIP) install pytest pytest-flask pytest-cov
	$(PIP) install black isort flake8 pylint mypy
	$(PIP) install bandit safety semgrep
	$(PIP) install ipython jupyter

test:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

test-unit:
	pytest tests/ -v -m unit --cov=app --cov-report=term-missing

test-int:
	pytest tests/ -v -m integration --cov=app --cov-report=term-missing

test-fast:
	pytest tests/ -v -m "not slow" --cov=app

lint:
	flake8 app tests --max-line-length=120
	pylint app --exit-zero
	mypy app --ignore-missing-imports

format:
	black app tests --line-length=120
	isort app tests

format-check:
	black --check app tests
	isort --check-only app tests

security:
	bandit -r app -f json -o bandit-report.json
	safety check --json > safety-report.json

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name 'htmlcov' -delete
	find . -type f -name '.coverage' -delete
	find . -type d -name '.mypy_cache' -delete
	rm -rf build/ dist/ *.egg-info

run:
	FLASK_ENV=production $(PYTHON) run.py

dev-run:
	FLASK_ENV=development DEBUG=True $(PYTHON) run.py

docker-build:
	docker build -t loto:latest .

docker-build-dev:
	docker build -f Dockerfile.dev -t loto:dev .

docker-up:
	docker-compose up -d

docker-up-dev:
	docker-compose -f docker-compose.dev.yml up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f web

db-init:
	$(PYTHON) -c "from app import create_app; app = create_app(); app.app_context().push(); from flask_migrate import Migrate, init, migrate; Migrate(app, db); init()"

db-migrate:
	$(PYTHON) -c "from app import create_app; app = create_app(); from flask_migrate import Migrate, upgrade; Migrate(app, db); upgrade()"

requirements:
	$(PIP) freeze > config/requirements.txt

deps-check:
	pip list --outdated

deps-update:
	pip list --outdated --format=json | jq -r '.[] | .name' | xargs -n1 pip install -U

all: clean install lint test
