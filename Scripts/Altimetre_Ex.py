import time
import datetime
from MS5607 import MS5607
from DS1307 import DS1307


if __name__ == '__main__':
    sensor = MS5607()
    rtc = DS1307(1, 0x68)   #i2c Bus, Address

    rtc.write_now()
    while True:

        # ALTIMETRE/PRESSURE SENSOR
        pressure = sensor.getDigitalPressure()
        temperature = sensor.getDigitalTemperature()

        realTemp = sensor.getTemperature()
        print("Digit Temps (celcius) = %f" % realTemp)
        converted = sensor.convertPressureTemperature(pressure, temperature)
        print("Pression (Pa) = %f" % converted)
        altitude = sensor.getImperialAltitude(converted, sensor.inHgToHectoPascal(
            33.8639))  # set the altimeter setting appropriately
        print("Altitude (m) = %f" % altitude)

     #   print("nsec = %s" %datetime.datetime.now().strftime("%H:%M:%S.%f"))

     #   print("Time is : %s" %rtc.read_str())


        time.sleep(1)
