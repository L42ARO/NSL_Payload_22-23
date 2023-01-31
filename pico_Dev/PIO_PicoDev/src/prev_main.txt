#include <Arduino.h>
#include <Servo.h>
#include<Wire.h>

#include "mini_steppers.h"
#include "MoveStepper.h"
#include "inputToInt.h"
#include "buzzerNotification.h"
#include "MoveServo.h"
#include "MoveStepper.h"
#include "recieveManager.h"
#include "microstepper.h"

// defines pins numbers
const int stepPin = 6; 
const int dirPin = 5; 
Stepper stepper1(stepPin, dirPin); //create stepper object



    
Servo myservo;
char incomingByte = 0;


void setup() {
  setupMiniSteppers();
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  digitalWrite(LED_BUILTIN, HIGH);
}

buzzer time_keeper(buzzerPin);//see buzzerNotification.h


void loop() {
  serialCom();
  time_keeper.buzzerNotification();
}

void serialCom(){
  int moveamount;
  if (Serial.available() > 0) {
    // read the incoming byte:
    //incomingByte = Serial.read();
    String data = Serial.readStringUntil('\n');
    // say what you got:
    Serial.println(data);
    switch (data.charAt(0))
    {
    case '0':{
      //WAITING
      int state = data.charAt(2);
      if(state == '1'){
        useBuzzer = 1;
      }else if(state == '0'){
        useBuzzer = 0;
      }
      Serial.println("High");
      break;
    }
    case '1':{
      //Run servo
      //Third character 
      useBuzzer = 0;
      moveamount = inputToInt(data);
      MoveServo(0, moveamount);
      Serial.println("High");
      break;
    }
    case '2':{
      //Run Stepper Big
      useBuzzer = 0;
      moveamount = inputToInt(data);
      //HOW TO GET DIR?
      /*
      negatives can't really be read in current inttoinput function 
      maybe in mrbluesky if (angle >0) angle = abs(angle)+360
      and here in recieval do:
      if (angle >360) moveamount -=360; dir =0;
      else dir = 1
      */
      int dir = 1; // placeholder
      stepper1.rotate(moveamount, dir)
      Serial.println("High");
      break;
    }
    case '3':{
      //Run radio frequency decoding
      useBuzzer = 0;
      Serial.println("High");
      break;
    }
    case '4':{
      //Run Stepper Small
      useBuzzer = 0;
      moveamount = inputToInt(data);
      MoveMiniBase(moveamount);
      Serial.println("High");
      break;
    }
    case '5':{
      useBuzzer = 0;
      moveamount = inputToInt(data);
      MoveStepper(moveamount, 0);
      Serial.println("High");
      break;
    }
    default:{
      useBuzzer = 0;
      //Undefined value recieved
      Serial.println("Low");
      break;
    }
    }

  }
}

void MoveStepper(int degrees, bool dir = 1){
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

void MoveServo(int startAngle, int endAngle) 
{
  const int i = startAngle > endAngle ? -1 : 1;

  for (int pos{ startAngle }; pos != endAngle; pos+=i) {
    myservo.write(pos);
    delay(15);
  }
  myservo.write(endAngle);
}

void recieveManager(int i){
  while(Wire.available()){
    char c = Wire.read();
    Serial.print(c);
  }
}

int inputToInt(String data){
  int numchar = data.length() - 2;
  int moveamount = 0;
  for(int i=0; numchar > 0; numchar--, i++){
    moveamount += (data.charAt(2+i)-'0') * (pow(10, numchar-1)) ;
  }
  return moveamount;
};