#include <Arduino.h>

const int full_rot_count{ 20 };
const int delay_btwn_loop{ 300 };
const double phase_shift_B{ 1.5708 };   // pi/2
const double delta_time_factor{ 0.3 };

enum class Micro1pins {
    A_plus = 3, A_minus = 11, B_plus = 9, B_minus = 10
};

enum class Micro2pins {
    A_plus = A0, A_minus = A1, B_plus = A2, B_minus = A3
};

void moveMicrostepper1(double angle, bool clockwise);
void moveMicrostepper2(double angle, bool clockwise);

void setup()
{
  pinMode((int)Micro1pins::A_plus, OUTPUT);
  pinMode((int)Micro1pins::A_minus, OUTPUT);
  pinMode((int)Micro1pins::B_plus, OUTPUT);
  pinMode((int)Micro1pins::B_minus, OUTPUT);

  Serial.begin(9600);
}

int count = 0;
void loop(){
  if(count <= 0) {
    Serial.print("Calling: ");
    Serial.println(count);
    moveMicrostepper2(PI/2, false);
  }
  count = 2;
}


void moveMicrostepper1(double angle, bool clockwise)
{
  int steps{ round(angle / (2*PI) * full_rot_count) };
  float starttime{ millis() };

  for (int i{0}; i < steps; ++i) {
    float floatTime = float(millis()) - starttime;
    float A = (sin((floatTime * delta_time_factor) )) * 255;
    float B = (sin((floatTime * delta_time_factor) + phase_shift_B)) * 255;
  
    if (!clockwise)  {
      analogWrite((int)Micro1pins::A_plus, max(0, A));
      analogWrite((int)Micro1pins::A_minus, max(0,-A));
      analogWrite((int)Micro1pins::B_plus, max(0, B));
      analogWrite((int)Micro1pins::B_minus, max(0,-B));
    }
    else {
      analogWrite((int)Micro1pins::A_plus, max(0, -B));
      analogWrite((int)Micro1pins::A_minus, max(0, B));
      analogWrite((int)Micro1pins::B_plus, max(0, -A));
      analogWrite((int)Micro1pins::B_minus, max(0, A));
    }
    delay(delay_btwn_loop);
  }
}

void moveMicrostepper2(double angle, bool clockwise)
{
  int steps = round(angle / (2*PI) * full_rot_count);
  float starttime = millis();

  for (int i=0; i < steps; ++i) {
    Serial.println(i);
    float floatTime = float(millis()) - starttime;
    float A = (sin((floatTime * delta_time_factor) )) * 255;
    float B = (sin((floatTime * delta_time_factor) + phase_shift_B)) * 255;
  
    if (!clockwise) {
      analogWrite((int)Micro2pins::A_plus, max(0, A));
      analogWrite((int)Micro2pins::A_minus, max(0,-A));
      analogWrite((int)Micro2pins::B_plus, max(0, B));
      analogWrite((int)Micro2pins::B_minus, max(0,-B));
    }
    else {
      analogWrite((int)Micro2pins::A_plus, max(0, -B));
      analogWrite((int)Micro2pins::A_minus, max(0, B));
      analogWrite((int)Micro2pins::B_plus, max(0, -A));
      analogWrite((int)Micro2pins::B_minus, max(0, A));
    }

    delay(delay_btwn_loop);
  }
}
