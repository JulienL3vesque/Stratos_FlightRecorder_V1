'''
Created on Jun 7, 2016
modified july 14 2016
@author: sgemme, Frantz Etienne
'''
from abc import ABCMeta, abstractmethod
from Adafruit_BNO055 import BNO055
import time

class INineDOF(object):
    '''
    classdocs
    '''
    
    __metaclass__ = ABCMeta


    @abstractmethod
    def getOrientation(self):
        '''
        Returns:         
           tuple: l'orientation, contenant un quaternion: qw,qx,qy,qz
        '''
        pass

    @abstractmethod
    def getTemperature(self):
        '''
        Returns:         
           la temperature, en celcius
        '''
        pass

    @abstractmethod
    def getMagnetometre(self):
        '''
        Returns:         
           data x, y, z du magnetometre en micro-teslas
        '''
        pass

    @abstractmethod
    def getGyroscope(self):
        '''
        Returns:         
           data x, y, z du gyroscope en degree par secondes
        '''
        pass

    @abstractmethod
    def getAccelerometre(self):
        '''
        Returns:         
           data x, y, z du accelerometre en metre par secondes carre
        '''
        pass        

    @abstractmethod
    def getAccelerometreLineaire(self):
        '''
        Returns:         
           data x, y, z d'acceleration venant uniquement du mouvement, 
           et ne prend pas en compte la grative. unite en metre par seconde carre.
        '''
        pass   
class NineDOF(INineDOF):
    
    #Data de calibration recueilli avec le demo webgl
    CALIBRATION_DATA = [237, 255, 20, 0, 41, 0, 202, 255, 77, 1, 139, 255, 254, 255, 0, 0, 255, 255, 232, 3, 52, 3]


    initialized = True
    def __init__(self):      
        '''
        On initialize le 9dof, model BNO055 sur le port dev/i2c-1
        ADDRESS I2C du BNO055 : 0x28
        '''        

        #initialize le BNO055 sur port /dev/i2c-1
        self.bno = BNO055.BNO055()

        try:
            if not self.bno.begin():
                self.initialized = False
                print('Erreur ouverture du BNO055!')

            self.bno.set_calibration(self.CALIBRATION_DATA)
        except Exception:
            print "Erreur initialization du BNO055 (9dof) "
            self.initialized = False

        return


    def getOrientation(self):
        '''
        Returns:         
           tuple: l'orientation, contenant un quaternion: qw,qx,qy,qz
        '''
        x,y,z,w = (-1,-1,-1,-1)
        if self.initialized:
            x,y,z,w = self.bno.read_quaternion()

        return (x,y,z,w)


    def getTemperature(self):
        '''
        Returns:         
           la temperature, en celcius
        '''
        temp = -1
        if self.initialized:
            temp = self.bno.read_temp()

        return temp


    def getMagnetometre(self):
        '''
        Returns:         
           data x, y, z du magnetometre en micro-teslas
        '''
        x,y,z = (-1,-1,-1)
        if self.initialized:
            x,y,z = self.bno.read_magnetometer()

        return (x,y,z)        
    

    def getGyroscope(self):
        '''
        Returns:         
           data x, y, z du gyroscope en degree par secondes
        '''
        x,y,z = (-1,-1,-1)
        if self.initialized:
            x,y,z = self.bno.read_gyroscope()

        return (x,y,z)


    def getAccelerometre(self):
        '''
        Returns:         
           data x, y, z du accelerometre en metre par secondes carre
        '''
        x,y,z = (-1,-1,-1)
        if self.initialized:
            x,y,z = self.bno.read_accelerometer()

        return (x,y,z)     


    def getAccelerometreLineaire(self):
        '''
        Returns:         
           data x, y, z d'acceleration venant uniquement du mouvement, 
           et ne prend pas en compte la grative. unite en metre par seconde carre.
        '''
        x,y,z = (-1,-1,-1)
        if self.initialized:
            x,y,z = self.bno.read_linear_acceleration()

        return (x,y,z)             


    def getInfoCalibration(self):
        '''
        Returns:         
           Statut de calibration des capteurs, 0=uncalibrated and 3=fully calibrated.
        '''
        sys, gyro, accel, mag = (-1,-1,-1,-1)
        if self.initialized:
            sys, gyro, accel, mag = self.bno.get_calibration_status()

        return (sys, gyro, accel, mag)    

    
class SimNineDOF(INineDOF):
    '''
    Un simulateur.
    '''
    
    def getOrientation(self):
        return (1,2,3,4)

    def getTemperature(self):
        return 0

    def getMagnetometre(self):
        return (1,2,3)       
    
    def getGyroscope(self):
        return (1,1,1)

    def getAccelerometre(self):
        return (1,2,3)       

    def getAccelerometreLineaire(self):
        return (1,2,3)

'''
print('starting test\n')
nine_df = NineDOF()
while True:
    sys, gyro, accel, mag = nine_df.getInfoCalibration()
    print('calibration (sys, gyro, accel, mag) {0}, {1}, {2}, {3}\n'.format( sys, gyro, accel, mag))
    x,y,z,w = nine_df.getOrientation()
    print('orientation {0}, {1}, {2}, {3}\n'.format( x,y,z,w))
    temp = nine_df.getTemperature()
    print('temperature {0}\n'.format( temp))
    x,y,z = nine_df.getAccelerometre()
    print('accelerometre {0}, {1}, {2}\n'.format( x,y,z))
    x,y,z = nine_df.getGyroscope()
    print('gyroscope {0}, {1}, {2}\n'.format( x,y,z))
    x,y,z = nine_df.getMagnetometre()
    print('magnetometre {0}, {1}, {2}\n'.format( x,y,z))
    x,y,z = nine_df.getAccelerometreLineaire()
    print('accelerometre lineraire {0}, {1}, {2}\n'.format( x,y,z))
    print("\n")
    time.sleep(2)
print('test end\n')
'''