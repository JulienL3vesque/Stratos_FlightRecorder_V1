#! /bin/sh

gcc -c -lwiringPi ipsw.c -o ipsw.o
gcc -lwiringPi ipsw.o -o ipsw
chmod +x ipsw
