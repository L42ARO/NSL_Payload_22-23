#ifndef MOVESERVO_H
#define MOVESERVO_H

#include <servo.h> 
//DONT KNOW IF I NEED TO REINCLUDE ARDUINO.H HERE

void MoveServo(int startAngle, int endAngle) 
{
  const int i = startAngle > endAngle ? -1 : 1;

  for (int pos{ startAngle }; pos != endAngle; pos+=i) {
    myservo.write(pos);
    delay(15);
  }
  myservo.write(endAngle);
}
//saving space by excluding implementation 

#endif