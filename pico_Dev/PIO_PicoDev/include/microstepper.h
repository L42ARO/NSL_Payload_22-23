#ifndef MICRO_H
#define MICRO_H

#include <Arduino.h>

class Microstepper {
  public:
    struct PinList{
      int A_plus;
      int A_minus;
      int B_plus;
      int B_minus;
    };
    Microstepper() = delete;
    Microstepper(int full_rot_count, int delay_btwn_loop, PinList pins)
      : full_rot_count(full_rot_count), delay_btwn_loop(delay_btwn_loop), pins(pins)
    {
      // Calibration to set current_idx to some value.  PI/3 is arbitary.  The microstpeper sometimes overshoot
      // in its first run because current_idx is unknown.
      rotate(30);
      delay(1000);
    }
    void rotate(int angle);
    PinList getPins();
    void begin();

  private:
    const int full_rot_count = 42;
    const int delay_btwn_loop = 50;
    const PinList pins;
    static const double phase_shift_B;   // pi/2
    static const double delta_time_factor;
    static const int rotation_bitmap[8][4];

    // Keeps track of where in the rotation bitmap it is at.
    int current_idx = -1;
};

#endif