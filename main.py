#!/usr/bin/env python3
'''
Created on Jun 7, 2016

@author: SBenoit
@modif: jLevesque
'''

import time
import datetime
import base64
import json

from frets.frets import FRETS
from frets.gps_frets import SimGPS, GPSFrets
from frets.frets_io import FileDataRecorder
from frets.nine_dof import SimNineDOF, NineDOF
from frets.pi_sense_hat import SimSenseHat, PiSenseHat
from frets.altimetre import altiMS5607, SimAltimetre
from frets.connect import maConnection
from frets.kiss import toKiss

SERVER_IP = '172.20.4.1'
SERVER_PORT = 5001
SERVER_IMG_PORT = 3000

#-----------------------------------------------------
# En simulation pour le fichier dans la branche master
sim = False
'''Indique si nous sommes en simulation ou non.'''
#-----------------------------------------------------

if __name__ == '__main__':

    gps = None
    nineDOF = None
    senseHat = None

    if sim:  # Si on est en simulation
        gps = SimGPS()
        nineDOF = SimNineDOF()
        senseHat = SimSenseHat()
        altimetre = SimAltimetre()

        #Ici on instancie le socket
        conn = maConnection()
    else:  # Nous ne sommes pas en sim.
        gps = GPSFrets()
        nineDOF = NineDOF()
        senseHat = PiSenseHat()
        altimetre = altiMS5607(1)  # Port I2C-1

        # Ici on instancie le socket
        conn = maConnection()
        #Connection pour envoyer l'image
        conn2 = maConnection()
    # Creation de l'objet fr
    fr = FRETS(gps, altimetre, nineDOF, senseHat, datetime.datetime.now())

    # On cree le recorder
    recorder = FileDataRecorder("record - " + str(datetime.datetime.date(datetime.datetime.now())) + ".dat")
    altitude = []
    #On se connecte ...
    conn.connect(SERVER_IP,SERVER_PORT)
    conn2.connect(SERVER_IP, SERVER_IMG_PORT)


    # On commence a interroger frets.
    while True:
        try:    # On prend la telemetry de frets.
            tlm = fr.getTelemetry()

            # On print ( pour les tests / debug )
            position = tlm.gpsPosition

            #Json string for debug
            jsonTlm = fr.getEncodedTelemetry()

            #Telemetry Send
            if conn.connected():
                conn.send(toKiss(fr.getEncodedTelemetry()))

            #Image Send
            if conn2.connected():
                conn.send(toKiss(jsonImg))

            position = tlm.gpsPosition

            # On enregistre dans le recorder.
            recorder.record(tlm)

            # On print ( pour les tests / debug )
            print jsonTlm

            if jsonImg is not None:
                print jsonImg
            # Pause de 1s
            time.sleep(5.0)

        except (KeyboardInterrupt, SystemExit):
            if sim == False:
                senseHat.printStop()
            #Let the thread finish his work
            if conn:
                #Attend que le thread se termine
                conn.join()
            if conn2:
                conn2.join()
            break
    raise
