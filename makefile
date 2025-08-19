SHELL := /bin/bash

APP := app

.PHONY: help
help:
	@echo "Targets:"
	@echo "  build    - Build Docker image"
	@echo "  rebuild  - Rebuild image without cache"
	@echo "  run      - Run CLI in container (ex: make run CMD='hello')"
	@echo "  helpcli  - Show CLI help"
	@echo "  test     - Run pytest inside container"
	@echo "  lint     - Run ruff"
	@echo "  fmt      - Run black"
	@echo "  shell    - Open interactive shell in the container"
	@echo "  doctor   - Run environment/CLI checks"
	@echo "  logs     - Tail container logs (if running via compose up)"
	@echo "  clean    - Remove dangling images/layers"

.PHONY: build
build:
	docker compose build

.PHONY: rebuild
rebuild:
	docker compose build --no-cache

.PHONY: run
run:
	@[ -n "$(CMD)" ] || (echo "Usage: make run CMD='hello' or CMD='--help'"; exit 2)
	docker compose run --rm $(APP) $(CMD)

.PHONY: helpcli
helpcli:
	docker compose run --rm $(APP) --help

.PHONY: test
test:
	docker compose run --rm --entrypoint pytest app -q

.PHONY: lint
lint:
	docker compose run --rm --entrypoint ruff app check .

.PHONY: fmt
fmt:
	docker compose run --rm --entrypoint black app .

.PHONY: shell
shell:
	docker compose run --rm --entrypoint sh $(APP)

.PHONY: doctor
doctor:
	./scripts/doctor.sh

.PHONY: logs
logs:
	docker compose logs -f $(APP)

.PHONY: clean
clean:
	docker image prune -f