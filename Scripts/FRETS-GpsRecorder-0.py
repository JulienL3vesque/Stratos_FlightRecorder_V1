# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
# ! usr/bin/python

import os
import os.path
import datetime
from httplib import NON_AUTHORITATIVE_INFORMATION

from MS5607 import MS5607
from gps import *
from time import *
import time
import threading
from Adafruit_BNO055 import BNO055

gpsd = gps(mode=WATCH_ENABLE)
f_gps = None  # GPS FILE
f_log = None  # Log File
f_gpsRAW = None  # RAW DATA

os.system('clear')  # Clear the terminal


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd

        self.current_value = None
        self.running = True  # Start the thread

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()


def gps_file_verif():
    global f_gps  # GPS FILE
    global f_log  # Log File
    global f_gpsRAW  # RAW DATA

    print("Verifying log file ...")

    if os.path.exists("/home/pi/FRETS/test/log"):
        f_log = open("/home/pi/FRETS/test/log", "a")
    else:
        print("File does not exist. Creating file...")
        f_log = open("/home/pi/FRETS/test/log", "w")

    print("Verifying gpsRAW ...")
    if os.path.exists("/home/pi/FRETS/test/gpsRAW"):
        f_gpsRAW = open("/home/pi/FRETS/test/gpsRAW", "a")
    else:
        print("File does not exist. Creating file...")
        f_gpsRAW = open("/home/pi/FRETS/test/gpsRAW", "w")

    print("Verifying gps ...")
    if os.path.exists("/home/pi/FRETS/test/gps"):
        f_gps = open("/home/pi/FRETS/test/gps", "a")
    else:
        print("File does not exist. Creating file...")
        f_gps = open("/home/pi/FRETS/test/gps", "w")
        f_gps.write(
            "GPS Data for FRETS module \n Data : utc;longitude;latitude;altitude;eps;epx;epv;ept;speed;climb \n")

    return 0


def reSyncSystem(tempsGPS):
    pass
    #TODO
    print("Need to resynchronize the system")

if __name__ == "__main__":
    # global f_gps   # GPS FILE
    # global f_log   # Log File
    # global f_gpsRAW   # RAW DATA
    maxDeltaTemps = 0.0
    numtry = 0
    gpsp = GpsPoller()  # Create the thread
    sensor = MS5607()
    err = gps_file_verif()  # Open/Create the files
    gpsp.start()
    sleep(1)
    while True:
        if gpsd.valid:
            try:
                # gpsp.start()
                #      while True:

                #Verify that GPS provide UTC time already transformed in seconds
                tempsGPS = gpsd.fix.time
                if type(tempsGPS) == type(0.0):
                #    print('%f' %tempsGPS)
                    tempsSystem = time.time()
                #    print('%f' % tempsSystem)
                    deltaTemps = abs(tempsGPS - tempsSystem)
                #    print('Delta time : %f' % deltaTemps)

                if deltaTemps > maxDeltaTemps :
                    maxDeltaTemps = deltaTemps
                    f_log.write("Delta time max gps/system : %f \n" %maxDeltaTemps)
                    f_log.flush()

                if deltaTemps > 5 :
                    reSyncSystem(tempsGPS)

                #Write the GPS data into the gps file
                f_gps.write(gpsd.utc)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.latitude)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.longitude)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.altitude)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.eps)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.epx)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.epv)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.ept)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.speed)
                f_gps.write(";")
                f_gps.write('%f' % gpsd.fix.climb)
                f_gps.write("\n")

                #Write the raw string
                f_gpsRAW.write('%s' % gpsd.response)  # Print the raw gps string into the file

                #Flush the file to avoid problem and so they can be read instantaneously
                f_gps.flush()
                f_gpsRAW.flush()

                #ALTIMETRE/PRESSURE SENSOR
                #pressure = sensor.getDigitalPressure()
                #temperature = sensor.getDigitalTemperature()

                #realTemp = sensor.getTemperature()
                #print("Digit Temps = %f" %realTemp)
                #converted = sensor.convertPressureTemperature(pressure, temperature)
                #print("Pression = %f" % converted)
                #altitude = sensor.getMetricAltitude(converted, sensor.inHgToHectoPascal(
                #    29.95))  # set the altimeter setting appropriately
               # print("Altitude (m) = %f" %altitude)
                # os.fsync(f_gps)
                # os.fsync(f_gpsRAW)

                time.sleep(1)

            except (KeyboardInterrupt, SystemExit):
                gpsp.running = False
                gpsp.join()
                f_log.write('%s' % datetime.datetime.now())
                f_log.write("  -  GPS Program Ended.\n")
                print("Closing files \n")


                ret = f_gps.close()
                if ret:
                    print("Error closing gps file\n")
                    f_log.write('%s' % datetime.datetime.now())
                    f_log.write("  -  Error Closing gps file.\n")

                ret = f_gpsRAW.close()
                if ret:
                    print("Error closing gpsRAW file\n")
                    f_log.write('%s' % datetime.datetime.now())
                    f_log.write("  -  Error closing gpsRAW file.\n")

                ret = f_log.close()
                if ret:
                    print("Error closing log file\n")

                print("End of line.\n")
                exit()

        else:
            f_log.write("GPS Offline, try #")
            f_log.write('%d' % numtry)
            numtry = numtry + 1
            print ("GPS Offline...reconnecting in 10 seconds\n")
            sleep(10)
            if numtry > 10:
                print("gpsd not responding, maybe GPS offline, exiting.\n")
                f_log.write("GPS Offline, not responding after 10 attempts \n exiting.")
                f_log.flush()
                exit()
