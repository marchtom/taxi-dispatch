# Taxi Dispatch System

This repository contains a simulation of a taxi dispatch system composed of two services:

- `dispatch` – a FastAPI service responsible for managing trip coordination and persistence.
- `taxi` – a minimal FastAPI service representing a single taxi that moves on a 100x100 grid.

## Requirements

- Docker with Docker Compose

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
    This will build the containers, wait for dependencies to become healthy, and start the services: PostgreSQL database, Dispatch and a single Taxi.

1. While dispatch service is running, you can access API documentation:
    `http://localhost:8080/docs`

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

## Stopping the Environment

1. To stop all containers and remove associated volumes:
    ```bash
    make down
    ```

## Tests

1. Run tests for all services:
    ```bash
    make tests
    ```

1. Run tests for an individual service:
    ```bash
    make tests-dispatch
    make tests-taxi
    ```
