'''
Created on Jun 7, 2016

@author: SBenoit
@modif: JLevesque
'''
import base64
import datetime
import json
import os

from gps_frets import IGPS
from nine_dof import INineDOF
from pi_sense_hat import ISenseHat
from altimetre import IALTIMETRE
import pygame
import pygame.camera
from pygame.locals import *


class FRETS(object):
    '''
    classdocs
    '''
    '''TODO : Choisir un timesource, faire une methode pour utiliser
    le RTC et/ou comparer le GPD le RTC et le time systeme'''

    def __init__(self, gps, altimetre, nineDOF, senseHat, timeSource):
        '''
        Constructor
        Args:        
            gps(IGPS): le gps
            nineDof(INineDOF): le 9DOF
            PiSenseHat(ISenseHat): le sense hat       
        '''
        # On s'assure que les object sont du bon type.
        assert (isinstance(gps, IGPS))
        assert (isinstance(nineDOF, INineDOF))
        assert (isinstance(senseHat, ISenseHat))
        assert (isinstance(timeSource, datetime.datetime))
        assert (isinstance(altimetre, IALTIMETRE))

        # le prefix __ indique que l'attribut est prive.
        self.__gps = gps
        self.__nineDOF = nineDOF
        self.__senseHat = senseHat
        self.__timestamp = timeSource
        self.__altimetre = altimetre
        self.__Camera = Camera()

        #Make sure our working folder exists
        if not os.path.exists("/home/pi/FRETS/"):
            os.mkdir("/home/pi/FRETS/", 0777)

    def getTelemetry(self):
        '''
        Returns:
            la telemetrie, de type telemetry
        '''
        tlm = Telemetry()

        tlm.nineDofOrientation = self.__nineDOF.getOrientation()
        tlm.nineDofMagnetometre = self.__nineDOF.getMagnetometre()
        tlm.nineDofGyroscope = self.__nineDOF.getGyroscope()
        tlm.nineDofAccelerometre = self.__nineDOF.getAccelerometre()
        tlm.nineDofAccelerometreLin = self.__nineDOF.getAccelerometreLineaire()
        tlm.senseHatTemperature = self.__senseHat.getTemperature()
        tlm.senseHatHumidite = self.__senseHat.getHumidity()
        tlm.senseHatOrientation = self.__senseHat.getOrientation()
        tlm.senseHatAcceleration = self.__senseHat.getAcceleration()
        tlm.senseHatPression = self.__senseHat.getPressure()
        tlm.gpsRaw = self.__gps.getRaw()
        tlm.gpsPosition = self.__gps.getPosition()
        tlm.gpsSpeed = self.__gps.getSpeed()
        tlm.timestamp = self.__timestamp.now()
        tlm.altitude = self.__altimetre.getAltitude()
        tlm.pression = self.__altimetre.getPression()
        tlm.altiTemp = self.__altimetre.getTemperature()

        return tlm

    def takePicture(self,name):
        if self.__Camera.camlist[0]:
            self.__Camera.getPicture(0)
            self.__Camera.savePicture(name)
        else:
            print "Camera not available ..."
            
    def getEncodedTelemetry(self):
        #Create a dictionary with the data
        data =  {}

        #Destination
        data['eClass'] = 'ca.gc.asc_csa.stratos.flight_recorder.client.frets#//FlightDataItemFRETS'
        
        #Time - Raspberry PI
        data['time'] = str(self.__timestamp.now())
        
        #Position - GPS
        data['longitude'] = self.__gps.getPosition()[0]
        data['latitude'] = self.__gps.getPosition()[1]
        data['elevation'] = self.__gps.getPosition()[2]
        
        #Climb - GPS
        data['gpsClimb'] = self.__gps.getClimb()
        
        #Speed - GPS
        data['gpsSpeed'] = self.__gps.getSpeed()
        
        #Fix - GPS
        #sdata['gpsFix'] = self.__gps.getFix()
        
        #Orientation - 9DOF
        data['nineDofOrientationW'] = self.__nineDOF.getOrientation()[0]
        data['nineDofOrientationX'] = self.__nineDOF.getOrientation()[1]
        data['nineDofOrientationY'] = self.__nineDOF.getOrientation()[2]
        data['nineDofOrientationZ'] = self.__nineDOF.getOrientation()[3]
        
        #Magnetometre - 9DOF
        data['nineDofMagX'] = self.__nineDOF.getMagnetometre()[0]
        data['nineDofMagY'] = self.__nineDOF.getMagnetometre()[1]
        data['nineDofMagZ'] = self.__nineDOF.getMagnetometre()[2]
        
        #Gyroscope - 9DOF
        data['nineDofGyroX'] = self.__nineDOF.getGyroscope()[0]
        data['nineDofGyroY'] = self.__nineDOF.getGyroscope()[1]
        data['nineDofGyroZ'] = self.__nineDOF.getGyroscope()[2]
        
        #Accelerometre - 9DOF
        data['nineDofAccX'] = self.__nineDOF.getAccelerometre()[0]
        data['nineDofAccY'] = self.__nineDOF.getAccelerometre()[1]
        data['nineDofAccZ'] = self.__nineDOF.getAccelerometre()[2]
        
        #Accelerometre Lineaire - 9DOF
        data['nineDofLinAccX'] = self.__nineDOF.getAccelerometreLineaire()[0]
        data['nineDofLinAccY'] = self.__nineDOF.getAccelerometreLineaire()[1]
        data['nineDofLinAccZ'] = self.__nineDOF.getAccelerometreLineaire()[2]
        
        #Temperature - Sense Hat
        data['senseTemperature'] = self.__senseHat.getTemperature()
        
        #Pression - Sense Hat
        data['sensePressure'] = self.__senseHat.getPressure()
        
        #Humidite - Sense Hat
        data['senseHumidity'] = self.__senseHat.getHumidity()
        
        #Orientation - Sense Hat
        data['sensePitch'] = self.__senseHat.getOrientation()[0]
        data['senseYaw'] = self.__senseHat.getOrientation()[1]
        data['senseRoll'] = self.__senseHat.getOrientation()[2]
        
        #Accelerometre - Sense Hat
        data['senseAccX'] = self.__senseHat.getAcceleration()[0]
        data['senseAccY'] = self.__senseHat.getAcceleration()[1]
        data['senseAccZ'] = self.__senseHat.getAcceleration()[2]
        
        #Temperature - Altimetre
        data['altimeterTemperature'] = self.__altimetre.getTemperature()
        
        #Pression - Altimetre
        data['altimeterPressure'] = self.__altimetre.getPression()
        
        #Altitude relative - Altimetre
        data['altimeterRelativeAltitude'] = self.__altimetre.getAltitude()
        
        #Altitude absolue - Altimetre
        data['altimeterAbsoluteAltitude'] = self.__altimetre.getAltitude()
        
        #Encode to json
        encodedData = json.dumps(data)

        return encodedData

class Telemetry(object):
    '''
    classdocs
    '''

    def __init__(self):
        ''' Construit une nouvelle instance de Telemetry'''
        self.nineDofOrientation = None
        self.nineDofMagnetometre = None
        self.nineDofGyroscope = None
        self.nineDofAccelerometre = None
        self.nineDofAccelerometreLin = None
        self.senseHatTemperature = 0.
        self.senseHatHumidite = None
        self.senseHatOrientation = None
        self.senseHatAcceleration = None
        self.senseHatPression = None
        self.gpsRaw = None
        self.gpsPosition = None
        self.gpsSpeed = 0
        self.timestamp = None
        self.altitude = 0
        self.pression = 0
        self.altiTemp = 0

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


'''
    def file_verif(self):
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
    '''
    
class Camera(object):
    def __init__(self):
        pygame.init()
        pygame.camera.init()
        self.camlist = pygame.camera.list_cameras()

    def getPicture(self,camNum):

            if  self.camlist:
                cam = pygame.camera.Camera(self.camlist[camNum], (640, 480))
                cam.start()
                self.image = cam.get_image()
                cam.stop()
            else:
                print "No camera available ..."


    def savePicture(self, name):


        savePath = "/home/pi/FRETS/camera/"
        if not os.path.exists(savePath):
            os.mkdir(savePath, 0777)
        pygame.image.save(self.image, savePath + name)
