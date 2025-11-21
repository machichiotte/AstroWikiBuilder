.PHONY: help install test lint format clean check

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances de développement
	pip install -e .[dev]
	pip install pre-commit
	pre-commit install

test: ## Lance les tests unitaires et d'intégration
	pytest

cov: ## Lance les tests avec rapport de couverture
	pytest --cov=src --cov-report=term-missing --cov-report=html

lint: ## Vérifie le style du code (Ruff, Black, MyPy)
	ruff check .
	black --check .
	mypy src

format: ## Formate le code automatiquement
	ruff check --fix .
	black .

clean: ## Nettoie les fichiers temporaires
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

check: lint test ## Lance lint et tests (pour CI)

run: ## Lance le pipeline principal (mode mock par défaut)
	python -m src.core.main --use-mock nasa_exoplanet_archive --skip-wikipedia-check
