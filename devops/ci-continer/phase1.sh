#!/bin/bash
#####  1) will do git clone inside test folder and will uplaoad a testing env'.
#####  2) will save the result in the file score.txt (OK=passes, ERROR = faild).
#####  3) will close all the test env' and delete the folder test.

# full paths
root_billing=/app/test/gan-shmuel-green/billing
root_weight=/app/test/gan-shmuel-green/weight
full_score_path_weight=/app/test/gan-shmuel-green/weight/tests/score.txt
full_score_path_billing=/app/test/gan-shmuel-green/billing/tests/score.txt

mkdir test 
cd test || { echo "'cd test' failed "; exit 1; }
git clone https://github.com/RachelNaane/gan-shmuel-green.git 
wait

# up env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }

echo -e "APP_PORT=8086\nDB_PORT=8087\nVOLUME=weight-test-volume" > .env
docker compose build -no-cache && docker compose up -d # -f for specifing compose file?
wait


cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }

echo -e "APP_PORT=8088\nDB_PORT=8089\nVOLUME=billing-test-volume" > .env
docker compose build -no-cache && docker compose up -d # -f for specifing compose file?
wait

# run test
bash $root_weight/tests/test.sh
exitcode_weight=$?
bash $root_billing/tests/test.sh
exitcode_billing=$?

# down env-testing
cd $root_weight || { echo "'cd $(root_weight)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }
docker compose down -v
wait

cd $root_billing || { echo "'cd $(root_billing)' the current path is $(pwd)" |tee $full_score_path_weight $full_score_path_billing ; exit 1; }
docker compose down -v
wait

# delete test dir
cd /app || { echo "'cd /app' failed"; exit 1; }
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

echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_weight
echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $full_score_path_billing