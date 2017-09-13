// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

//Modified by Simon Benoit
//  24/05/2016

#include <Wire.h>
#include <TM1637Display.h>

// Module connection pins (Digital Pins)
#define CLK 2 //FOR TM1637 ONLY
#define DIO 3 //FOR TM1637 ONLY

#define  MAX_SENT_BYTES       3

int receivedByte;
byte receivedCommands[MAX_SENT_BYTES];
int printNumber = 0;

TM1637Display display(CLK, DIO);

void setup() {
  Wire.begin(10);                 // join i2c bus with address #11
  Wire.onReceive(receiveEvent);   // register event
  Wire.onRequest(requestEvent);   // register event
  Serial.begin(115200);           // start serial for debug output
  //Display  
  display.setBrightness(0x0f);
}

void loop() {

}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
     for (int a = 0; a < howMany; a++)
     {
          if ( a < MAX_SENT_BYTES){
               receivedCommands[a] = Wire.read();
          }
          else{
               Wire.read();  // if we receive more data then allowed just throw it away
          }
     }
   
    switch (receivedCommands[0])  // Action on a "SET" command from the master 
    {
        case 0x01 : 
            printNumber = receivedCommands[1];
            display.showNumberDec(printNumber, false, 3, 1);
            break;
        case 0x02 : 
            display.setBrightness(receivedCommands[1]);
            display.showNumberDec(printNumber, false, 3, 1);
            break;
    }
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void requestEvent() { //Those actions will run on a "get" command from the master
  switch (receivedCommands[0])
  {
    case 0x01 : 
          Wire.write(0x10); // respond with message of 13 bytes
      //    display.showNumberDec(receivedCommands[1], false, 3, 1);
          break;
    case 0x02 : 
          Wire.write(0x20); // respond with message of 13 bytes
          break;
    case 0x03 : 
          Wire.write(0x30); // respond with message of 13 bytes
          break;
    case 0x04 : 
          Wire.write(0x40); // respond with message of 13 bytes
          break;
    case 0x05 : 
          Wire.write(0x50); // respond with message of 13 bytes
          break;
    case 0x06 : 
          Wire.write(0x60); // respond with message of 13 bytes
          break;
    case 0x07 : 
          Wire.write(0x70); // respond with message of 13 bytes
          break;
    case 0x08 : 
          Wire.write(0x80); // respond with message of 13 bytes
          break;
  }
  // as expected by master
}
