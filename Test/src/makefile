test1: testi2c.c
	gcc -Wall -c -std=c99 -pthread  -lwiringPi testi2c.c -o testi2c.o
	gcc -lwiringPi -pthread testi2c.o -o testi2c

test2 : test2.c
	gcc -Wall -c -std=c99 -pthread -lwiringPi test2.c -o test2.o
	gcc -lwiringPi -pthread test2.o -o test2
