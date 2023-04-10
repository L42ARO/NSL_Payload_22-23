#include <Wire.h>

void setup() {
  Wire.begin(); // join i2c bus (address optional for master)
  Serial.begin(9600);
}

void loop() {
  Wire.beginTransmission(8); // transmit to device #8
  Wire.write("Hello Raspberry Pi!"); // sends the string
  Wire.endTransmission(); // stop transmitting

  delay(1000);
}