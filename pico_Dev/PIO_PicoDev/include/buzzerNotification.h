#ifndef BUZZERNOTIFICATION_H
#define BUZZERNOTIFICATION_H

#include <Arduino.h>

class Buzzer {
public:
    Buzzer(int givenBuzzerPin, int buzzStato = 0, int useBuzzeru = 0, int starto = -1, int currento = 0, int limito = 1000)
        : useBuzzer(useBuzzeru), buzzState(buzzStato), buzzerPin_(givenBuzzerPin), timerStart(starto), timerCurrent(currento), timerLimit(limito)
    {
    };

    ~Buzzer(){//make sure buzzing stops as a destructor
        analogWrite(buzzerPin_, LOW);
    };

    void buzzerNotification();
    void setUseBuzzer(int newUseBuzzer);
    void begin();

private:
    int buzzerPin_;
    int buzzState;
    int useBuzzer;
    int timerStart;
    int timerCurrent;
    int timerLimit;
};

/*

correct usage: 
buzzer objeckt(buzzerPin_, 0,0, -1,0, 1000);
structure: buzzer objeckt(buzzerPin_, int buzzState (default 0), int useBuzzer (default 0), int start (default -1), int current (default 0), int limit (default 1000))

buzzer.buzzerNotification();
-------
buzzer.setUseBuzzer(0);

*/
#endif
