#/bin/bash
#####  1) will do git clone inside test folder and will uplaoad a testing env'.
#####  2) will save the result in the file score.txt (OK=passes, ERROR = faild).
#####  3) will close all the test env' and delete the folder test.

root_billing=/home/ubuntu/gan-shmuel-green/billing
root_weight=/home/ubuntu/gan-shmuel-green/weight
root_devops=/home/ubuntu/gan-shmuel-green/devops/ci-continer

mkdir test && cd test
git clone https://github.com/RachelNaane/gan-shmuel-green.git 
wait

#up env-testing
cd $root_weight
export APP_PORT=8086
export DB_PORT=8087
docker compose build -no-cache && docker compose up -d # add network envs
wait

cd $root_billing
export APP_PORT=8088
export DB_PORT=8089
docker compose build -no-cache && docker compose up -d # add network envs 
wait

#run test
bash $root_weight/tests/test.sh > score.txt
exitcode_weight=$?
bash $root_billing/tests/test.sh > score.txt
exitcode_billing=$?

#down env-testing
cd $root_weight
docker compose down -v
wait

cd $root_billing
docker compose down -v
wait

#deleate test dir
cd $root_devops
rm -fr test

# add conclusion message to report
message="CI RESULT: "
billing_result="billing test-failure"
weight_result="weight test-failure"
conclusion="cant run this version in production. please fix bugs"

if [ $exitcode_billing -eq 0 ]; then billing_result="billing test-success"; fi
if [ $exitcode_billing -eq 0 ]; then weight_result="weight test-success"; fi
if [ $exitcode_billing -eq 0 ] && [ $exitcode_weight -eq 0 ]; then
    #run new version on production!
    phase2.sh
    conclusion="new version up in production. good work everyone!"
fi

echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $root_billing/score.txt
echo -e "\n\n$message \n$billing_result \n$weight_result \n$conclusion" >> $root_weight/score.txt