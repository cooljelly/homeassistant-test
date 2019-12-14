#!/usr/bin/python3

#encoding=utf-8
import os
import serial
import time
import sys
import sqlite3
from struct import *
def main():
    conn = sqlite3.connect('/home/pi/plantower/plantower.db')
    c = conn.cursor()
    cursor = c.execute('''select value from sensor
            where key = "%s"''' % sys.argv[1])
    for row in cursor:
        print(row[0])
    conn.close()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: {} pm1.0/pm2.5/pm10/hcho/temp/humidity".format(sys.argv[0]))
        os._exit(0)

    main()
