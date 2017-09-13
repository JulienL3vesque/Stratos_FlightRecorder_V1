'''
Created on Jun 7, 2016

@author: sgemme
'''
from abc import ABCMeta, abstractmethod
from fileinput import filename
import os
import os.path
import json

class IDataRecorder(object):
    '''
    classdocs
    '''

    __metaclass__ = ABCMeta

    def __init__(self, params):
        '''
        Constructor
        '''

    @abstractmethod
    def record(self, telemetry):
        '''
        Enregistre une donnee de telemetry.

        Args:
            telemetry(Telemetry): la telemetry a enregistrer.

        '''
        pass


class FileDataRecorder(IDataRecorder):
    
    def __init__(self, fileName):
        '''
        Constructeur.
        
        Args:
            fileName(str): le fichier dans lequel enregistrer.
        '''
        
        # On s'assure que c'est un 'str'
        assert(isinstance(fileName,str))
        
        self.__fileName = filename
        # On fait le reste, ouvrir le fichier, etc ...
        if not os.path.exists("/home/pi/FRETS/record/"):
            os.mkdir("/home/pi/FRETS/record/", 0777)

        if os.path.exists("/home/pi/FRETS/record/" + fileName) :
            self.__fd = open("/home/pi/FRETS/record/" + fileName, "a")
        else:
            print("File does not exist. Creating file...")
            self.__fd = open("/home/pi/FRETS/record/" + fileName, "w")

    def record(self, telemetry):
        '''
        Enregistre une donnee de telemetry.

        Args:
            telemetry(Telemetry): la telemetry a enregistrer.
        '''
        #Write the data
        self.__fd.write(repr(telemetry))
        #Flush, so we don't lose any data
        self.__fd.flush()
