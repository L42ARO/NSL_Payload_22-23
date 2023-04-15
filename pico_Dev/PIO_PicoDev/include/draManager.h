#ifndef DRAMANAGER_H
#define DRAMANAGER_H

#include <SoftwareSerial.h>
#include <arduino.h>

class DRA {
    private:
        int state;
        int PTT_PIN;
        int SQ_PIN;
        int HL_PIN;
        volatile bool squelch = false;
        volatile unsigned long lastPrintTime = 0;
        volatile unsigned long squelch_start = 0;
        volatile unsigned long curr_sr = 0;
    public:

        void operator+(int add_To_State) { 
            state = state + add_To_State;
            return;
        }
        void operator++(){
            state++;
        }

        DRA(int PTT_PIN_, int SQ_PIN_, int HL_PIN_, int state_ = 0) : PTT_PIN(PTT_PIN_), SQ_PIN(SQ_PIN_), HL_PIN(HL_PIN_), state(state_){
            SoftwareSerial dra(3,4); // will make it difficult to declare different DRA classes. find out if leaving a string variable typename instead of "dra" will work
            pinMode(PTT_PIN, OUTPUT); // Set the PTT pin as an output
            pinMode(PD_PIN, OUTPUT); // Set the PD pin as an output
            pinMode(HL_PIN, OUTPUT);
            pinMode(SQ_PIN, INPUT);
            digitalWrite(PD_PIN, HIGH); // Set the PD pin to a high state
            digitalWrite(PTT_PIN, HIGH); // Set the module to RX mode initially
            analogWrite(HL_PIN, 150);
            delay(500);
            dra.begin(9600);
        }
        int get_State() const { return state;}
        bool HandShake();
        bool SetFilter();
        bool SetFrequency();
        bool SetVolume()

        void squelch_Loop();

        String getmessages();
        void SendCommand(String cmd);
}

#endif