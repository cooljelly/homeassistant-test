#!/usr/bin/python

import sys
import requests
import Adafruit_DHT

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
val = 1
while val < 10:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 26)
    if temperature < 40 and temperature > 0:
        break

print temperature
