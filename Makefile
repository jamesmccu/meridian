SHELL := /bin/bash

PYTHON ?= .venv/bin/python
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap test lint typecheck yaml compose trivy-fs trivy-config check

bootstrap:
	./scripts/bootstrap.sh

test:
	$(PYTHON) -m pytest tools/meridian-core/tests

lint:
	$(PYTHON) -m ruff check tools/meridian-core

typecheck:
	$(PYTHON) -m mypy tools/meridian-core/src

yaml:
	ruby -e 'require "yaml"; Dir["**/*.{yml,yaml}"].each { |f| YAML.load_file(f) }'

compose:
	docker compose -f onprem/docker-compose.yml config --quiet

trivy-fs:
	trivy fs --config security/trivy/trivy.yaml .

trivy-config:
	trivy config --config security/trivy/trivy.yaml .

check: test lint typecheck yaml compose
