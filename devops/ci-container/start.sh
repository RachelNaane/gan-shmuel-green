#!/bin/bash
docker rm -f ci-container
docker compose build --no-cache 
docker exec -it ci-container  bash 
