
functest=0
HOST="localhost:5000"
# HOST='localhost:8081'

#truck in 
result=$(curl -X POST -d 'direction=in&truck=T-SystemTest&containers='C-65816'&weight=1500&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":1500,"id":.*,"truck":"T-SystemTest"}'; then
	functest=$((functest + 1))
     

else

	echo "Error when fisrt truck in " >> "score.txt"
fi

#truck out 
result=$(curl -X POST -d 'direction=out&truck=T-SystemTest&containers='C-65816'&weight=830&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '{"bruto":830,"id":".*","neto":400,"truck":"T-SystemTest"}'; then
	functest=$((functest + 1))
    

else

	echo "Error when fisrt truck out " >> "score.txt"
fi

#truck out again
result=$(curl -X POST -d 'direction=out&truck=T-SystemTest&containers='C-65816'&weight=730&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '{"bruto":730,"id":".*","neto":500,"truck":"T-SystemTest"}'; then
	functest=$((functest + 1))
    

else

	echo "Error when fisrt truck out again " >> "score.txt"
fi

#truck in 
result=$(curl -X POST -d 'direction=in&truck=T-SystemTest2&containers='C-65816'&weight=1500&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":1500,"id":.*,"truck":"T-SystemTest2"}'; then
	functest=$((functest + 1))
else
	echo "Error when new truck in " >> "score.txt"
fi

#truck in again
result=$(curl -X POST -d 'direction=in&truck=T-SystemTest2&containers='C-65816'&weight=1600&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":1600,"id":".*","truck":"T-SystemTest2"}'; then
	functest=$((functest + 1))
else
	echo "Error when new truck in again " >> "score.txt"
fi

#None
result=$(curl -X POST -d 'direction=None&truck=T-SystemTest2&containers='C-35434'&weight=619&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":296,"containers":"C-35434","id":.*}'; then
	functest=$((functest + 1))
else
	echo "Error when None " >> "score.txt"
fi


#truck in 
result=$(curl -X POST -d 'direction=in&truck=T-SystemTest7&containers='C-65816'&weight=1500&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":1500,"id":.*,"truck":"T-SystemTest7"}'; then
	functest=$((functest + 1))
else
	echo "Error when new truck in " >> "score.txt"
fi


#truck in multi conts
result=$(curl -X POST -d 'direction=in&truck=T-SystemTest&containers='C-52273,C-63478,C-42418'&weight=3200&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":3200,"id":.*,"truck":"T-SystemTest"}'; then
	functest=$((functest + 1))
else

	echo "Error when new truck in with multi containers" >> "score.txt"
fi

#truck out multi conts
result=$(curl -X POST -d 'direction=out&truck=T-SystemTest&containers='C-52273,C-63478,C-42418'&weight=2200&unit=kg&force=true&produce=apples' "http://$HOST/weight")

if echo "$result" | grep -q '"bruto":2200,"id":".*","neto":161,"truck":"T-SystemTest"}'; then
	functest=$((functest + 1))
else
	echo "Error when new truck out with multi containers" >> "score.txt"
fi

#batch
result=$(curl -X post -d 'filename=containers1.csv&pass=pass123' "http://$HOST/batch")

if echo "$result" | grep -q 'OK'; then
	functest=$((functest + 1))
else
	echo "Error in Batch" >> "score.txt"
fi



echo "Request to post/weight $functest/10 Passed successfully" >> "score.txt"

if [[ "$functest" -eq 10 ]]; then
    exit 0
else
    exit 1
fi