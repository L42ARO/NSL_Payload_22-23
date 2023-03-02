#ifndef MOVESTEPPER_H
#define MOVESTEPPER_H

class Stepper
{
public:
    Stepper(const int stepPinu, const int dirPinu, const int rstPinu);
    ~Stepper();
    void rotate(int degrees, bool dir = 1);
    void begin();

private:
    const int stepPin_;
    const int dirPin_;
    const int rstPin_;
    static const int microDelay = 5000;
    static const int betweenDelay = 250;
};

#endif