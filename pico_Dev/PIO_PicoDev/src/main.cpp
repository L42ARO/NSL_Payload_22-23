#include <Arduino.h>
#include <Servo.h>
#include<Wire.h>
// defines pins numbers
const int stepPin = 6; 
const int dirPin = 5; 
const int microDelay = 1000;
const int betweenDelay = 500;
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
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(0);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  int moveamount;
  if (Serial.available() > 0) {
    // read the incoming byte:
    //incomingByte = Serial.read();
    String data = Serial.readStringUntil('\n');
    // say what you got:
    Serial.print(data);
    switch (data.charAt(0))
    {
    case '0':{
      //WAITING
      break;
    }
    case '1':{
      //Run servo
      //Third character 
      moveamount = inputToInt(data);
      MoveServo(0, moveamount);
      Serial.print("High");
      break;
    }
    case '2':{
      //Run Stepper Big
      moveamount = inputToInt(data);
      MoveStepper(moveamount);
      Serial.print("High");
      break;
    }
    case '3':{
      //Run radio frequency decoding
      Serial.print("High");
      break;
    }
    default:{
      //Undefined value recieved
      Serial.print("Low");
      break;
    }
    }

  }
}

void MoveStepper(int degrees){
  int steps = degrees * (200/360);
  digitalWrite(LED_BUILTIN, HIGH);
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