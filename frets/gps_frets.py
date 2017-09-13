'''
Created on Jun 7, 2016

@author: sgemme
@modif: SBenoit
'''

import datetime
import os
import os.path
from abc import ABCMeta, abstractmethod
from gps import *
from time import *
import time
import threading



os.system('clear')  # Clear the terminal
NaN = float('nan')

class IGPS(object):
    '''
    Interface representant un GPS.
    '''

    __metaclass__ = ABCMeta


    @abstractmethod
    def getPosition(self):
        '''C'est la methode qui interrroge le vrai GPS.
        '''
        pass

    @abstractmethod
    def getSpeed(self):
        pass

    @abstractmethod
    def getClimb(self):
        pass

    @abstractmethod
    def getTime(self):
        pass

    @abstractmethod
    def getFix(self):
        pass

    @abstractmethod
    def getRaw(self):
        pass

class GPSFrets(IGPS):

    def __init__(self):
        self.__gpsd = gps(mode= WATCH_ENABLE)
        self.__f_gps = None  # GPS FILE
        self.__f_log = None  # Log File
        self.__f_gpsRAW = None  # RAW DATA
        self.__maxDeltaTemps = 0.0
        self.__numtry = 0
        self.__gpsp = GpsPoller(self.__gpsd)  # Create the thread
      #  err = self.gps_file_verif()  # Open/Create the files
        self.__gpsp.start()
        sleep(1)

    def getPosition(self):
        '''C'est la methode qui interrroge le vrai GPS.
        '''
        a = self.__gpsd.fix.longitude
        b = self.__gpsd.fix.latitude
        c = self.__gpsd.fix.altitude
        if isnan(a):
            a = -1
        if isnan(b):
            b = -1
        if isnan(c):
            c = -1
        return (a,b,c)

    def getSpeed(self):
        if isnan(self.__gpsd.fix.speed):
            return -1
        else:
            return self.__gpsd.fix.speed

    def getClimb(self):
        if isnan(self.__gpsd.fix.climb):
            return -1
        else:
            return self.__gpsd.fix.climb

    def getTime(self):
        if isnan(self.__gpsd.fix.time ):
            return -1
        else:
            return self.__gpsd.fix.time

    def getFix(self):
        #Return toute la structure fix
        return self.__gpsd.fix

    def getRaw(self):
        return self.__gpsd.response


class GPSModelXYZ(IGPS):
    '''
    La classe qui parle au vrai gps ( GPSD )
    '''

    def __init__(self):
        pass

class GpsPoller(threading.Thread):
    def __init__(self, gpsd):
        threading.Thread.__init__(self)
        self.__gpsd = gpsd
        self.current_value = None
        self.running = True  # Start the thread

    def run(self):
        while self.running:
            self.__gpsd.next()

class SimGPS(IGPS):
    '''
    Un simulateur de GPS
    '''

    def getPosition(self):
        '''Simulateur simple qui retourne toujours la meme position '''
        return (0,1,2)


    def getSpeed(self):
        return 42


    def getClimb(self):
        return 43


    def getTime(self):
        return 44


    def getFix(self):
        # Return toute la structure fix
        return 45


    def getRaw(self):
        return 46