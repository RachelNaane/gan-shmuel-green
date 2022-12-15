#!/bin/bash

root_billing=/app/gan-shmuel-green/billing
root_weight=/app/gan-shmuel-green/weight
full_score_path_weight=/app/gan-shmuel-green/weight/tests/score.txt
full_score_path_billing=/app/gan-shmuel-green/billing/tests/score.txt

# pulling main and replacing the production with a new version
cd /app/gan-shmuel-green || { echo "'cd /app/gan-shmuel-green' has failed";exit 1; }
git pull origin main

cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }
docker compose down

echo -e "APP_PORT=8083\nDB_PORT=8084\nVOLUME=billing-prod-volume" > .env
docker compose up -d
wait

cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }
docker compose down

echo -e "APP_PORT=8081\nDB_PORT=8082\nVOLUME=weight-prod-volume" > .env
docker compose up -d
wait

# check to run docker compose through socket
