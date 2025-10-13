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

NORMAL_CODE       := \033[0m
BOLD_CODE         := \033[1m
CYAN_CODE         := \033[36m

.POSIX:
.SUFFIXES:
.DELETE_ON_ERROR:

## General

##@ Display available commands
help:
	@awk 'BEGIN         { printf "\nUsage: ";                                  \
	                      printf "make $(CYAN_CODE)<target>$(NORMAL_CODE)\n"; \
	                      FS      = ":"}                                      \
	      /^##@/        { COMMENT = substr ($$0, 5); next };                  \
	      /^##/         { printf "\n$(BOLD_CODE)%s$(NORMAL_CODE)\n",          \
	                             substr ($$0, 4); }                           \
	      /^[-a-z_%]*:/ { printf "  $(CYAN_CODE)%-20s$(NORMAL_CODE)%s\n",     \
	                             $$1, COMMENT;                                \
	                     COMMENT = ""; }' $(MAKEFILE_LIST)

##@ Show containers status
status:
	$(DOCKER_COMPOSE) ps

##@ Start all containers of the project
start: .env
	$(DOCKER_COMPOSE) up -d --wait --wait-timeout 120
	$(DOCKER_COMPOSE) ps

##@ Stop all containers of the project
stop:
	$(DOCKER_COMPOSE) down

##@ Restart all containers of the project
restart:
	$(MAKE) stop
	$(MAKE) start

##@ Show logs from all containers (hit Ctrl-C to quit).
logs:
	$(DOCKER_COMPOSE) logs -f

## Auto tests

##@ Run all automatic checks
check: lint check_licenses

##@ Run only linters checks
lint:
	$(YAMLLINT)
	-$(ISORT)
	-$(PYLINT)
	-$(MYPY)

##@ Run only licences & copyrights checks
check_licenses:
	RESULT=$$($(LICENCES_CHECKER) 2>&1) || (printf "%s\n" "$$RESULT" >&2 && exit 1)

##@ Run coverages checks
coverage:
	$(PYTEST) --cov=src --cov-report=term-missing

COMMIT_MESSAGE ?= "Merge dev into main"

## Strange and brutal things I would not recommend

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

.PHONY: lint check check_licenses status start stop restart logs coverage merge-dev delete-ci-runs

.env:
	echo "FRONTEND_PORT = 8501"                        >  $@
	echo "DB_NAME       = simulator"                   >> $@
	echo "DB_USER       = simulator_user"              >> $@
	echo "DB_PASSWORD   = $$(openssl rand -base64 32)" >> $@


extract/projet_complet.md: extract/project_extrator.py
	$(PYTHON) $<
