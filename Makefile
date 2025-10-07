.PHONY: install lint coverage merge-dev

lint:
	isort src/ tests/
	python -m pylint src/ tests/

coverage:
	pytest --cov=src --cov-report=term-missing

COMMIT_MESSAGE ?= "Merge dev into main"

merge-dev:
	git checkout main
	git merge --squash dev
	git commit -m $(COMMIT_MESSAGE)
	git push origin main
	git branch -D dev
	git checkout -b dev main
	git push origin dev --force