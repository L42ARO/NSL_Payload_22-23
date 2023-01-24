#include <Wire.h>
#include <i2c_com.h>

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
        case 1:
            Serial.print("Command 1 received with value: ");
            Serial.println(value);
            break;
        case 2:
            Serial.print("Command 2 received with value: ");
            Serial.println(value);
            break;
        case 3:
            Serial.print("Command 3 received with value: ");
            Serial.println(value);
            break;
        case 4:
            Serial.print("Command 4 received with value: ");
            Serial.println(value);
            break;
        case 5:
            Serial.print("Command 5 received with value: ");
            Serial.println(value);
            break;
        default:
            Serial.println("Invalid command received");
    }
}
