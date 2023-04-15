#include <Arduino.h>

#include "i2c_com.h"
#include "MoveStepper.h"
#include "MoveServo.h"
#include "buzzerNotification.h"
#include "microstepper.h"
//#include "draManager.h"

I2C_Comm &i2c = I2C_Comm::getInstance();
const int stepPin = 11; 
const int dirPin = 10; 
const int rstPin = 12;
Stepper stepper1(stepPin, dirPin, rstPin); //create stepper object
MainServo mainServo(9);
Microstepper micro(42, 500, {3, 5, 4, 6});    // purpose, yellow, orange green or blue, black, red, white
//3,11,9,10

//DRA PINS
//const int PTT_PIN 2; // PTT control pin
//const int PD_PIN 7; // PD pin
//const int SQ_PIN 5; //Squelch pin
//const int HL_PIN 6;

bool readingRF = false;

void processCommand(int commandNumber, int value);

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  i2c.begin(8, &processCommand);

  // Setting the pins up
  micro.begin();
  stepper1.begin();
  mainServo.begin();
  //micro.rotate(360);
  delay(1000);
}
int c = 0;

//DRA Behelit= new DRA(PTT_PIN,SQ_PIN,HL_PIN); // SET UP DRA OBJECT NOW CALLED BEHELIT

void loop() {
    if(readingRF) { 
        // if(Behelit.get_State() == 4){
        //     Behelit.squelch_Loop();
        //     return;
        // } else if( Behelit.get_State() == 1){
        //     if(Behelit.Handshake()){
        //         Behelit++;
        //     }
        // } else if (Behelit.get_State() == 2){
        //     if(Behelit.SetVolume()){
        //         Behelit++;
        //     }
        // } else if (Behelit.get_State() == 3){
        //     if(Behelit.SetFilter()){
        //         Behelit++;
        //         Serial.write(">");
        //     }
        // }

        // return; //this return error?
    }
    delay(100);
}


void processCommand(int commandNumber, int value){
    Serial.println("Processing command");
    switch(commandNumber){
       case 0:
       //WAIT
           Serial.print("Command 0 recieved with value: ");
           Serial.println(value);
           break;    
       case 1:
       //RUN SERVO
           Serial.print("Command 1 received with value: ");
           Serial.println(value);
           mainServo.rotate(0, value);
           break;
       case 2:
       //RUN STEPPER BIG
           Serial.print("Command 2 received with value: ");
           Serial.println(value);
           stepper1.rotate(value);
           break;
       case 3:
       //Run 360 degrees microstepper
           Serial.print("Command 3 received with value: ");
           Serial.println(value);
           micro.rotate(value);
           break;
       case 4:
       //once case is called int rfreciever is set to true and i2c communication is stopped
            readingRF = true;
            i2c.end();
            break;
       default:
           Serial.println("Invalid command received");
           break;
    }
}