#!/bin/bash

# Set the base URL of your Flask API
API_BASE_URL="http://localhost:8081"


# Declare an empty array to store the responses from the requests
declare -a RESPONSES

# clear file
> tests/score.txt

# Define an array of the endpoints to test
ENDPOINTS=( "/health" "/weight" "/unknown" )

# Iterate over the array of endpoints
for endpoint in "${ENDPOINTS[@]}"; do
  # Make a request to the endpoint and save the response
  response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL$endpoint")
  RESPONSES+=("$response")
  # Check the status code of the response
  if [[ $response == *"200"* ]]; then
    # If the status code is 200, echo that the request was successful
    echo "Request to $endpoint was successful." >> tests/score.txt
  else
    # Otherwise, echo that the request failed
    echo "Request to $endpoint failed." >> tests/score.txt
  fi
  
done

if [[ ${RESPONSES[@]} =~ "200" ]]; then
  # If all the responses are 200, return 0
  echo "worked!"
  exit 0 
else
  # Otherwise, return 1
  exit 1
fi
