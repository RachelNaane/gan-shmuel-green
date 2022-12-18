#!/bin/bash
## phase2 of ci-test runs is tests where successfull - and runs new prod env.

#paths
root_billing="/app/gan-shmuel-green/billing"
root_weight="/app/gan-shmuel-green/weight"
billing_host_volume="/var/lib/docker/volumes/prod_prod_billing/_data"
weight_host_volume="/var/lib/docker/volumes/prod_prod_weight/_data"
billing_mysql_volume="/var/lib/mysql"
weight_mysql_volume="/var/lib/mysql"

# pulling main and replacing the production with a new version
cd /app/gan-shmuel-green || { echo "cd /app/gan-shmuel-green has failed">app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
git pull origin main || { echo "pull from rep failed">app/report.txt; curl localhost:5000/send_mail/report; exit 1; }

#weight down&up
cd $root_weight || { echo "cd to $root_weight failed">app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
docker-compose -p prod down

echo -e "APP_PORT=8081\nDB_PORT=8082\nHOST_VOLUME=$weight_host_volume\nMYSQL_VOLUME=$weight_mysql_volume\nNETWORK=production-net" > .env
docker-compose build --no-cache 
docker-compose -p prod up -d || { echo "could not run weight prod containers!!!!"; exit 1; }
wait

#billing down&up
cd $root_billing || { echo "cd to $root_billing failed">app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
docker-compose -p prod down

echo -e "APP_PORT=8083\nDB_PORT=8084\nHOST_VOLUME=$billing_host_volume\nMYSQL_VOLUME=$billing_mysql_volume\nNETWORK=production-net" > .env
docker-compose build --no-cache 
docker-compose -p prod up -d || { echo "could not run billing prod containers!!!!">app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
wait