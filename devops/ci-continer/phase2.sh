#!/bin/bash

root_billing=/home/ubuntu/gan-shmuel-green/billing
root_weight=/home/ubuntu/gan-shmuel-green/weight
#root_devops=/home/ubuntu/gan-shmuel-green/devops/ci-continer

cd $root_billing || { echo "cd failed"; exit 1; }
docker compose down

echo -e "APP_PORT=8083\nDB_PORT=8084\nVOLUME=billing-prod-volume" > .env
docker compose up -d
wait

cd $root_weight || { echo "cd failed"; exit 1; }
docker compose down

echo -e "APP_PORT=8081\nDB_PORT=8082\nVOLUME=weight-prod-volume" > .env
docker compose up -d
wait

# check to run docker compose through socket
