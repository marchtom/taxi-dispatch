include .env
export

.DEFAULT_GOAL := help

# Text colors and styles
COLOR_DEFAULT := \033[0m
BOLD_TEXT := \033[1m
COLOR_RED := \033[31m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m

DOCKER_COMPOSE := docker compose -f docker-compose.yml

##############################
### HELP
##############################

help: ## Display available commands
	@printf "$(COLOR_YELLOW)$(BOLD_TEXT)Available make commands:\n$(COLOR_DEFAULT)"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//' \
	| awk 'BEGIN {FS = ":"}; {printf "$(COLOR_GREEN)%-20s$(COLOR_DEFAULT)%s\n", $$1, $$2}'
.PHONY: help

##############################
### ENVIRONMENT / NETWORK
##############################

init: ## Initialize required Docker network
	@docker network create $(DOCKER_NETWORK)
.PHONY: init

status: ## Check status of Docker network
	@docker network ls --format '{{.Name}}' | grep -q "^$(DOCKER_NETWORK)$$" \
		&& echo "$(COLOR_GREEN)[O]$(COLOR_DEFAULT) Network '$(DOCKER_NETWORK)' exists" \
		|| echo "$(COLOR_RED)[X]$(COLOR_DEFAULT) Network '$(DOCKER_NETWORK)' does not exist. Run $(COLOR_GREEN)make init$(COLOR_DEFAULT)"
.PHONY: status

up: ## Start development environment using Docker Compose
	@printf "$(COLOR_GREEN)\nStarting development environment$(COLOR_DEFAULT)\n\n"
	$(DOCKER_COMPOSE) up --build
.PHONY: up
 
down: ## Stop development environment, remove orphans and volumes
	@printf "$(COLOR_GREEN)\nStopping development environment$(COLOR_DEFAULT)\n\n"
	$(DOCKER_COMPOSE) down --remove-orphans --volumes
.PHONY: down

##############################
### BUILD
##############################

build: ## Build all images
	@$(MAKE) build-dispatch build-taxi
.PHONY: build

build-dispatch: ## Build Dispatch image
	docker build -t dispatch ./dispatch
.PHONY: build-dispatch

build-taxi: ## Build Taxi image
	docker build -t taxi ./taxi
.PHONY: build-taxi

##############################
### TESTS AND LINTING
##############################

test: ## Run all tests (Dispatch + Taxi)
	@printf "$(COLOR_GREEN)\nRunning tests for DISPATCH$(COLOR_DEFAULT)\n\n"
	@$(DOCKER_COMPOSE) run --rm --build dispatch poetry --quiet run pytest -x --cov=app --cov-report=term-missing
	@printf "$(COLOR_GREEN)\nRunning tests for TAXI$(COLOR_DEFAULT)\n\n"
	@$(DOCKER_COMPOSE) run --rm --build taxi poetry --quiet run pytest -x --cov=app --cov-report=term-missing
.PHONY: test

test-dispatch: ## Run Dispatch tests
	@$(DOCKER_COMPOSE) run --rm --build dispatch poetry --quiet run pytest -x -v --cov=app --cov-report=term-missing
.PHONY: test-dispatch

test-taxi: ## Run Taxi tests
	@$(DOCKER_COMPOSE) run --rm --build taxi poetry --quiet run pytest -x -v --cov=app --cov-report=term-missing
.PHONY: test-taxi

lint: lint-dispatch lint-taxi ## Run ruff for both Dispatch and Taxi
.PHONY: lint

lint-dispatch: ## Run ruff linter for Dispatch
	@$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run ruff check app
.PHONY: lint-dispatch

lint-taxi: ## Run ruff linter for Taxi
	@$(DOCKER_COMPOSE) run --rm taxi poetry --quiet run ruff check app
.PHONY: lint-taxi

typecheck: typecheck-dispatch typecheck-taxi ## Run mypy for both Dispatch and Taxi
.PHONY: typecheck

typecheck-dispatch: ## Run mypy type check for Dispatch
	@$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run mypy app
.PHONY: typecheck-dispatch

typecheck-taxi: ## Run mypy type check for Taxi
	@$(DOCKER_COMPOSE) run --rm taxi poetry --quiet run mypy app
.PHONY: typecheck-taxi

##############################
### DATABASE / MIGRATIONS
##############################

migrate: ## Run database migrations
	@$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run alembic upgrade head
.PHONY: migrate

create-migration: ## Create database migration
	@read -p "Specify migration message (-m) " msg; \
	read -p "New Revision ID (--rev-id) " id; \
	$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run alembic revision --autogenerate -m "$$msg" --rev-id "$$id"
.PHONY: create-migration

##############################
### TAXI MANAGEMENT
##############################

add-taxi: ## Start a single Taxi container
	docker run --rm \
		--network $(DOCKER_NETWORK) \
		-e DISPATCH_URL=http://dispatch:8080 \
		--name taxi-$(shell uuidgen | cut -c1-8) \
		taxi:latest
.PHONY: add-taxi

add-taxi-d: ## Start a single Taxi container (detached)
	@printf "$(COLOR_GREEN)\nStarting new TAXI container (detached)$(COLOR_DEFAULT)\n\n"
	@docker run --rm -d \
		--network $(DOCKER_NETWORK) \
		-e DISPATCH_URL=http://dispatch:8080 \
		--name taxi-$(shell uuidgen | cut -c1-8) \
		taxi:latest
.PHONY: add-taxi-d

add-taxis: ## Start multiple detached Taxi containers
	@read -p "How many TAXI containers do you want to start? " count; \
	for i in $$(seq 1 $$count); do \
		name=taxi-$$(uuidgen | cut -c1-8); \
		echo "Starting $$name..."; \
		docker run --rm -d \
			--network $(DOCKER_NETWORK) \
			-e DISPATCH_URL=http://dispatch:8080 \
			--name $$name \
			taxi:latest; \
	done
.PHONY: add-taxis
