#include <Arduino.h>
#include <Servo.h>
#include<Wire.h>
// defines pins numbers
const int stepPin = 6; 
const int dirPin = 5; 
const int microDelay = 1000;
const int betweenDelay = 500;
Servo myservo;

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
  Wire.begin(2);
  Wire.onReceive(recieveManager);
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(0);
}

void loop() {
  delay(100);
}

void MoveStepper(int degrees){
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 100; x++) {
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