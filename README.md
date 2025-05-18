# Taxi Dispatch (POC version)
Dispatch service registers new taxies joining docker network. Taxies are able to uphold bi-directional communication.

## Quick setup

### Prerequisites
1. Docker with docker-compose
1. make

### Running the service
1. copy .env.example as .env
    ```bash
    cp .env.example .env
    ```
1. Create docker network:
    ```bash
    docker network create taxi_net
    ```
1. Start dispatch service with a single taxi using docker compose:
    ```bash
    docker compose up --build
    ```
1. (Optional) Add new taxies to the network using docker run
    1. Make sure taxi image is available:
        ```bash
        docker build -t taxi ./taxi
        ```
    1. Run new taxi container:  
        ```bash
        docker run --rm \  
            --network $(DOCKER_NETWORK) \  
            -e DISPATCH_URL=http://dispatch:8080 \  
            --name taxi-$(shell uuidgen | cut -c1-8) \  
            taxi:latest
        ```
1. Check available taxies by sending `GET` request to `localhost:8080/taxi`
