#ifndef SERVO_H
#define SERVO_H

#include <servo.h>
#include "MoveServo.h"

void MainServo::rotate(int startAngle, int endAngle) 
{
    const int i = startAngle > endAngle ? -1 : 1;

    for (int pos{ startAngle }; pos != endAngle; pos+=i) {
        myservo.write(pos);
        delay(15);
    }
    myservo.write(endAngle);
}

void MainServo::begin()
{
    pinMode(pin, OUTPUT);
    myservo.attach(pin);
}

#endif  // SERVO_H