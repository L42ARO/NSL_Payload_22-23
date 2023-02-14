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
    }
    void rotate(int angle);
    PinList getPins();
    void begin();

  private:
    const int full_rot_count;
    const int delay_btwn_loop;
    const PinList pins;
    static const int rotation_bitmap[8][4];

    // Keeps track of where in the rotation bitmap it is at.
    int current_idx = -1;
};

#endif