#include <Arduino.h>

/************ Microstepper Class ****************/
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
      rotate(PI/3, true);
      delay(1000);
    }
    void rotate(double angle, bool clockwise);

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

// Initializing static member variables in Microstepper class.
const double Microstepper::phase_shift_B = 1.5708;
const double Microstepper::delta_time_factor = 0.3;
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

void Microstepper::rotate(double angle, bool clockwise)
{
  int steps{ round(angle / (2*PI) * full_rot_count) };
  if (current_idx == -1) 
    current_idx = clockwise ? 0 : 7;

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

/*************** Microstepper Class End *********************/

void setup()
{
  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);

  Serial.begin(9600);
}

int count = 0;
// steps = 42.  delay = 50 or 500

void loop()
{
  Microstepper stepper1(42, 50, {3, 11, 9, 10});

  if(count <= 0) {
    Serial.print("\nStarting: ");
    Serial.println(count);

    // stepper1.rotate(PI/2, true);
    // delay(2000);
    // stepper1.rotate(PI/2, true);
    // delay(2000);
    // stepper1.rotate(PI/2, true);
    // delay(2000);
    // stepper1.rotate(PI/2, true);
    // delay(2000);

    // stepper1.rotate(2*PI, false);
    // delay(2000);
    // stepper1.rotate(2*PI, true);
    // delay(2000);

    stepper1.rotate(PI/3, true);
    delay(2000);
    stepper1.rotate(PI/3, true);
    delay(2000);
    stepper1.rotate(PI/3, true);
    delay(2000);
    stepper1.rotate(PI/3, false);
    delay(2000);
    stepper1.rotate(PI/3, false);
    delay(2000);
    stepper1.rotate(PI/3, false);
    delay(2000);
  }

  count = 0;
  delay(2000);
}