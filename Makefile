# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO
# SPDX-FileContributor:    Henri  GEIST

SHELL             := /bin/sh
LICENCES_CHECKER  := reuse lint
PYTHON            := python
PYTEST            := pytest

.POSIX:
.SUFFIXES:
.DELETE_ON_ERROR:

all: check

check: lint check_licenses

lint:
	isort src/ tests/
	$(PYTHON) -m pylint src/ tests/

check_licenses:
	$(LICENCES_CHECKER)

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

.PHONY: install lint coverage merge-dev delete-ci-runs

extract/projet_complet.md: extract/project_extrator.py
	$(PYTHON) $<
