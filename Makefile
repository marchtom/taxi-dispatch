include .env
export

.DEFAULT_GOAL:=help

# text colors and styles
COLOR_DEFAULT:=\033[0m
BOLD_TEXT:=\033[1m
COLOR_RED:=\033[31m
COLOR_GREEN:=\033[32m
COLOR_YELLOW:=\033[33m

# additional commands
DOCKER_COMPOSE := docker compose -f docker-compose.yml


help: ## Display available commands
	@printf "$(COLOR_YELLOW)$(BOLD_TEXT)Available make commands:\n$(COLOR_DEFAULT)"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//' \
	| awk 'BEGIN {FS = ":"}; {printf "$(COLOR_GREEN)%-20s$(COLOR_DEFAULT)%s\n", $$1, $$2}'
.PHONY: help

init: ## Initialize required components
	@docker network create $(DOCKER_NETWORK)
.PHONY: init

status: ## Checks status of required dependencies
	@docker network ls --format '{{.Name}}' | grep -q "^$(DOCKER_NETWORK)$$" \
		&& echo "$(COLOR_GREEN)[O]$(COLOR_DEFAULT) Network '$(DOCKER_NETWORK)' exists" \
		|| echo "$(COLOR_RED)[X]$(COLOR_DEFAULT) Network '$(DOCKER_NETWORK)' does not exist. Run $(COLOR_GREEN)make init$(COLOR_DEFAULT)"
.PHONY: status

up: ## Start development environment using docker compose
	@printf "$(COLOR_GREEN)\nStarting development environment$(COLOR_DEFAULT)\n\n"
	$(DOCKER_COMPOSE) up --build
.PHONY: up
 
down: ## Stop development environment, removes orphans and volumes
	@printf "$(COLOR_GREEN)\nStopping development environment$(COLOR_DEFAULT)\n\n"
	$(DOCKER_COMPOSE) down --remove-orphans --volumes
.PHONY: down

build: ## Build taxi and dispatch image
	@$(MAKE) build-dispatch build-taxi
.PHONY: build

build-dispatch: ## Build dispatch image
	docker build -t dispatch ./dispatch
.PHONY: build-dispatch

build-taxi: ## Build taxi image
	docker build -t taxi ./taxi
.PHONY: build-taxi

tests: ## Run all tests
	@printf "$(COLOR_GREEN)\nRunning tests for DISPATCH$(COLOR_DEFAULT)\n\n"
	@$(DOCKER_COMPOSE) run --rm --build dispatch poetry --quiet run pytest -x --cov=app --cov-report=term-missing
	@printf "$(COLOR_GREEN)\nRunning tests for TAXI$(COLOR_DEFAULT)\n\n"
	@$(DOCKER_COMPOSE) run --rm  --build taxi poetry --quiet run pytest -x --cov=app --cov-report=term-missing
.PHONY: test

tests-dispatch: ## Run dispatch tests
	@$(DOCKER_COMPOSE) run --rm --build dispatch poetry --quiet run pytest -x -v --cov=app --cov-report=term-missing
.PHONY: test-dispatch

tests-taxi: ## Run taxi tests
	@$(DOCKER_COMPOSE) run --rm --build taxi poetry --quiet run pytest -x -v --cov=app --cov-report=term-missing
.PHONY: test-taxi

migrate: ## Run database migration
	@$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run alembic upgrade head

create-migration: ## Autogenerate database migration
	@$(DOCKER_COMPOSE) run --rm dispatch poetry --quiet run alembic revision --autogenerate -m "$(m)" --rev-id "$(id)"

add-taxi: ## Start single taxi container
	docker run --rm \
		--network $(DOCKER_NETWORK) \
		-e DISPATCH_URL=http://dispatch:8080 \
		--name taxi-$(shell uuidgen | cut -c1-8) \
		taxi:latest
.PHONY: add-taxi

add-taxi-d: ## Start single detached taxi container
	@printf "$(COLOR_GREEN)\nStarting new TAXI container (detached)$(COLOR_DEFAULT)\n\n"
	@docker run --rm -d \
		--network $(DOCKER_NETWORK) \
		-e DISPATCH_URL=http://dispatch:8080 \
		--name taxi-$(shell uuidgen | cut -c1-8) \
		taxi:latest
.PHONY: add-taxi-d
