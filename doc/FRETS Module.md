*Created by : Simon Benoit*
*Date : 2016-06-23*

# FRETS Module

List of packages to be installed after setting up Raspbian Jessie
---
### GPIO - [Source](https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio)

[Global Documentation](http://elinux.org/RPi_GPIO_Code_Samples)

python-rpi.gpio

[Wiring pi install](http://wiringpi.com/download-and-install/)

### GPS - [GPSD Source](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/use-gpsd)

gpsd

gpsd-clients

python-gps

### 9DOF - [Source](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/overview)

python3-pip

python-pip

python-dev

```
    sudo pip install rpi.gpio
    sudo pip3 install rpi.gpio

    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
    cd Adafruit_Python_BNO055
    sudo python setup.py install
```

### I2C-0 - [Source](http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)

i2c-tools

python-smbus

### Webcam - [Source](http://www.pygame.org/docs/tut/camera/CameraIntro.html)

Need pygame, i think it comes with Raspbian Jessie

python-pygame

### Altimetre - 

```
    git clone https://github.com/llinear/MS5607.git
```

### PI Camera

### 


# Settings to modify

### UART for GPS

The TTY UART must be disabled !!!!!!!!!!

    `sudo nano /boot/cmdline.txt`

First line should be

    `dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait`

Then stop and disable getty service

``` sudo systemctl stop serial-getty@ttyAMA0.service
    sudo systemctl disable serial-getty@ttyAMA0.service 
```

Test the UART : 
    `stty -F /dev/ttyAMA0 raw 9600 cs8 clocal -cstopb`

### 9DOF

Object creation is : 

    `bno = BNO055.BNO055(rst=18)`

### Boot Sequence

In `/etc/rc.local` , add the lines : 

```
    date >> /home/pi/FRETS.log

    sudo /home/pi/FRETS/ip_switch/ipsw -i xxx.xxx.xxx.xxx <--- The IP you want if the jumper is on

    add ">> /home/pi/FRETS.log" to put the output in the log file
```

You need to run `sudo nano /etc/rc.local`

#### Verify the IP switch jumper

Automaticaly when you run ipsw

#### Start the FRETS script

### Watchdog

[Documentation](http://www.switchdoc.com/2014/11/reliable-projects-using-internal-watchdog-timer-raspberry-pi/)

