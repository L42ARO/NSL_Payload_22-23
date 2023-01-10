#ifndef MINI_STEPPERS_H
#define MINI_STEPPERS_H
#define MiniBaseDir 2
#define MiniBaseStep 3
#define MiniRegDelay 5000
#define MiniBetweenDelay 250
void setupMiniSteppers();
void MoveMiniBase(int degrees);

#endif