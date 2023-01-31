#ifndef MOVESTEPPER_H
#define MOVESTEPPER_H

class Stepper
{
public:
    Stepper(const int stepPinu, const int dirPinu);
    ~Stepper();
    void rotate(int degrees, bool dir = 1);
private:
    const int stepPin_;
    const int dirPin_;
    static const int microDelay = 5000;
    static const int betweenDelay = 250;
};

#endif