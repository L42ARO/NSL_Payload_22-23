#ifndef BUZZERNOTIFICATION_H
#define BUZZERNOTIFICATION_H

#include <Arduino.h>

class buzzer{
public:
    const int buzzerPin_;
    int buzzState;
    int useBuzzer;
    int timerStart;
    int timerCurrent;
    int timerLimit;

    buzzer(const int givenBuzzerPin, int buzzStato = 0, int useBuzzeru = 0, int starto = -1, int currento = 0, int limito = 1000){
        useBuzzer = useBuzzeru;
        buzzState = buzzStato;
        buzzerPin_ = givenBuzzerPin;
        timerStart = starto;
        timerCurrent = currento;
        timerLimit = limito;
    };

    ~buzzer(){//make sure buzzing stops as a destructor
        analogWrite(buzzerPin_, LOW);
    };

    void buzzerNotification(){ 
        if(useBuzzer ==0 ){
            if(buzzState == 1){
                analogWrite(buzzerPin_, LOW);
                buzzState = 0;
            }
            return;
        }

        if(timerStart == -1){
            timerStart = millis();
        }else{
            timerCurrent = millis();
            if(timerCurrent - timerStart > timerLimit){
                timerStart = timerCurrent;
                if(buzzState == 0){
                    analogWrite(buzzerPin_, 255);
                    buzzState = 1;
                } else {
                    analogWrite(buzzerPin_, LOW);
                    buzzState = 0;
                }
            }
        }
    }

    void setUseBuzzer( int newUseBuzzer){
        useBuzzer = newUseBuzzer;
    }
}

/*

correct usage: 
buzzer objeckt(buzzerPin_, 0,0, -1,0, 1000);
structure: buzzer objeckt(buzzerPin_, int buzzState (default 0), int useBuzzer (default 0), int start (default -1), int current (default 0), int limit (default 1000))

buzzer.buzzerNotification();
-------
buzzer.setUseBuzzer(0);

*/
#endif
