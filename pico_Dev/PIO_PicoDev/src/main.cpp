#include <Arduino.h>
#include "i2c_com.h"

I2C_Comm i2c;

void setup(){
  i2c.begin();
}

void loop(){
  
  i2c.loop();
}