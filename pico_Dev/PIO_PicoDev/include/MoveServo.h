#ifndef MOVESERVO_H
#define MOVESERVO_H

#include <servo.h> 
//DONT KNOW IF I NEED TO REINCLUDE ARDUINO.H HERE

class MainServo {
  public:
    void rotate(int startAngle, int endAngle) 
    {
      const int i = startAngle > endAngle ? -1 : 1;

      for (int pos{ startAngle }; pos != endAngle; pos+=i) {
        myservo.write(pos);
        delay(15);
      }
      myservo.write(endAngle);
    }

  private:
    Servo myservo;
};

#endif