# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO
# SPDX-FileContributor:    Henri  GEIST

PROGRAMS             := backend/app/main.py
PROGRAMS             += frontend/app.py
PROGRAMS             += tests/e2e/conftest.py
PROGRAMS             += tests/unit/steps/test_simulation.py

VENV_DIR             := .venv
REQUIERMENTS         := $(addsuffix /requirements.txt, . frontend backend tests)

SHELL                := /bin/sh
DOCKER_NETWORK       := docker network
DOCKER_COMPOSE       := docker compose -f docker-compose.yml
DOCKER_START_OPTIONS := --detach --wait --wait-timeout 120
LICENCES_CHECKER     := reuse lint
PIP                  := pip3
PYTHON               := python3
ACTIVATE_VENV        := . $(VENV_DIR)/bin/activate
PYTEST               := pytest
MYPY                 := mypy  --strict $(PROGRAMS)
PYLINT               := pylint   $(dir $(PROGRAMS))
YAMLLINT             := yamllint .
ISORT                := isort    .

NORMAL_CODE          := \033[0m
BOLD_CODE            := \033[1m
CYAN_CODE            := \033[36m

include .env

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
	      /^[-a-z_%]*:/ { printf "  $(CYAN_CODE)%-25s$(NORMAL_CODE)%s\n",     \
	                             $$1, COMMENT;                                \
	                     COMMENT = ""; }' $(MAKEFILE_LIST)

##@ Show containers status
status:
	$(DOCKER_COMPOSE) ps

##@ Build / rebuild the containers
build: .env check_precommit_hook
	$(DOCKER_NETWORK) create $(TRAEFIK_NETWORK_NAME) 2> /dev/null || true
	$(DOCKER_COMPOSE) -f docker-compose.tests.yml build

##@ Start all containers of the project
start: .env build
	$(DOCKER_COMPOSE) up $(DOCKER_START_OPTIONS)
	$(DOCKER_COMPOSE) ps

##@ Stop all containers of the project
stop:
	$(DOCKER_COMPOSE) -f docker-compose.tests.yml down

##@ Restart all containers of the project
restart:
	$(MAKE) stop
	$(MAKE) start

##@ Show logs from all containers (hit Ctrl-C to quit).
logs:
	$(DOCKER_COMPOSE) -f docker-compose.tests.yml logs -f

##@ To get all new commits auto checked before validation.
install-pre-commit-hook: pre-commit.hook
	install pre-commit.hook .git/hooks/pre-commit

##@ Generaite PDF and HTML version of the documentation.
doc:
	$(MAKE) -C specs

## Tests

##@ Start in tests mode
test_mode_start: .env build
	$(DOCKER_COMPOSE) -f docker-compose.tests.yml up $(DOCKER_START_OPTIONS)
	$(DOCKER_COMPOSE) ps

##@ Run all automatic checks
check: lint check_licenses check_precommit_hook
	$(MAKE) -C tests

##@ Run only linters checks
lint: venv
	$(YAMLLINT)
	-$(ISORT)
	-$(ACTIVATE_VENV) && $(PYLINT)
	-$(ACTIVATE_VENV) && $(MYPY)

##@ Run only licences & copyrights checks
check_licenses:
	RESULT=$$($(LICENCES_CHECKER) 2>&1) || (printf "%s\n" "$$RESULT" >&2 && exit 1)

##@ Install a pre-commit-hook to validate each commits by autotests
check_precommit_hook:
	[ -e .git ] && (diff --brief .git/hooks/pre-commit pre-commit.hook || echo "Please run 'make install-pre-commit-hook' to update it" >&2)

##@ Run coverages checks
coverage:
	$(PYTEST) --cov=src --cov-report=term-missing

COMMIT_MESSAGE ?= "Merge dev into main"

##@ Clean builds arthefacts
clean:
	$(MAKE) -C specs clean

##@ Create Python virtual environnement
venv: $(VENV_DIR)/is_up_to_date

$(VENV_DIR)/is_up_to_date: $(REQUIERMENTS) $(VENV_DIR)/pyvenv.cfg
	$(ACTIVATE_VENV) && $(PIP) install --quiet $(addprefix -r , $(REQUIERMENTS))
	touch $@

$(VENV_DIR)/pyvenv.cfg: $(MAKEFILE_LIST)
	$(PYTHON) -m venv $(VENV_DIR)


## Strange and brutal things I would not recommend (Don't use it if collaborative works)

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

.PHONY: status build start stop restart logs test_mode_start install-pre-commit-hook
.PHONY: venv lint check check_licenses check_precommit_hook coverage doc clean
.PHONY: merge-dev delete-ci-runs

.env:
	echo "INSTANCE_NAME        = $$USER"                                >  $@
	echo "DOMAIN_NAME          = simulateur.$$USER"                     >> $@
	echo "TRAEFIK_NETWORK_NAME = traefik"                               >> $@
	echo "DB_NAME              = simulator"                             >> $@
	echo "DB_USER              = simulator_user"                        >> $@
	echo "DB_PASSWORD          = $$(openssl rand -base64 32)"           >> $@
	echo ""                                                             >> $@
	echo "# Only for tests mode. (started with 'make test_mode_start')" >> $@
	echo "# 127.0.0.1:ports for local test access only."                >> $@
	echo "# No host part for testing from a remote host."               >> $@
	echo "# for the ports number on localhost any free ones will do"    >> $@
	echo "# for extern access see with your firewall admin"             >> $@
	echo "BACKEND_LISTEN_ON    = 127.0.0.1:8000"                        >> $@
	echo "FRONTEND_LISTEN_ON   = 127.0.0.1:8501"                        >> $@


extract/projet_complet.md: extract/project_extrator.py
	$(PYTHON) $<

##@ Simple echo command

ECHO_MESSAGE ?= "Hello World!"

echo:
	# make echo ECHO_MESSAGE="Votre message personnalisé"
	echo $(ECHO_MESSAGE)
