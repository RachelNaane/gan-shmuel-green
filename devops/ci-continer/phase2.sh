#!/bin/bash

root_billing=/app/gan-shmuel-green/billing
root_weight=/app/gan-shmuel-green/weight
full_score_path_weight=/app/gan-shmuel-green/weight/tests/score.txt
full_score_path_billing=/app/gan-shmuel-green/billing/tests/score.txt

billing_host_volume="/var/lib/docker/volumes/billing-prod-volume/_data"
weight_host_volume="/var/lib/docker/volumes/weight-prod-volume/_data"
billing_mysql_volume="/var/lib/mysql"
weight_mysql_volume="/var/lib/mysql"

# pulling main and replacing the production with a new version
cd /app/gan-shmuel-green || { echo "'cd /app/gan-shmuel-green' has failed"; exit 1; }
git pull origin main || { echo "pull from rep failed";exit 1; }

cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)"; exit 1; }
docker-compose down

echo -e "APP_PORT=8083\nDB_PORT=8084\nHOST_VOLUME=$billing_host_volume\nMYSQL_VOLUME=$billing_mysql_volume" > .env
docker-compose up -d || { echo "could not run billing containers"; exit 1; }
wait

cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)"; exit 1; }
docker-compose down

echo -e "APP_PORT=8081\nDB_PORT=8082\nHOST_VOLUME=$weight_host_volume\nMYSQL_VOLUME=$weight_mysql_volume" > .env
docker-compose up -d || { echo "could not run weight containers"; exit 1; }
wait

python3 mail.py