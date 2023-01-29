#include "MoveStepper.h"
#include <Arduino.h> 

Stepper::Stepper(const int stepPinu, const int dirPinu){
    stepPin_ = stepPinu;
    dirPin_ = dirPinu;
}

Stepper::rotate(int degrees, bool dir = 1)
//~HinazukiKayo: if a negative value is passed then we would have to change the other function that gives us the final angle to move, to also give back a bool instead of a negative value. Maybe it would be better to just handle it in this function as in if degrees<0 then dir = 1 idfk?
{
    if(degrees < 0 || degrees >360){
        Serialprintln("Illogical degree input given");
    }
    int steps = double((degrees*200)/360);
    if(dir) digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
    else digitalWrite(dirPin, LOW);
  
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < steps; x++) {
        digitalWrite(stepPin,HIGH); 
        delayMicroseconds(microDelay); 
        digitalWrite(stepPin,LOW); 
        delayMicroseconds(betweenDelay); 
        }
  delay(2000);
}

Stepper::~Stepper()
{
    // making sure stepper stop
    digitalWrite(stepPin, LOW);
    digitalWrite(dirPin, LOW);
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

#endif 