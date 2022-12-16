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
cd test || { echo "'cd test' failed "; curl localhost:5000/send_mail; exit 1;}
git clone https://github.com/RachelNaane/gan-shmuel-green.git || { echo "clone from rep failed"; curl localhost:5000/send_mail; exit 1;}
wait

# up env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)"; curl localhost:5000/send_mail; exit 1;}

echo -e "APP_PORT=8086\nDB_PORT=8087\nHOST_VOLUME=$weight_host_volume\nMYSQL_VOLUME=$weight_mysql_volume\nNETWORK=test-net" > .env
docker-compose build --no-cache || { echo "could not build the image for weight"; curl localhost:5000/send_mail; exit 1; }
wait
docker-compose -p test up -d || { echo "could not run the dockers for weight "; curl localhost:5000/send_mail; exit 1;}
wait


cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; curl localhost:5000/send_mail; exit 1;}

echo -e "APP_PORT=8088\nDB_PORT=8089\nHOST_VOLUME=$billing_host_volume\nMYSQL_VOLUME=$billing_mysql_volume\nNETWORK=test-net"> .env
docker-compose build --no-cache || { echo "could not build the image for weight"; curl localhost:5000/send_mail; exit 1; }
wait 
docker-compose -p test up -d || { echo "could not run the dockers for weight "; curl localhost:5000/send_mail; exit 1;}
wait

# run test
bash $root_weight/tests/test.sh
exitcode_weight=$?
bash $root_billing/tests/test.sh
exitcode_billing=$?

# down env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)"; curl localhost:5000/send_mail; exit 1;}
docker-compose -p test down
wait

cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)"; curl localhost:5000/send_mail; exit 1;}
docker-compose -p test down 
wait

# delete test dir
cd /app || { echo "'cd /app' failed"; curl localhost:5000/send_mail; exit 1;}


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

echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_weight || { echo "problem"; curl localhost:5000/send_mail; exit 1;}
echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_billing || { echo "problem"; curl localhost:5000/send_mail; exit 1;}

curl localhost:5000/send_mail
rm -r test
