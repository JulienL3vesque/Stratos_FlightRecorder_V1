from MS5607 import MS5607
from abc import ABCMeta, abstractmethod
import math


class IALTIMETRE(object):
    '''Interface d'un altimetre'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getAltitude(self):
        pass

    @abstractmethod
    def getPression(self):
        pass

    @abstractmethod
    def getTemperature(self):
        pass

    @abstractmethod
    def setAltitudeOffset(self, offset):
        pass

    @abstractmethod
    def updateOffsets(self):
        pass


class altiMS5607(IALTIMETRE):

    isValid = True

    '''Initialisation de l'objet, l'argument permet de choisir le port I2C ( 1 ou 0 )'''

    def __init__(self, i2cBus):
        self.sensor = MS5607(i2cBus)
        self.temperature = -1
        self.pression = -1
        self.altitude = -1
        self.SENS2 = 0
        self.OFF2 = 0
        self.altitudeOffset = 0

    def getAltitude(self):
        # Pression de l'ADC du sensor
        pressure = self.sensor.getDigitalPressure()
        # Temperature qui vient de l'ADC du sensor
        temperature = self.sensor.getDigitalTemperature()

        if pressure == -1:
            self.isValid = False


        ''' Correction de 2eme ordre, provient de la datasheet
        https://www.parallax.com/sites/default/files/downloads/29124-MS5607-02BA03-Datasheet.pdf'''
        # Mise a jour des offsets s'il y a lieu
        self.updateOffsets()

        if self.isValid == False:
     	    return -1
        else:
            # Calculate 1st order pressure and temperature
            dT = temperature - (self.sensor.coefficients[4] * 256)
            # Offset at actual temperature
            off = self.sensor.coefficients[1] * 4 + ((float(dT) / 2048) * (float(self.sensor.coefficients[3]) / 1024))
            # Sensitivity at actual temperature
            sens = self.sensor.coefficients[0] * 2 + ((float(dT) / 4096) * (float(self.sensor.coefficients[2]) / 1024))
            # Temperature compensated pressure
            compPress = (float(pressure) / 2048) * ((float(sens) - float(self.SENS2)) / 1024) - (
            float(off) - float(self.OFF2))

            # Formule base sur p = 101325(1-2.25577*10^-5*h)^5.25588
            # http://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html
            R = float(287.053)
            T = float(288.15)
            g = float(9.80665)
            P0 = float(101325)
            altitude = ((-R * T) / g) * math.log(compPress / P0, math.e)
            # altitude = 44330.760671 - 4946.545907 * pow(compPress,0.1902630958)
            return (altitude - self.altitudeOffset)

    def updateOffsets(self):
        self.getTemperature()
        return

    def setAltitudeOffset(self, offset):
        # On s'assure que c'est un float
        assert (isinstance(offset, float))
        self.altitudeOffset = offset

    def getPression(self):
    	if self.isValid == False:
    		return -1
    	else:
	        # Retourne la pression corrige avec la temperature actuel ( tel que dans la datasheet )
	        return self.sensor.convertPressureTemperature(self.sensor.getDigitalPressure(),
	                                                      self.sensor.getDigitalTemperature())

    def getTemperature(self):
    	if self.isValid == False:
    		return -1
    	else:
	        # SB - 2016-06-06
	        dT = self.sensor.getDigitalTemperature() - self.sensor.coefficients[4] * math.pow(2, 8)
	        temp = (2000 + dT * self.sensor.coefficients[5] / math.pow(2, 23))

	        if temp < 2000:
	            T2 = math.pow(dT, 2) / math.pow(2, 31)
	            self.OFF2 = 61 * math.pow((temp - 2000), 2) / math.pow(2, 4)
	            self.SENS2 = 2 * math.pow((temp - 2000), 2)
	        else:
	            T2 = 0
	            self.OFF2 = 0
	            self.SENS2 = 0

	        if temp < -1500:
	            self.OFF2 = self.OFF2 + 15 * math.pow((temp + 1500), 2)
	            self.SENS2 = self.SENS2 + 8 * math.pow((temp + 1500), 2)

	        temp = temp - T2
	        return temp / 100


class SimAltimetre(IALTIMETRE):
    def __init__(self):
        self.temperature = 0
        self.pression = 0
        self.altitude = 0
        self.SENS2 = 0
        self.OFF2 = 0
        self.altitudeOffset = 0

    def getAltitude(self):
        return 99

    def getTemperature(self):
        return 23

    def getPression(self):
        return 101999

    def setAltitudeOffset(self, offset):
        pass

    def updateOffsets(self):
        self.getTemperature()
        return
