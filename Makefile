SHELL := /bin/bash

PYTHON ?= .venv/bin/python
PIP ?= $(PYTHON) -m pip

.PHONY: bootstrap cli-help test lint typecheck yaml compose trivy-fs trivy-config check

bootstrap:
	./scripts/bootstrap.sh

cli-help:
	.venv/bin/meridian-detect --help

test:
	$(PYTHON) -m pytest tools/meridian-detect/tests

lint:
	$(PYTHON) -m ruff check tools/meridian-detect

typecheck:
	$(PYTHON) -m mypy tools/meridian-detect/src

yaml:
	ruby -e 'require "yaml"; Dir["**/*.{yml,yaml}"].each { |f| YAML.load_file(f) }'

compose:
	docker compose -f onprem/docker-compose.yml config --quiet

trivy-fs:
	trivy fs --config security/trivy/trivy.yaml .

trivy-config:
	trivy config --config security/trivy/trivy.yaml .

check: test lint typecheck yaml compose
