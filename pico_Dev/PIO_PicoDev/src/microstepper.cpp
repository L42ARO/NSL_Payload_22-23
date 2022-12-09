#include <Arduino.h>
#include <cmath>

void setup() {
    pinMode(3 , OUTPUT);
    pinMode(11, OUTPUT);
    pinMode(9 , OUTPUT);
    pinMode(10, OUTPUT);
}
void loop() {
    float floatTime = float(millis());
    float A = (sin((floatTime * 0.03) )) * 255;
    float B = (sin((floatTime * 0.03) + 1.5708)) * 255;
    analogWrite(3, max(0, A));
    analogWrite(11, max(0,-A));
    analogWrite(9, max(0, B));
    analogWrite(10, max(0,-B));
}