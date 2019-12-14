# homeassistant-test
This is my homeassistant config, just simple and easy to try.

## Overall

I use homeassistant as the central controlling node of my home. It is used to:

1. Control light, air purifier, humidifier, etc
2. Use sensors to detect realtime temperature/humidity/air_condition, etc
3. Automation

The initial HA screenshot is as below:




Steps to setup homeassistant:

## Install hassbian (image_2019-07-02-Hassbian)

1. We can choose Raspbian/Hassbian/Mossbian/Hass.io to install. The detailed difference between them is shown in https://home-assistant.cc/installation/raspberrypi/. I use raspberry Pi 3B+ and choose hassbian.

2. Download hassbian image, and balenaEtcher burn tool.
3. Burn hassbian image into SD card, which is then inserted to Raspberry Pi.

Refer:

https://www.home-assistant.io/docs/installation/raspberry-pi/

https://www.home-assistant.io/getting-started/)

## Start homeassistant (v0.102.3)
```
# sudo hassbian-config upgrade hassbian-script
# sudo hassbian-config install homeassistance
```

## Network configuration

### Wifi: 

```
# sudo raspi-config
select network options-> Wi-fi -> Wifi name -> WiFi password ->  OK
Advanced option -> A1 Expand Filesystem->OK-finish
# reboot
```
### VPN

I want to access HA from outside, so I need to use openvpn to connect HA to the IPv6 Internet.
You can use any other VPN to solve the connection problem.

### NGINX

Since HA supports IPv6 not very well, I use nginx to proxy IPv6 requests.
Refer https://www.home-assistant.io/docs/ecosystem/nginx/ for more details.

### HTTPS

I use letsencrypt to secure my HA service:

```
sudo apt-get install certbot python-certbot-nginx
sudo certbot --nginx
```

Refer:

https://certbot.eff.org/lets-encrypt/debianbuster-nginx

https://www.home-assistant.io/docs/ecosystem/nginx/


## Sensors and Switches

### ds18b20 (temperature)

(refer https://github.com/timofurrer/w1thermsensor)

```
sudo vim /boot/config.txt; scroll down to the bottom of the file, and add the line: 
dtoverlay=w1-gpio
Finally reboot the Raspberry Pi so that the changes take effect.
sudo modprobe w1-gpio
sudo modprobe w1-therm
sudo apt-get install python-w1thermsensor
ls /sys/bus/w1/devices/
find the file 28-xxxxxxxxxxxx and fill in read_temp_ds18b20.py
python read_temp_ds18b20.py
```

### dht22 (temperature and humidity)

```
cd Adafruit_Python_DHT
python setup.py install
python /home/pi/temperature/read_temp_dht22.py
python /home/pi/humidity/read_humidity.py
```

### Plantower (PM1.0/2.5/10, cc0.3/0.5/1.0/2.5/5.0/10.0)

```
python3 /home/pi/plantower/read_g5_sensor.py
```
If it runs well, we can add it in crontab, and fetch data in HA configuration file.


### switch

I use broadlink MP1 to turn on/off air purifier/humidifier and broadlink RM to turn on/off airconditioner, etc.

refer:
https://www.home-assistant.io/integrations/broadlink/


## homebridge 

Add following code to configuration.yaml:

```
homekit:
  auto_start: true 
```

After restart HA, it will show a pairing code, which should be paste to your iOS device. 

## GUI

We can customize ui-lovelace.yaml.

For icons we can refer https://cdn.materialdesignicons.com/4.5.95/

## Future application

1. Connect with Xiaodu Speaker(control light, etc.)
2. Hot water circulation system
3. Smart curtain....

# BUGS:

1. always reboot. --> should use original cable.
2. homekit not available --> debugging
