#! /bin/sh

INTERVAL=20
TS=$(date +"%Y-%m-%d_%H%M%S")

while true; do
	#Grab the image from the webcam
    fswebcam -r 640x480 /home/pi/FRETS/webcam/imageWeb.jpg >> /home/pi/webcamLog.txt
    #Copy the file with another name
    cp /home/pi/FRETS/webcam/imageWeb.jpg /home/pi/FRETS/webcam/$TS.jpg
    #Wait
    sleep $INTERVAL
done




