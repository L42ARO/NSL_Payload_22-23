#include <Arduino.h>
#include "mini_steppers.h"
void setupMiniSteppers(){
  pinMode(MiniBaseDir,OUTPUT); 
  pinMode(MiniBaseStep,OUTPUT);
}
void MoveMiniBase(int degrees){
  int steps = double((degrees*200)/360);
  if(steps > 0){
    digitalWrite(MiniBaseDir,HIGH); // Enables the motor to move in a particular direction
  }else{
    digitalWrite(MiniBaseDir,LOW); // Enables the motor to move in a particular direction
  }
  for(int i =0; i<steps; i++){
    digitalWrite(MiniBaseStep,HIGH); 
    delayMicroseconds(MiniRegDelay);
    digitalWrite(MiniBaseStep,LOW); 
    delayMicroseconds(MiniBetweenDelay);
  }
}

