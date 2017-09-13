#include <stdlib.h>
#include </usr/include/wiringPi.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

#define ARG_LEN 16

int isValidIpAddress(char *ipAddress)
{
    struct sockaddr_in sa;
    int result = inet_pton(AF_INET, ipAddress, &(sa.sin_addr));
    return result != 0;
}

int main(int argc, char** argv){ 
	char name[ARG_LEN];
	int sw;
	char ip1[ARG_LEN] = "172.20.4.30";
	char ip2[ARG_LEN] = "172.20.4.31";
	char ipDef[ARG_LEN] = "192.168.1.100";
	
	char *ip;
	char cmd[] = "sudo ifconfig eth0 ";
	char dhcp[] = "sudo ifconfig eth0 0.0.0.0 0.0.0.0 && dhclient";
	
	//Get the current PI hostname
	gethostname(name,16);
	
	//Set the default ip if no argument, depending on the hostname
	if (strcmp(name,"FRETS_PI1") == 0)
		ip = ip1;
	else if (strcmp(name,"FRETS_PI2") == 0)
		ip = ip2;
	else
		ip = ipDef;

	//VERIFY THE SWITCHES
	while((sw = getopt(argc,argv,"i:")) != -1)
		switch (sw)
		{
			case 'i':
				printf("IPSW - Ip entered\n");
				if (isValidIpAddress(optarg))
					memcpy(ip,optarg,ARG_LEN*sizeof(char));
				else
					fprintf(stdout,"IPSW - Invalid IP, using default %s\n",ip);
				break;
			default :
				fprintf(stdout, "\nUse -i [ip address xxx.xxx.xxx.xxx]\n");
				exit(EXIT_FAILURE);
		}




	//SETUP THE GPIO
 	if (wiringPiSetup () == -1){
		fprintf(stderr,"IPSW - Error with wiringpi\n ");
    		return 1 ;
	}
  	pinMode (7, INPUT) ;         // aka BCM_GPIO pin 4


	printf("IPSW - Verifying switch on device - %s \n",name);
	printf("IPSW - If jumper is on, eth0 will be set to : %s\n\n",ip);


	//READ THE JUMPER STATUS
	printf("IPSW - Reading pin ...\n");
    	if (digitalRead(7)){
		fprintf(stdout, "IPSW - IP switch jumper removed- Staying in DHCP\n");
	}
	else{
		fprintf(stdout,"IPSW - IP Switch jumper found - Moving to static IP\n");
		strcat(cmd,ip);
		//system("eth0 down");
		//Live IP swap
		system(cmd);
		//system("eth0 up");
	}

	exit(EXIT_SUCCESS);
}
