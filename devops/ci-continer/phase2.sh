#!/bin/bash

root_billing=/home/ubuntu/gan-shmuel-green/billing
root_weight=/home/ubuntu/gan-shmuel-green/weight
root_devops=/home/ubuntu/gan-shmuel-green/devops/ci-continer

cd $root_billing 
docker compose down

echo -e "APP_PORT=8083\nDB_PORT=8084" > .env
docker compose up -d
wait

cd $root_weight
docker compose down

echo -e "APP_PORT=8081\nDB_PORT=8082" > .env
docker compose up -d
wait

# check to run docker compose through socket
