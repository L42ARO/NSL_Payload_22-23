#ifndef MINI_STEPPERS_H
#define MINI_STEPPERS_H
#define in_A_1 10
#define in_B_1 11
#define in_A_2 12
#define in_B_2 13
void setupMiniSteppers();
void step1();
void step2();
void step3();
void step4();
void clockwise(long st);
void counter_clockwise(long st);

#endif