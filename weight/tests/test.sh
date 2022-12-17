#!/bin/bash

# Set the base URL of your Flask API
API_BASE_URL="3.9.66.97:8086"
# API_BASE_URL="localhost:5000"


# Declare an empty array to store the responses from the requests
declare -a RESPONSES

# Clear file
echo "Starting Tests" > score.txt

# Define an array of the endpoints to test
ENDPOINTS=( "/health" "/weight?t1=200104041" "/unknown" "/session/22324" "/item/C-00124?t1=20010404" )

# Iterate over the array of endpoints
for endpoint in "${ENDPOINTS[@]}"; do
  # Make a request to the endpoint and save the response
  response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL$endpoint")
  RESPONSES+=("$response")
  # Check the status code of the response
  if [[ $response == *"200"* ]]; then
    # If the status code is 200, echo that the request was successful
    echo "Request to $endpoint was successful." >> score.txt
  else
    # Otherwise, echo that the request failed
    echo "Request to $endpoint failed." >> score.txt
  fi
  
done

bash postweighttest.sh
if [ $? -eq 0 ]; then
  echo "post/weight ran successfully"
else
  echo "post/weight failed"
  exit 1
fi

# Check if all items in the array equal 200
for item in "${RESPONSES[@]}"; do
  if [[ $item == 200 ]]; then
    continue
  else
    echo "TEST FAILED"
    exit 1
  fi
done

echo "Test Run successfully"
exit 0
