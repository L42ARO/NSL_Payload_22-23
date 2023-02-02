#ifndef MOVESERVO_H
#define MOVESERVO_H

#include <servo.h> 
#include <Arduino.h>
//DONT KNOW IF I NEED TO REINCLUDE ARDUINO.H HERE

class MainServo {
  public:
    MainServo(int pin) 
      : pin(pin)
    {
    }

    void rotate(int startAngle, int endAngle);
    void begin();

  private:
    int pin;
    Servo myservo;
};

#endif