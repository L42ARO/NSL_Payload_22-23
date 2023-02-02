#include <Wire.h>
#include <i2c_com.h>

#include "buzzerNotification.h"
#include "MoveStepper.h"
#include "MoveServo.h"
#include "mini_steppers.h"

const int buzzerPin = 14;
const int stepPin = 6; 
const int dirPin = 5; 
Stepper stepper1(stepPin, dirPin); //create stepper object
MainServo mainServo(9);
buzzer time_keeper(buzzerPin); //create buzzer object


I2C_Comm* I2C_Comm::instance = 0;
I2C_Comm::I2C_Comm() {
    instance = this;
}
void I2C_Comm::begin() {
    Wire.begin(_address);                // join i2c bus with address #8
    Wire.onReceive(receiveEvent); // register event
}

void I2C_Comm::loop() {
  delay(100);
}

// function that executes whenever data is received from master
void I2C_Comm::receiveEvent(int howMany) {
  char buffer[20];
  int count = 0;
  while (Wire.available()) { // loop through all but the last
    buffer[count++] = Wire.read();
  }
  buffer[count] = '\0';
  String data = String(buffer);
  int separatorIndex = data.indexOf("_");
  if(separatorIndex > 0){
    int commandNumber = data.substring(0, separatorIndex).toInt();
    int value = data.substring(separatorIndex + 1).toInt();
    // process the commandNumber and value here
    processCommand(commandNumber, value);
    // ...
    Wire.beginTransmission(_address); // transmit to device #8
    Wire.write("ready");        // sends ready
    Wire.endTransmission();     // stop transmitting
    Serial.println("received command and sent ready");
  }
}
void I2C_Comm::processCommand(int commandNumber, int value){
    switch(commandNumber){
        case 0:
        //WAIT
            Serial.print("Command 0 recieved with value: ");
            Serial.println(value);
            if(value == '1'){
                time_keeper.setUseBuzzer(1);
            }else if(value == '0'){
                time_keeper.setUseBuzzer(0);
            }
            break;
        case 1:
        //RUN SERVO
            Serial.print("Command 1 received with value: ");
            Serial.println(value);
            time_keeper.setUseBuzzer(0);
            mainServo.rotate(0, value);
            break;
        case 2:
        //RUN STEPPER BIG
            int dir = 1; //CHECK ACTUAL DIRECTIONS dont know if 
            Serial.print("Command 2 received with value: ");
            Serial.println(value);
            time_keeper.setUseBuzzer(0);
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
            time_keeper.setUseBuzzer(0);
            break;
        case 4:
        //Run Stepper Small
            Serial.print("Command 4 received with value: ");
            Serial.println(value);
            time_keeper.setUseBuzzer(0);
            MoveMiniBase(value);
            break;
        default:
            time_keeper.setUseBuzzer(0);
            Serial.println("Invalid command received");
            break;
    }
}
