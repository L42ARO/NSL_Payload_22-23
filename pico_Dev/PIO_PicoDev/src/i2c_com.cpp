#include<Arduino.h>
#include "i2c_com.h"
#include "LinkedList.h"

#include "buzzerNotification.h"
#include "MoveStepper.h"
#include "MoveServo.h"
#include "mini_steppers.h"
#include "microstepper.h"

I2C_Comm* I2C_Comm::instance =0;

void I2C_Comm::begin(int address, void (*processCommand)(int, int)) {
    _address = address;
    Wire.begin(_address);                // join i2c bus with address #8
    Wire.onReceive(receiveEvent); // register event
    instance=this;
    instance->processCommand = processCommand;
}

// function that executes whenever data is received from master
void I2C_Comm::receiveEvent(int howMany) {
    if (howMany <= 1) 
        return;
    String command = "";
    Wire.read();
    for (int i = 0; i < howMany; i++) {
     command += (char)Wire.read();
    }
    int commandNumber = command.substring(0, command.indexOf("_")).toInt();
    int value = command.substring(command.indexOf("_") + 1).toInt();
    Serial.print("received command:");
    Serial.print(command);
    // process the commandNumber and value here
    instance->processCommand(commandNumber, value);
    Wire.write("ready");        // sends ready
    Wire.endTransmission();     // stop transmitting
}