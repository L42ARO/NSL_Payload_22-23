#ifndef RECIEVEMANAGER_H
#define RECIEVEMANAGER_H

#include <Arduino.h>
#include <Wire.h>

void recieveManager(int i){
  while(Wire.available()){
    char c = Wire.read();
    Serial.print(c);
  }
}

#endif