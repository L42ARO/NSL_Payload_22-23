#include <Arduino.h>
#include <Servo.h>
#include<Wire.h>
#include "mini_steppers.h"
// defines pins numbers
const int buzzer = 14;
const int stepPin = 6; 
const int dirPin = 5; 
const int microDelay = 5000;
const int betweenDelay = 250;
Servo myservo;
char incomingByte = 0;

int inputToInt(String data);

void MoveServo(int startAngle, int endAngle);
void MoveStepper(int degrees);
class MicroStepper{
  public:
    MicroStepper(int stepPin, int dirPin, int microDelay){

    };
    void step(int steps);
};

void recieveManager(int i);


void setup() {
  setupMiniSteppers();
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  digitalWrite(LED_BUILTIN, HIGH);
}
void serialCom();
void buzzerNotification();

struct timer{
  int start;
  int curr;
  int limit;
};
timer time_keeper = {-1,0,1000};
int buzzState = 0;
int useBuzzer = 0;
int led = 1;
void loop() {
  serialCom();
  buzzerNotification();
  if(led ==1){
    digitalWrite(LED_BUILTIN, HIGH);
    led =0;
  }else{
    digitalWrite(LED_BUILTIN, LOW);
    led =1;
  }
  clockwise(100);
}

void buzzerNotification(){
  if(useBuzzer ==0 ){
    if(buzzState == 1){
      analogWrite(buzzer, LOW);
      buzzState = 0;
    }
    return;
  }
  if(time_keeper.start == -1){
    time_keeper.start = millis();
  }else{
    time_keeper.curr = millis();
    if(time_keeper.curr - time_keeper.start > time_keeper.limit){
      time_keeper.start = time_keeper.curr;
      if(buzzState == 0){
        analogWrite(buzzer, 255);
        buzzState = 1;
      }
      else {
        analogWrite(buzzer, LOW);
        buzzState = 0;
      }
    }
  }
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
      MoveStepper(moveamount);
      Serial.println("High");
      break;
    }
    case '3':{
      //Run radio frequency decoding
      useBuzzer = 0;
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

void MoveStepper(int degrees){
  int steps = double((degrees*200)/360);
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  
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