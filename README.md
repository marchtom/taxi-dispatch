# Taxi Dispatch System

This repository contains a simulation of a taxi dispatch system composed of two services:

- `dispatch` – a FastAPI service responsible for managing trip coordination and persistence.
- `taxi` – a minimal FastAPI service representing a single taxi that moves on a 100x100 grid.

## Requirements

- Docker with Docker Compose
- GNU Make

## Make
1. You can check available make commands:
    ```
    make
    ```

## Setup

1. Copy the example environment configuration:
    ```bash
    cp .env.example .env
    ```

1. Create the required Docker network:
    ```bash
    make init
    ```

1. Start services:
    ```bash
    make up
    ```
    This will build the containers, wait for dependencies to become healthy, and start the services: PostgreSQL database, Dispatch, a single Taxi and Traffic Generator.

1. While dispatch service is running, you can access API documentation:
    `http://localhost:8080/docs`

1. [Optional] You can check docker network status using:
    ```bash
    make status
    ```

### Adding a Taxi Container

1. You can manually add a taxi instance to the network:

    1. Foreground mode:
        ```bash
        make add-taxi
        ```

    1. Detached mode:
        ```bash
        make add-taxi-d
        ```

1. If you wish to start multiple detached taxi containers run:
    ```bash
    make add-taxis
    ```
    Terminal prompt will ask you to specify number of containers.

## Stopping the Environment

1. To stop all containers and remove associated volumes:
    ```bash
    make down
    ```

## Tests

1. Run tests for all services:
    ```bash
    make test
    ```

1. Run tests for an individual service:
    ```bash
    make test-dispatch
    make test-taxi
    ```

## Linting

1. Run linting for all services:
    ```bash
    make lint
    ```

1. Run linting for an individual service:
    ```bash
    make lint-dispatch
    make lint-taxi
    ```