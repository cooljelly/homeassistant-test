#!/usr/bin/python3

#encoding=utf-8
import os
import serial
import time
import sys
import sqlite3
from struct import *
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=2.0)
def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(30)
                return rv
def main():
    i = 1;
    while (i < 10):
        print("begin %dth round" % i)
        recv = read_pm_line(ser)
        tmp = recv[4:28]
        datas = unpack('>hhhhhhhhhhhh', tmp)
        if datas[4] >= 0 and datas[4] < 500 \
           and datas[3] >= 0 and datas[3] < 500 \
           and datas[5] >= 0 and datas[5] < 500:
            break
        ser.flushInput()
        time.sleep(0.5)
        pm2p5 = datas[4]
        pm1p0 = datas[3]
        pm10 = datas[5]
        print('fail: %d %d %d' % (pm2p5, pm1p0, pm10));
        i = i + 1

    if i == 10:
        print("no result")
        return

    pm2p5 = datas[4]
    pm1p0 = datas[3]
    pm10 = datas[5]
    print('read successful: %d %d %d %d %d %d %d %d %d %d %d %d' % (datas[4], datas[3], datas[5], datas[1], datas[0], datas[2], datas[6], datas[7], datas[8], datas[9], datas[10], datas[11]));

    conn = sqlite3.connect('/home/pi/plantower/plantower.db')
    c = conn.cursor()
    c.execute('''update sensor
            set value = %d
            where key = "pm2.5"''' % pm2p5)
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "pm1.0"''' % pm1p0)
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "pm10"''' % pm10)
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc0.3um"''' % datas[6])
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc0.5um"''' % datas[7])
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc1.0um"''' % datas[8])
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc2.5um"''' % datas[9])
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc5.0um"''' % datas[10])
    conn.commit()
    c.execute('''update sensor
            set value = %d
            where key = "cc10um"''' % datas[11])
    conn.commit()
    conn.close()

    ser.flushInput()
    time.sleep(0.1)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
