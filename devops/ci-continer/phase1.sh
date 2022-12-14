#####  1) will do git clone inside test folder and will uplaoad a testing env'.
#####  2) will save the result in the file score.txt (OK=passes, ERROR = faild).
#####  3) will close all the test env' and delete the folder test.

mkdir test && cd test
git clone https://github.com/RachelNaane/gan-shmuel-green.git
wait
cd gan-shmuel-green 
cd billing && docker compose build -no-cache && docker compose up # add port and network envs 
wait
cd -
cd weight && docker compose build -no-cache && docker compose up # add port and network envs
wait
cd -
bash billing/test/test.sh
exitcode_billing=$?
bash weight/test/test.sh
exitcode_weight=$?

cd ~/
rm -f -r test
# to add the if from phase2 to here
if [ $(($exitcode_billing)) -eq 0 ] && [ $(($exitcode_billing)) -eq 0 ]
then
#run script phase2
#echo "message">> billing/score.txt
#echo "message">> weight/score.txt
else
#echo "message">> score.txt
fi




