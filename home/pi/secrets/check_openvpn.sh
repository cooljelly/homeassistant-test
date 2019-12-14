#!/bin/sh

#a=`/bin/ps ax | grep openvpn | grep -v "grep"`
b=`/sbin/ip a | grep tun`
if [[ "x$b" == "x" ]]; then
	/usr/sbin/openvpn --config /home/homeassistant/.homeassistant/secrets/pi-home-iviaas-server.ovpn &
fi

