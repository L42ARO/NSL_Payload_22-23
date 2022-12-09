#include <Arduino.h>
#include "mini_steppers.h"

unsigned int time_delay = 30;
void setupMiniSteppers(){
    pinMode(in_A_1, OUTPUT);
    pinMode(in_B_1, OUTPUT);
    pinMode(in_A_2, OUTPUT);
    pinMode(in_B_2, OUTPUT);
}
void step1(){
    //A+, B+
    analogWrite(in_A_1, 0);
    analogWrite(in_A_2, 255);
    analogWrite(in_B_1, 255);
    analogWrite(in_B_2, 0);
    delay(time_delay);
}
void step2(){
    //A+, B-
    analogWrite(in_A_1, 0);
    analogWrite(in_A_2, 255);
    analogWrite(in_B_1, 0);
    analogWrite(in_B_2, 255);
    delay(time_delay);
}

void step3(){
    //A-, B-
    analogWrite(in_A_1, 255);
    analogWrite(in_A_2, 0);
    analogWrite(in_B_1, 0);
    analogWrite(in_B_2, 255);
    delay(time_delay);
}

void step4(){
    //A-,B+
    analogWrite(in_A_1, 255);
    analogWrite(in_A_2, 0);
    analogWrite(in_B_1, 255);
    analogWrite(in_B_2, 0);
}

void clockwise(long st){
  long i = 0;
  while( i < st ){
    analogWrite(in_A_2, 255);
    i++;
  }
}

void counter_clockwise(long st){
  long i = 0;
  while( i < st ){
    //step1
    step1();
    //step4
    step4();
    //step3
    step3();
    //step2
    step2();
    delay(50);
    i++;
  }
}