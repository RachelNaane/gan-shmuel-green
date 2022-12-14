#!/bin/bash

root_billing=/home/ubuntu/gan-shmuel-green/billing
root_weight=/home/ubuntu/gan-shmuel-green/weight
root_devops=/home/ubuntu/gan-shmuel-green/devops/ci-continer

cd $root_billing 
docker compose down
export APP_PORT=8083
export DB_PORT=8084

docker compose up -d
wait

cd $root_weight
docker compose down
export APP_PORT=8081
export DB_PORT=8082
docker compose up -d
wait

# check to run docker compose through socket
