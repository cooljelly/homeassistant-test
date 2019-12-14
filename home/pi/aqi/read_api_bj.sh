#!/bin/bash
# get AQI
MY_VAR="$(curl -s https://api.waqi.info/feed/beijing/?token=147f85dff02409e05fac7c944eb4f547be452717  | jq "{aqi: .data.aqi, pm25: .data.iaqi.pm25.v, pm10: .data.iaqi.pm10.v}")"  


pm25="$(echo $MY_VAR | jq ".pm25")"  
echo $pm25
