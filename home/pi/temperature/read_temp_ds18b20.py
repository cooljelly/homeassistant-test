#!/usr/bin/python
#import Adafruit_DHT
import datetime
import json
import copy
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "02131d572daa")
print sensor.get_temperature()
