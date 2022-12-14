#!/bin/bash

value=$(cat exitcode.txt)
echo "$value"

if [ $(($value)) -eq 0 ]
then
    # remove last working production
    cd ~/gan-shmuel-green
    cd billing && docker compose down -v
    wait
    cd -
    cd weight && docker compose down -v
    wait
    cd -
    # pulling and uploading the new production
    git pull origin main
    wait
    cd billing && docker compose up # add port and netwok envs
    wait
    cd -
    cd weight && docker compose up # add port and netwok envs
    wait
    cd -
fi
# check to run docker compose through socket
