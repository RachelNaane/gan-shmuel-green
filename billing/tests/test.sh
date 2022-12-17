API_BASE_URL="http://localhost:8083"

> score.txt

# /rates APIS

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

response=$(curl -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"name":"Best Provider"}' $API_BASE_URL/provider)
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

response=$(curl -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"id":"T-32126", "provider":10001}' $API_BASE_URL/truck)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "POST Request to /truck was successful." >> score.txt
else
  echo "POST Request to /truck failed." >> score.txt
fi

response=$(curl -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: application/json" -d '{"provider_id":10001}' $API_BASE_URL/truck/T-32123)
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "PUT Request to /truck was successful." >> score.txt
else
  echo "PUT Request to /truck failed." >> score.txt
fi

response=$(curl -s -o /dev/null -w "%{http_code}" "localhost:8083/truck/T-11111")
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "GET Request to /truck was successful." >> score.txt
else
  echo "GET Request to /truck failed." >> score.txt
fi

response=$(curl -s -o /dev/null -w "%{http_code}" "localhost:8083/bill/10001")
RESPONSES+=("$response")

if [[ $response == *"200"* ]]; then
  echo "GET Request to /bill was successful." >> score.txt
else
  echo "GET Request to /bill failed." >> score.txt
fi

if [[ ${RESPONSES[@]} =~ "200" ]]; then
  echo "Wokred" 
  exit 0

else
  
  exit 1
fi
