#include<Arduino.h>
#include "i2c_com.h"
#include "LinkedList.h"

#include "buzzerNotification.h"
#include "MoveStepper.h"
#include "MoveServo.h"
#include "mini_steppers.h"
#include "microstepper.h"

I2C_Comm* I2C_Comm::instance =0;

void I2C_Comm::begin(int address) {
    _address = address;
    Wire.begin(_address);                // join i2c bus with address #8
    Wire.onReceive(receiveEvent); // register event
    instance=this;
}

// function that executes whenever data is received from master
void I2C_Comm::receiveEvent(int howMany) {
    if(howMany <=1)
        return;
    LinkedList receivedBits= LinkedList();
    Wire.read(); //First bit is always 0 or NULL char
    Serial.print("Received: ");
    for(int i=1; i<howMany; i++){
        receivedBits.PushBack(Wire.read());
        Serial.print(receivedBits[i-1]);
    }
    Serial.println();
    //First 5 bits say the size of the command bits
    int commandSize = 0;
    for(int i=4; i>=0; i--){
        if(receivedBits[i]!=0)
        commandSize += receivedBits[i] * (1<< i); //1<<i is the same as pow(2, i)
    }
    //Next 5 bits say the size of the value bits
    int valueSize = 0;
    for(int i=0; i<5; i++){
        if(receivedBits[5+i]!=0){
        valueSize += (1<< (4-i));
        Serial.println(i);

        }
    }
    Serial.print("Command size: ");
    Serial.print(commandSize);
    Serial.print(" Value size: ");
    Serial.println(valueSize);

    //Use commandSize and valueSize to get the command and value
    int currentStart = 10;
    int command = 0;
    for(int i=0; i<commandSize; i++){
        if(receivedBits[i+currentStart]!=0)
        command += (1<< (commandSize-i-1));
    }
    //Value comes in as a 2's complement number
    currentStart += commandSize;
    int value = 0;
    bool isNegative = receivedBits[currentStart];
    for (int i =1; i<valueSize-1; i++){//Start form 1 to skip the sign bit
        if(receivedBits[i+currentStart]==0) continue;
        if(isNegative)
            value -= (1<< (valueSize-i-1));
        else
            value += (1<< (valueSize-i-1));
    }
    if(isNegative){
        value ++;
        Serial.println("Negative! ");
    }
    Serial.print("Command: ");
    Serial.print(command);
    Serial.print(" Value: ");
    Serial.println(value);
    //String command = "";
    //for (int i = 0; i < howMany; i++) {
    //  command += (char)Wire.read();
    //}
    //int commandNumber = command.substring(0, command.indexOf("_")).toInt();
    //int value = command.substring(command.indexOf("_") + 1).toInt();
    //Serial.print("received command:");
    //Serial.print(command);
    //int commandNumber = data.substring(0, separatorIndex).toInt();
    //int value = data.substring(separatorIndex + 1).toInt();
    //// process the commandNumber and value here
    //instance->processCommand(commandNumber, value);
    //Wire.write("ready");        // sends ready
    //Wire.endTransmission();     // stop transmitting
}