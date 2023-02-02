#ifndef BUZZER_H
#define BUZZER_H

#include <Arduino.h>
#include "buzzerNotification.h"

void Buzzer::buzzerNotification()
{
    if (useBuzzer == 0) {
        if(buzzState == 1){
            analogWrite(buzzerPin_, LOW);
            buzzState = 0;
        }
        return;
    }

    if (timerStart == -1) {
        timerStart = millis();
    }
    else {
        timerCurrent = millis();
        if (timerCurrent - timerStart > timerLimit) {
            timerStart = timerCurrent;
            if (buzzState == 0) {
                analogWrite(buzzerPin_, 255);
                buzzState = 1;
            } else {
                analogWrite(buzzerPin_, LOW);
                buzzState = 0;
            }
        }
    }
}

void Buzzer::setUseBuzzer(int newUseBuzzer)
{
    useBuzzer = newUseBuzzer;
}

void Buzzer::begin()
{
    pinMode(buzzerPin_, OUTPUT);
}

#endif  // BUZZER_H