#include <Arduino.h>
#include <Servo.h>
// defines pins numbers
const int stepPin = 6; 
const int dirPin = 5; 
const int microDelay = 1000;
const int betweenDelay = 250;
Servo myservo;

void MoveMotor(int degrees);
void moveServo(int startAngle, int endAngle);

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 200; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(microDelay); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(betweenDelay); 
  }
  delay(1000); // One second delay
  digitalWrite(LED_BUILTIN,LOW);
  digitalWrite(dirPin,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 400; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(microDelay);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(betweenDelay);
  }
  delay(1000);
}

void MoveMotor(int degrees){
  
}

void moveServo(int startAngle, int endAngle) 
{
  const int i = startAngle > endAngle ? -1 : 1;

  for (int pos = startAngle; pos != endAngle; pos+=i) {
    myservo.write(pos);
    delay(15);
  }
}