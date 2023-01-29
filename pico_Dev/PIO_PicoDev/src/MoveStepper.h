#ifndef MOVESTEPPER_H
#define MOVESTEPPER_H

class Stepper
{
public:
    int degrees;
    bool dir;
    const int stepPin_;
    const int dirPin_;
    Stepper(const int stepPinu, const int dirPinu);
    ~Stepper();
    void rotate(int degrees, bool dir = 1);
};

#endif