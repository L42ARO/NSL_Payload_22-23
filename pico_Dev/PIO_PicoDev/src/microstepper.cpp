#include <Arduino.h>
#include "microstepper.h"

// Initializing static member variables in Microstepper class.
const int Microstepper::rotation_bitmap[8][4] = {
      {HIGH, LOW, LOW, LOW},
      {HIGH, LOW, HIGH, LOW},
      {LOW, LOW, HIGH, LOW},
      {LOW, HIGH, HIGH, LOW},
      {LOW, HIGH, LOW, LOW},
      {LOW, HIGH, LOW, HIGH},
      {LOW, LOW, LOW, HIGH},
      {HIGH, LOW, LOW, HIGH}
};

void Microstepper::rotate(int angle)
{
  bool clockwise{ angle < 0 };
  int steps{  angle / 360 * full_rot_count };

  if (current_idx == -1) 
    current_idx = clockwise ? 0 : 7;
  else
    clockwise ? ++current_idx : --current_idx;

  for (int i{0}; i < steps; ++i) {
    digitalWrite(pins.A_plus, rotation_bitmap[current_idx][0]);
    digitalWrite(pins.A_minus, rotation_bitmap[current_idx][1]);
    digitalWrite(pins.B_plus, rotation_bitmap[current_idx][2]);
    digitalWrite(pins.B_minus, rotation_bitmap[current_idx][3]);
    
    // Increment if clockwise is true, decrement if false
    clockwise ? ++current_idx : --current_idx;

    if (current_idx < 0) {
      current_idx = 7;
    }
    else if (current_idx > 7) {
      current_idx = 0;
    }
  
    delay(delay_btwn_loop);
  }

  // Undo last increment because rotation direction might change
  clockwise ? --current_idx : ++current_idx;
}

// probably not needed
Microstepper::PinList Microstepper::getPins()
{
  return pins;
}

void Microstepper::begin()
{
  pinMode(pins.A_plus, OUTPUT);
  pinMode(pins.A_minus, OUTPUT);
  pinMode(pins.B_plus, OUTPUT);
  pinMode(pins.B_minus, OUTPUT);

  // Calibration to set current_idx to some value.  30 degrees is arbitary.  The microstpeper overshoots
  /// in its first run because current_idx is unknown.
  rotate(30);
  delay(1000);
}