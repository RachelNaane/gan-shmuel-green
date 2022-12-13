#####  1) will do git clone inside test folder and will uplaoad a testing env'.
#####  2) will save the result in the file score.txt (OK=passes, ERROR = faild).
#####  3) will close all the test env' and delete the folder test.


mkdir test && cd test
git clone https://github.com/RachelNaane/gan-shmuel-green.git
wait
rm -f -r test