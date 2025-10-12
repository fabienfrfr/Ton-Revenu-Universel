# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO
# SPDX-FileContributor:    Henri  GEIST

PROGRAMS          := backend/app/main.py
PROGRAMS          += frontend/app.py
PROGRAMS          += tests/e2e/conftest.py
PROGRAMS          += tests/unit/steps/test_simulation.py

SHELL             := /bin/sh
DOCKER_COMPOSE    := docker compose
LICENCES_CHECKER  := reuse lint
PYTHON            := python
PYTEST            := pytest
MYPY              := mypy  --strict $(PROGRAMS)
PYLINT            := pylint   $(dir $(PROGRAMS))
YAMLLINT          := yamllint .
ISORT             := isort    .

.POSIX:
.SUFFIXES:
.DELETE_ON_ERROR:

all: check

start: .env
	$(DOCKER_COMPOSE) up -d --wait --wait-timeout 120
	$(DOCKER_COMPOSE) ps

stop:
	$(DOCKER_COMPOSE) down

restart:
	$(MAKE) stop
	$(MAKE) start

status:
	$(DOCKER_COMPOSE) ps
logs:
	$(DOCKER_COMPOSE) logs -f

check: lint check_licenses

lint:
	-$(YAMLLINT)
	-$(ISORT)
	-$(PYLINT)
	-$(MYPY)

check_licenses:
	RESULT=$$($(LICENCES_CHECKER) 2>&1) || (printf "%s\n" "$$RESULT" >&2 && exit 1)

coverage:
	$(PYTEST) --cov=src --cov-report=term-missing

COMMIT_MESSAGE ?= "Merge dev into main"

merge-dev:
	git checkout main
	git merge --squash dev
	git commit -m $(COMMIT_MESSAGE)
	git push origin main
	git branch -D dev
	git checkout -b dev main
	git push origin dev --force

delete-ci-runs:
	@echo "Deleting all GitHub Actions runs from GitHub CLI..."
	gh run list --limit 1000 --json databaseId -q '.[].databaseId' | xargs -n 1 gh run delete

.PHONY: lint check check_licenses build start stop restart logs coverage merge-dev delete-ci-runs

.env:
	echo "DB_NAME     = simulator"                   >  $@
	echo "DB_USER     = simulator_user"              >> $@
	echo "DB_PASSWORD = $$(openssl rand -base64 32)" >> $@


extract/projet_complet.md: extract/project_extrator.py
	$(PYTHON) $<
