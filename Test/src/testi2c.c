//Programme de test pour le bus I2C
// 2 arduino as slaves
// slave 0x0A et 0x0B

#include "stdlib.h"
#include "stdio.h"
#include "wiringPiI2C.h"
#include "wiringPi.h"
#include "pthread.h"

#define SLAVE_A		0x0A
#define SLAVE_B		0x0B
#define CHANGE_NUM_REG	0x01
#define I2C_INTERFACE  "/dev/i2c-0"

int slaveAfd,slaveBfd;
void changeNum(int num);

int main(int argv, char** argc)
{
	int x = 0;
	slaveAfd = wiringPiI2CSetupInterface(I2C_INTERFACE,SLAVE_A);
	slaveBfd = wiringPiI2CSetupInterface(I2C_INTERFACE,SLAVE_B);
	if (slaveAfd < 0){
		printf("Error slave a : %d",slaveAfd);
		return 1;
	}
	if (slaveBfd < 0){
		printf("Error slave b : %d",slaveBfd);
		return 1;
	}

	while(1)
	{
		changeNum(x);
		x++;
		if (x > 255)
		    x = 0;

		delay(10);
	}

}

void changeNum(int num)
{
	wiringPiI2CWriteReg8(slaveAfd,CHANGE_NUM_REG,num);

}
