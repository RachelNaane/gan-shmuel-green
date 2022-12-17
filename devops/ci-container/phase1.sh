#!/bin/bash
#####  1) will do git clone inside test folder and will uplaoad a testing env'.
#####  2) will save the result in the file score.txt (OK=passes, ERROR = faild).
#####  3) will close all the test env' and delete the folder test.

# full paths
root_billing="/app/test/gan-shmuel-green/billing"
root_weight="/app/test/gan-shmuel-green/weight"
full_score_path_weight="/app/test/gan-shmuel-green/weight/tests/score.txt"
full_score_path_billing="/app/test/gan-shmuel-green/billing/tests/score.txt"

billing_host_volume="/var/lib/docker/volumes/billing-test-volume/_data"
weight_host_volume="/var/lib/docker/volumes/weight-test-volume/_data"
billing_mysql_volume="/docker-entrypoint-initdb.d"
weight_mysql_volume="/docker-entrypoint-initdb.d"

mkdir test 
cd test || { echo "cd to test failed">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}
git clone https://github.com/RachelNaane/gan-shmuel-green.git || { echo "clone from rep failed">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}
wait

# up env-testing
cd $root_weight || { echo "could not cd into $root_weight">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}

echo -e "APP_PORT=8086\nDB_PORT=8087\nHOST_VOLUME=$weight_host_volume\nMYSQL_VOLUME=$weight_mysql_volume\nNETWORK=test-net" > .env
docker-compose build --no-cache || { echo "could not build the image for weight">/app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
wait
docker-compose -p test up -d || { echo "could not run the dockers for weight">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}
wait


cd $root_billing || { echo "could not cd into $root_billing">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}

echo -e "APP_PORT=8088\nDB_PORT=8089\nHOST_VOLUME=$billing_host_volume\nMYSQL_VOLUME=$billing_mysql_volume\nNETWORK=test-net" > .env
docker-compose build --no-cache || { echo "could not build the image for weight">/app/report.txt; curl localhost:5000/send_mail/report; exit 1; }
wait 
docker-compose -p test up -d || { echo "could not run the dockers for weight">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}
wait


echo "waiting for last finishes"
sleep 15 

echo "start testing!!!!!!!"
# run test
cd $root_weight/tests
bash test.sh
exitcode_weight=$?
cd $root_billing/tests
bash test.sh
exitcode_billing=$?

# down env-testing
cd $root_weight
docker-compose -p test down
wait

cd $root_billing
docker-compose -p test down 
wait

cd /app

# add conclusion message to report
message="CI RESULT: "
billing_result="billing test-failure"
weight_result="weight test-failure"
conclusion="cant run this version in production. please fix bugs"

# checking exitcode 
if [ $exitcode_billing -eq 0 ]; then billing_result="billing test-success"; fi
if [ $exitcode_weight -eq 0 ]; then weight_result="weight test-success"; fi
if [ $exitcode_billing -eq 0 ] && [ $exitcode_weight -eq 0 ]; then
    # run new version on production!
    bash phase2.sh
    conclusion="new version up in production. good work everyone!"
fi

echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_weight || { echo "problem with adding ci result to score.txt">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}
echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_billing || { echo "problem with adding ci result to score.txt">/app/report.txt; curl localhost:5000/send_mail/report; exit 1;}


curl localhost:5000/send_mail/score

# delete test dir
rm -fr test
