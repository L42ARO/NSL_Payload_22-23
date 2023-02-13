#include <Arduino.h>
#include <i2c_com.h>

I2C_Comm &i2c = I2C_Comm::getInstance();

void setup() {
  Serial.begin(9600);
  i2c.getInstance().begin(8);
}

void loop() {
  delay(100);
}
