#!/bin/bash
# get AQI
MY_VAR="$(curl https://api.waqi.info/feed/beijing/?token=147f85dff02409e05fac7c944eb4f547be452717 | jq "{aqi: .data.aqi, pm25: .data.iaqi.pm25.v, pm10: .data.iaqi.pm10.v}")"  
echo $MY_VAR


pm25="$(echo $MY_VAR | jq ".pm25")"  
if [[ $pm25 -gt 100 ]]; then 
    curl -X POST -H 'x-ha-access: xxxxxxxxx' \
     -H 'Content-Type: application/json' \
     -d '{"entity_id":"switch.airpurifier"}' \
     http://hassbian.local:8123/api/services/switch/turn_on?api_password=xxxxxxxxx 
elif [[ $pm25 -lt 60 ]]; then 
    curl -X POST -H 'x-ha-access: xxxxxxxxx' \
     -H 'Content-Type: application/json' \
     -d '{"entity_id":"switch.airpurifier"}' \
     http://hassbian.local:8123/api/services/switch/turn_off?api_password=xxxxxxxxx 
fi
