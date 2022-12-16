#!bin/bash
docker rm -f ci-container
docker compose build --no-cashe
docker exec -it ci-container  bash 
