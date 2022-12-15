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
cd test || { echo "'cd test' failed "; python3 mail.py ;exit 1;}
git clone https://github.com/RachelNaane/gan-shmuel-green.git || { echo "clone from rep failed"; python3 mail.py ;exit 1;}
wait

# up env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)"; python3 mail.py ;exit 1;}

echo -e "APP_PORT=8086\nDB_PORT=8087\nHOST_VOLUME=$weight_host_volume\nMYSQL_VOLUME=$weight_mysql_volume\nNETWORK=production-net" > .env
docker-compose build --no-cache || { echo "could not build the image for weight"; exit 1; }
wait
docker-compose up -d || { echo "could not run the dockers for weight "; python3 mail.py ;exit 1;}
wait


cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; python3 mail.py ;exit 1;}

echo -e "APP_PORT=8088\nDB_PORT=8089\nHOST_VOLUME=$billing_host_volume\nMYSQL_VOLUME=$billing_mysql_volume\nNETWORK=production-net"> .env
docker-compose build --no-cache || { echo "could not build the image for weight"; exit 1; }
wait 
docker-compose up -d || { echo "could not run the dockers for weight "; python3 mail.py ;exit 1;}
wait

# run test
bash $root_weight/tests/test.sh || { echo "no test.sh file found for weight"; python3 mail.py ; exit 1;}
exitcode_weight=$?
bash $root_billing/tests/test.sh || { echo "no test.sh file found for billing"; python3 mail.py ;exit 1;}
exitcode_billing=$?

# down env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)"; python3 mail.py ;exit 1;}
docker-compose down -v
wait

cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)"; python3 mail.py ;exit 1;}
docker-compose down -v
wait

# delete test dir
cd /app || { echo "'cd /app' failed"; python3 mail.py ;exit 1;}
rm -fr test

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

echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_weight || { echo "problem"; python3 mail.py ;exit 1;}
echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_billing || { echo "problem"; python3 mail.py ;exit 1;}

python3 mail.py