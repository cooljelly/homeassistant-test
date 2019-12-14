#!/bin/sh

a=`/bin/ps ax | grep openvpn | grep -v "check_openvpn" | grep -v "grep"`
if [[ "x$a" = "x" ]]; then
	/usr/sbin/openvpn --config /home/pi/secrets/pi-home-iviaas-server.ovpn &
fi

