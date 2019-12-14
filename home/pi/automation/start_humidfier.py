#!/usr/bin/python

import sys
import requests
import Adafruit_DHT

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 26)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

url_on  = 'http://hassbian.local:8123/api/services/switch/turn_on?api_password=xxxxxxxxx'
url_off = 'http://hassbian.local:8123/api/services/switch/turn_off?api_password=xxxxxxxxx'
data = '{"entity_id":"switch.humidifier"}'

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

if humidity < 35:
    requests.post(url_on, data=data,headers={"Content-Type": "application/json", "x-ha-access": "xxxxxxxxx"})
elif humidity > 50:
    requests.post(url_off, data=data,headers={"Content-Type": "application/json", "x-ha-access": "xxxxxxxxx"})





#if [[ $pm25 -gt 100 ]]; then 
#    curl -X POST -H 'x-ha-access: xxxxxxxxx' \
#     -H 'Content-Type: application/json' \on
#     -d '{"entity_id":"switch.airpurifier"}' \
#     http://hassbian.local:8123/api/services/switch/turn_on?api_password=xxxxxxxxx 
#elif [[ $pm25 -lt 60 ]]; then 
#    curl -X POST -H 'x-ha-access: xxxxxxxxx' \
#     -H 'Content-Type: application/json' \
#     -d '{"entity_id":"switch.airpurifier"}' \
#     http://hassbian.local:8123/api/services/switch/turn_off?api_password=xxxxxxxxx 
#fi
