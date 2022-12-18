#!/bin/bash

API_BASE_URL="3.9.66.97:8088"
touch score.txt

# /rates API

response=$(curl -o /dev/null -w "%{http_code}" -X GET -H "Content-Type: application/json" -d '{"filename":"rates.xlsx"}' $API_BASE_URL/rates)
RESPONSES+=("$response") 
if [[ $response == *"200"* ]]; then 
  echo "GET Request to /rates was successful." >> score.txt
else
   
  echo "GET Request to /rates failed." >> score.txt
fi

response=$(curl -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"filename":"rates.xlsx"}' $API_BASE_URL/rates)
RESPONSES+=("$response") 
if [[ $response == *"200"* ]]; then
  echo "POST Request to /rates was successful." >> score.txt
else 
  echo "POST Request to /rates failed." >> score.txt
fi

# /health API

response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/health")
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "GET Request to /health was successful." >> score.txt
else
  echo "GET Request to /health failed." >> score.txt
fi

# /provider API

response=$(curl -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"name":"New Provider"}' $API_BASE_URL/provider)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "POST Request to /provider was successful." >> score.txt
else
  echo "POST Request to /provider failed." >> score.txt
fi

response=$(curl -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d '{"name":"Updated Name"}' $API_BASE_URL/provider/10001)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "PUT Request to /provider was successful." >> score.txt
else
  echo "PUT Request to /provider failed." >> score.txt
fi

# /truck API

response=$(curl -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"id":"T-32129", "provider":10001}' $API_BASE_URL/truck)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "POST Request to /truck was successful." >> score.txt
else
  echo "POST Request to /truck failed." >> score.txt
fi

response=$(curl -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d '{"provider_id":10002}' $API_BASE_URL/truck/T-32123)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "PUT Request to /truck was successful." >> score.txt
else
  echo "PUT Request to /truck failed." >> score.txt
fi

# response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/truck/T-12345")
# RESPONSES+=("$response")

# if [[ $response == *"200"* ]]; then
#   echo "GET Request to /truck was successful." >> score.txt
# else
#   echo "GET Request to /truck failed." >> score.txt
# fi

# # /bill API

# response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL/bill/10002?from=20050404")
# RESPONSES+=("$response")

# if [[ $response == *"200"* ]]; then
#   echo "GET Request to /bill was successful." >> score.txt
# else
#   echo "GET Request to /bill failed." >> score.txt
# fi

for item in "${RESPONSES[@]}"; do
  if [[ $item == 200 ]]; then
    continue
  else
    echo "Test Failed"
    exit 1
  fi
done
