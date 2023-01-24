#include <Arduino.h>

/************ Microstepper Class****************/
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
    {}
    void rotate(double angle, bool clockwise);

  private:
    int ClockwiseBitmap[8][4] = {
      {HIGH, LOW, LOW, LOW},
      {HIGH, LOW, HIGH, LOW},
      {LOW, LOW, HIGH, LOW},
      {LOW, HIGH, HIGH, LOW},
      {LOW, HIGH, LOW, LOW},
      {LOW, HIGH, LOW, HIGH},
      {LOW, LOW, LOW, HIGH},
      {HIGH, LOW, LOW, HIGH}      
    };
    const int full_rot_count;
    const int delay_btwn_loop;
    const PinList pins;
    static const double phase_shift_B;   // pi/2
    static const double delta_time_factor;
};

// Initializing static member variables in Microstepper class.
const double Microstepper::phase_shift_B = 1.5708;
const double Microstepper::delta_time_factor = 0.3;

void Microstepper::rotate(double angle, bool clockwise)
{
  int steps{ round(angle / (2*PI) * full_rot_count) };
  float starttime{ millis() };

  int vel_delay = 50;
  int step_idx = clockwise ? 0 : 7;
  for (int i{0}; i < steps; ++i) {
    float floatTime = float(millis()) - starttime;
    float A = (sin((floatTime * delta_time_factor) )) * 255;
    float B = (sin((floatTime * delta_time_factor) + phase_shift_B)) * 255;
  
    if (!clockwise)  {
      digitalWrite(pins.A_plus, ClockwiseBitmap[step_idx][0]);
      digitalWrite(pins.A_minus, ClockwiseBitmap[step_idx][1]);
      digitalWrite(pins.B_plus, ClockwiseBitmap[step_idx][2]);
      digitalWrite(pins.B_minus, ClockwiseBitmap[step_idx][3]);
      delay(vel_delay);
      step_idx--;
      if (step_idx < 0) {
        step_idx = 7;
      }
    }
    else {
      digitalWrite(pins.A_plus, ClockwiseBitmap[step_idx][0]);
      digitalWrite(pins.A_minus, ClockwiseBitmap[step_idx][1]);
      digitalWrite(pins.B_plus, ClockwiseBitmap[step_idx][2]);
      digitalWrite(pins.B_minus, ClockwiseBitmap[step_idx][3]);
      delay(vel_delay);
      step_idx++;
      if (step_idx % 8 == 0 && step_idx != 0) {
        step_idx = 0;
      }

      // analogWrite(pins.A_plus, max(0, -B));
      // analogWrite(pins.A_minus, max(0, B));
      // analogWrite(pins.B_plus, max(0, -A));
      // analogWrite(pins.B_minus, max(0, A));
    }
    //delay(delay_btwn_loop);
  }
}

/*************** Microstepper Class End *********************/


void moveMicrostepper1(double angle, bool clockwise);
void moveMicrostepper2(double angle, bool clockwise);

void setup()
{
  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);

  Serial.begin(9600);
}

int count = 0;
void loop(){

  Microstepper digitalMicro(42, 300, {3, 11, 9, 10});
  Microstepper analogMicro(15, 300, {A0, A1, A2, A3});

  if(count <= 0) {
    Serial.print("Calling: ");
    Serial.println(count);
    //analogMicro.rotate(2*PI, true);
    digitalMicro.rotate(2*PI, false);
  }
  count=2;

    // float floatTime = float(millis());
    // static float starttime = floatTime;
    // float A = (sin((floatTime * 0.03))) * 255;
    // float B = (sin((floatTime * 0.03) + 1.5708)) * 255;

    // //if (floatTime*0.03 < starttime*0.03 + 2*PI) {
    //   if (count >= 0 && count < 25) {
    //     Serial.print("Current time: ");
    //     Serial.println(floatTime);
    //     Serial.print("Start time: ");
    //     Serial.println(starttime);
    //     Serial.println(count);
    
    //     analogWrite(3, max(0, A));
    //     analogWrite(11, max(0,-A));
    //     analogWrite(9, max(0, B));
    //     analogWrite(10, max(0,-B));
    //   }
   // }
}