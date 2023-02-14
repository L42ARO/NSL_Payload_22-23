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
    instance = this;
    instance->processCommand = processCommand;
}

// function that executes whenever data is received from master
void I2C_Comm::receiveEvent(int howMany) {
    if (howMany <= 1) 
        return;
    LinkedList valueBuffer=LinkedList();
    Wire.read();//NULL VALUE
    int commandNumber= Wire.read();
    int sign = Wire.read();
    for (int i = 3; i < howMany; i++) {
        valueBuffer.PushBack(Wire.read());
    }
    int value = valueBuffer[0];
    //int commandNumber = command.substring(0, command.indexOf("_")).toInt();
    //int value = command.substring(command.indexOf("_") + 1).toInt();
    Serial.print("received command:");
    Serial.println(commandNumber);
    // process the commandNumber and value here
    if(sign == 1)
        value *= -1;
    Serial.print(" value:");
    Serial.println(value);
    instance->processCommand(commandNumber, value);
    Wire.write("ready");        // sends ready
    Wire.endTransmission();     // stop transmitting
}