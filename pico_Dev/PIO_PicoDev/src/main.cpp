#include <Arduino.h>

#include "i2c_com.h"
#include "MoveStepper.h"
#include "MoveServo.h"
#include "buzzerNotification.h"
#include "microstepper.h"

I2C_Comm &i2c = I2C_Comm::getInstance();
const int stepPin = 11; 
const int dirPin = 10; 
const int rstPin = 12;
Stepper stepper1(stepPin, dirPin, rstPin); //create stepper object
MainServo mainServo(9);
Microstepper micro(42, 100, {3, 5, 4, 6});    // purpose, yellow, orange green or blue, black, red, white
//3,11,9,10

void processCommand(int commandNumber, int value);

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  i2c.begin(8, &processCommand);

  // Setting the pins up
  micro.begin();
  stepper1.begin();
  mainServo.begin();
  micro.rotate(360);
  delay(1000);
}
int c = 0;
void loop() {
  delay(100);
  //if (c==0){
  //  stepper1.rotate(180, 1);
  //}
}

void processCommand(int commandNumber, int value){
    switch(commandNumber){
       case 0:
       //WAIT
           Serial.print("Command 0 recieved with value: ");
           Serial.println(value);
           break;    
       case 1:
       //RUN SERVO
           Serial.print("Command 1 received with value: ");
           Serial.println(value);
           mainServo.rotate(0, value);
           break;
       case 2:
       //RUN STEPPER BIG
           int dir = 1; //CHECK ACTUAL DIRECTIONS dont know if 
           Serial.print("Command 2 received with value: ");
           Serial.println(value);
           
           if(value <0){
               value = value * (-1); // do abs() if brave
               dir = 0;
           }
           stepper1.rotate(value, dir);
           break;
       case 3:
       //Run radio frequency decoding
           Serial.print("Command 3 received with value: ");
           Serial.println(value);
           break;
       case 4:
       //Run 360 degrees microstepper
           Serial.print("Command 4 received with value: ");
           Serial.println(value);
           micro.rotate(value);
           break;
    //    case 5:
    //    //Run camera tilting microstepper
    //        Serial.print("Command 5 received with value: ");
    //        Serial.println(value);
    //        micro2.rotate(value);
    //        break;
       default:
           Serial.println("Invalid command received");
           break;
    }
}