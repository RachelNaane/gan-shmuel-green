API_BASE_URL="http://localhost:8083"

> score.txt

ENDPOINTS=( "/health" "/rates")


for endpoint in "${ENDPOINTS[@]}"; do
 
  response=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE_URL$endpoint")
  RESPONSES+=("$response")
  
  if [[ $response == *"200"* ]]; then
   
    echo "Request to $endpoint was successful." >> score.txt
  else
   
    echo "Request to $endpoint failed." >> score.txt
  fi
  
done

if [[ ${RESPONSES[@]} =~ "200" ]]; then
  
  echo "Wokred" 
  exit 0
else
  
  exit 1
fi