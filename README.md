# Vector-search task

A simple vector search task implementation using
Weaviate vector database with pre-built model for vector embedding.

# How to run

## Prerequisites

docker and docker-compose

## How to setup and run

```bash
docker-compose up --build
```

Note: The first time you run the service, it will take some time to populate the database.

## How to destroy

```bash
docker-compose down
```

# How to use

The service will be available at http://0.0.0.0:8000.
OpenAPI documentation is available at http://0.0.0.0:8000/docs.

This API contains /query endpoint which can be used to search for similar items in the database.
It has the following parameters:
- q: query string for vector search
- filters: list of phrases to filter the results (exactly match)

Example:
```sh
curl -X 'GET' \
  'http://0.0.0.0:8000/query?q=smart%20computer&filters=python&limit=10&offset=0' \
  -H 'accept: application/json'
```