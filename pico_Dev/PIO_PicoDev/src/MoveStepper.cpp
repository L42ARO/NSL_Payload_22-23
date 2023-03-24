#include "MoveStepper.h"
#include <Arduino.h> 

Stepper::Stepper(const int stepPinu, const int dirPinu, const int rstPinu)
    : stepPin_(stepPinu), dirPin_(dirPinu) , rstPin_(rstPinu)
{
}

void Stepper::begin()
{
    pinMode(dirPin_, OUTPUT);
    pinMode(stepPin_, OUTPUT);
    pinMode(rstPin_ , OUTPUT);
    digitalWrite(rstPin_, HIGH);
}

void Stepper::rotate(int degrees)
//~HinazukiKayo: if a negative value is passed then we would have to change the other function that gives us the final angle to move, to also give back a bool instead of a negative value. Maybe it would be better to just handle it in this function as in if degrees<0 then dir = 1 idfk?
{
    if(degrees == 0) return;
    //If degrees negative dir=0 else dir=1
    bool dir = degrees > 0 ? 1 : 0;
    double steps = double(degrees/360.0)*200.0; // 200 steps per rotation  
    if(steps==0) return;
    if(steps<0) steps = steps * -1;
    Serial.println("Steps: " + String(steps));
    if(dir) digitalWrite(dirPin_,HIGH); // Enables the motor to move in a particular direction
    else digitalWrite(dirPin_, LOW);
  
  // Makes 200 pulses for making one full cycle rotation
    for(double x = 0; x < steps; x++) {
        digitalWrite(stepPin_, HIGH); 
        delayMicroseconds(microDelay); 
        digitalWrite(stepPin_, LOW); 
        delayMicroseconds(betweenDelay); 
    }
    delay(2000);
}

// Never called.
Stepper::~Stepper()
{
    // making sure stepper stop
    digitalWrite(stepPin_, LOW);
    digitalWrite(dirPin_, LOW);
}

/*
ideal usage:
int main(){
    MoveStepper stepper1(steppin, dirpin); //create stepper object

    stepper1.rotate(180, 1) // move stepper motor 180 deg
    
    //complicated uses (loops) do delete stepper1;
    return 0;
}

*/