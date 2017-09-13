# coding=utf-8

'''
Created on Jun 7, 2016

@author: sgemme, frantz
'''
from sense_hat import SenseHat
from abc import ABCMeta, abstractmethod
import random
import time


class ISenseHat(object):
    '''
    classdocs
    '''

    __metaclass__ = ABCMeta

    
    @abstractmethod
    def getTemperature(self):
        '''
        Returns:
            float: la temperature courante, en celcius.
        '''
        pass

    @abstractmethod
    def getPressure(self):
        '''
        Returns:
            float: la pression courante, en millibar.
        '''
        pass

    @abstractmethod
    def getHumidity(self):
        '''
        Returns:
            float: l'humidite courante, en pourcentage entre 0 et 100.
        '''
        pass

    @abstractmethod
    def getOrientation(self):
        '''
        Returns:
            float: Le roulis, tangage et lacet en degree
        '''
        pass

    @abstractmethod
    def getAcceleration(self):
        '''
        Returns:
            float: Acceleration x, y, z
        '''
        pass    
    

class PiSenseHat(ISenseHat):

    '''
    Par mesure de precaution, et pour avoir des rÃ©sultats plus fiable, on ne prend
    jamais la premiere donnÃ©e que le sense hat nous fourmi. Dans une boucle for,
     On va lire le nombre de donnÃ©e defini dans la variable POLL_NUM, 
     et ensuite retournÃ©e la derniere donnÃ©e qu'on obtient.
    '''
    POLL_NUM = 10
    initialized = True

    def __init__(self):
        '''
        Initialize le module du sense hat, on reset le registre et on initialize les 
        variables de calibration
        '''
        try:
            self.sense = SenseHat()
            self.sense.clear()
            self.printReady()
            self.calibration()
        except Exception:
            self.initialized = False
            print "error initializing sense hat"
        
        
    
    def getTemperature(self):
        '''retoure la temperature
        Returns:
            float: la temperature courante, en celcius.
        '''

        temperature = -1
        if self.initialized:
            for num in range(0,self.POLL_NUM):
                temperature = round(self.sense.get_temperature_from_pressure(),1)
        return temperature


    def getPressure(self):
        '''retoure la pression
        Returns:
            float: la pression courante, en millibar.
        '''
        pressure = -1
        if self.initialized:
            for num in range(0,self.POLL_NUM):
                pressure = round(self.sense.get_pressure(),1)
        return pressure
    

    def getHumidity(self):
        '''retoure l'humidite
        Returns:
            float: l'humidite courante, en pourcentage.
        '''

        humidity = -1
        if self.initialized:
            for num in range(0,self.POLL_NUM):
                humidity = round(self.sense.get_humidity(),1)
        return humidity


    def getOrientation(self):
        '''retoure les 3 axes d'orientation en degrÃ©e
        Returns:
            float: Le roulis, tangage et lacet en degree
        '''

        (pitch,roll,yaw) = (-1,-1,-1)
        if self.initialized:
            for num in range(0,self.POLL_NUM):
                o = self.sense.get_orientation()
                
            pitch = round(o["pitch"]-self.calib_pitch,1)
            roll = round(o["roll"]-self.calib_roll,1)
            yaw = round(o["yaw"],1)
        return (pitch,roll,yaw)


    def getAcceleration(self):
        '''retoure les 3 axes d'acceleration
        Returns:
            float: l'acceleration en x, y, z entre -1 et 1
        '''

        (x, y, z) = (-1,-1,-1)
        if self.initialized:
            for num in range(0,self.POLL_NUM):
                a = self.sense.get_accelerometer_raw()

            x = round(a["x"]-self.accel_calib_x,1)
            y = round(a["y"]-self.accel_calib_y,1)
            z = round(a["z"]-self.accel_calib_z,1)
        return (x, y, z) 


    def calibration(self):
        '''
            calibre le roulis et tangage (yaw,pitch) et l'acceleration du sense hat
            il faut s'assurer que le sense est a plat et completement immobile
             avant d'appeler cette fonction
        '''

        if self.initialized:
            for num in range(0,self.POLL_NUM):
                o = self.sense.get_orientation()
                a = self.sense.get_accelerometer_raw()

            self.calib_pitch = o["pitch"] - 360
            self.calib_roll = o["roll"]

            self.accel_calib_x = a["x"]
            self.accel_calib_y = a["y"]
            self.accel_calib_z = a["z"]-1
        return;           


    def printValues(self):
        '''
        Fonction test qui va faire un print de toutes les valeurs recueillis par le sense
        '''
        print("temperature: %s \n" % self.getTemperature())
        print("pressure: %s \n" % self.getPressure())
        print("humidity: %s \n" % self.getHumidity())
        print("Orientation (pitch: %f, roll: %f, yaw: %f) \n" % self.getOrientation())
        print("Acceleration (x: %f, y: %f z: %f)  \n" % self.getAcceleration())
        return;


    def printReady(self):
        '''
        Fonction qui affiche 2 pixels verte sur le screen du sense hat
        '''
        if self.initialized:
            self.sense.set_pixel(7, 0, [0, 255, 0])
            self.sense.set_pixel(7, 1, [0, 255, 0])
        return;


    def printStop(self):
        '''
        Fonction qui affiche 2 pixels rouge sur le screen du sense hat
        '''
        if self.initialized:
            self.sense.set_pixel(7, 0, [255, 0, 0])
            self.sense.set_pixel(7, 1, [255, 0, 0])
        return;

    def printClear(self):
        if self.initialized:
            self.sense.clear()
        return;

class SimSenseHat(ISenseHat):
    ''' 
    Un simulateur
    ''' 
    
    def getTemperature(self):
        '''
        Retourne une valeur aleatoire entre 10 et 20 C
        '''
        return random.uniform(10.0,20.0)
    

    def getPressure(self):
        '''
        Retourne une valeur aleatoire entre 500 et 1500 millibar
        '''
        return random.uniform(500.0,1500.0)    


    def getHumidity(self):
        '''
        Retourne une valeur aleatoire entre 1 et 99%
        '''
        return random.uniform(1,99)      


    def getOrientation(self):
        '''
        Retourne 3 valeurs aleatoires entres 0 et 360 degree
        '''
        roll = random.uniform(0,360)  
        pitch = random.uniform(0,360)  
        yaw = random.uniform(0,360)  
        return (roll,pitch,yaw);


    def getAcceleration(self):
        '''
        Retourne 3 valeurs aleatoires entres -1 et 1
        '''
        x = random.uniform(-1,1)  
        y = random.uniform(-1,1)  
        z = random.uniform(-1,1)  
        return (x,y,z);


'''
print("test start\n")
senseTest = PiSenseHat()
senseTest.calibration()
while True:
  #senseTest.printValues()
  print("temperature: " + str(senseTest.getTemperature()))
  time.sleep(2)
print("test end\n")
senseTest.printStop()
'''
