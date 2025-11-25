.PHONY: help install test lint format clean check clean-data

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances de développement
	pip install -e .[dev]
	pip install pre-commit
	pre-commit install

test: ## Lance les tests unitaires et d'intégration
	poetry run pytest

cov: ## Lance les tests avec rapport de couverture
	poetry run pytest --cov=src --cov-report=term-missing --cov-report=html --cov-report=json

lint: ## Vérifie le style et la sécurité (Ruff, Bandit)
	poetry run ruff check .
	poetry run bandit -c pyproject.toml -r src/

audit: ## Audit de sécurité approfondi avec Bandit
	poetry run bandit -c pyproject.toml -r src/ -f screen

stats: ## Compte les lignes de code avec cloc
	@powershell -Command "if (Get-Command cloc -ErrorAction SilentlyContinue) { cloc src/ tests/ --exclude-dir=build,dist,venv,.mypy_cache } else { Write-Host 'cloc non trouvé. Redémarrez votre terminal ou installez avec: winget install AlDanial.Cloc' }"

complexity: ## Analyse la complexité cyclomatique avec Radon
	@echo "\n=== Complexité Cyclomatique (Radon) ==="
	poetry run radon cc src/ -a -nc
	@echo "\n=== Indice de Maintenabilité (Radon) ==="
	poetry run radon mi src/

format: ## Formate le code automatiquement
	poetry run ruff check --fix .
	poetry run ruff format .

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

check: lint test complexity ## Lance tout (CI complet)

clean-data: ## Nettoie les fichiers de données générées (consolidated, statistics)
	@echo "Nettoyage des données générées..."
	@if exist "data\generated\consolidated" rmdir /s /q "data\generated\consolidated"
	@echo "Données nettoyées."

run: clean-data ## Lance le pipeline principal (mode mock par défaut)
	poetry run python -m src.core.main --use-mock nasa_exoplanet_archive --skip-wikipedia-check

run-prod: clean-data ## Lance le pipeline principal en production (sans mock, skip Wikipedia check)
	poetry run python -m src.core.main --sources nasa_exoplanet_archive --skip-wikipedia-check

run-prod-full: clean-data ## Lance le pipeline principal en production complète (avec Wikipedia check)
	poetry run python -m src.core.main --sources nasa_exoplanet_archive
