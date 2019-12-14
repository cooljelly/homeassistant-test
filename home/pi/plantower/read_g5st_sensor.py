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
                rv += _port.read(38)
                return rv
def main():
    i = 1;
    while (i < 10):
        print("haha begin %dth round" % i)
        recv = read_pm_line(ser)
        tmp = recv[4:36]
        datas = unpack('>hhhhhhhhhhhhhhhh', tmp)
        if datas[4] >= 0 and datas[4] < 500 \
           and datas[3] >= 0 and datas[3] < 500 \
           and datas[5] >= 0 and datas[5] < 500 \
           and datas[12] >= 0 and datas[12] < 5000 \
           and datas[13] > 0 and datas[13] < 400 \
           and datas[14] > 0 and datas[14] < 800:
            break
        ser.flushInput()
        time.sleep(0.5)
        pm2p5 = datas[4]
        pm1p0 = datas[3]
        pm10 = datas[5]
        HCHO = datas[12]/1000.0
        temp = datas[13]/10.0
        humidity = datas[14]/10.0
        print('heihei %d %d %d %f %f %f' % (pm2p5, pm1p0, pm10, HCHO, temp, humidity));
        i = i + 1

    if i == 10:
        print("no result")
        return

    pm2p5 = datas[4]
    pm1p0 = datas[3]
    pm10 = datas[5]
    HCHO = datas[12]/1000.0
    temp = datas[13]/10.0
    humidity = datas[14]/10.0
    print('haha %d %d %d %f %f %f' % (pm2p5, pm1p0, pm10, HCHO, temp, humidity));

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
            set value = %f
            where key = "HCHO"''' % HCHO)
    conn.commit()
    c.execute('''update sensor
            set value = %f
            where key = "temp"''' % temp)
    conn.commit()
    c.execute('''update sensor
            set value = %f
            where key = "humidity"''' % humidity)
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
