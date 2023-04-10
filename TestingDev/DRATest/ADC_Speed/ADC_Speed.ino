#include <Arduino.h>

inline int analogReadDirect(uint8_t pin) {
  ADMUX = (pin & 0x07) | (1 << REFS0);
  ADCSRA |= (1 << ADEN) | (1 << ADSC);

  while (ADCSRA & (1 << ADSC));
  return ADC;
}
// Number of samples to take for the test
const unsigned long num_samples = 10000;
unsigned long start_time;
unsigned long end_time;
double sampling_rate;
int first_readings[10];
int last_readings[10];

void setup() {
  Serial.begin(500000);
  while (!Serial);

  // Start the test
  start_time = micros();
  for (unsigned long i = 0; i < num_samples; i++) {
    int reading = analogRead(A0);
    if (i < 10) {
      first_readings[i] = reading;
    } else if (i >= num_samples - 10) {
      last_readings[i - (num_samples - 10)] = reading;
    }
    byte high_byte = reading >> 8;
    byte low_byte = reading & 0xFF;
    Serial.write(high_byte);
    Serial.write(low_byte);
  }
  end_time = micros();

  // Calculate the sampling rate
  sampling_rate = 1000000.0 * num_samples / (end_time - start_time);

  // Print the human-readable text section
  Serial.write('<');
  Serial.print("Time taken: ");
  Serial.print(end_time - start_time);
  Serial.println(" us");
  Serial.print("Sampling rate: ");
  Serial.print(sampling_rate);
  Serial.println(" samples/s");
  Serial.print("First 10 readings: ");
  for (int i = 0; i < 10; i++) {
    Serial.print(first_readings[i]);
    Serial.print(" ");
  }
  Serial.println();
  Serial.print("Last 10 readings: ");
  for (int i = 0; i < 10; i++) {
    Serial.print(last_readings[i]);
    Serial.print(" ");
  }
  Serial.println();
  Serial.write('>');
}

void loop() {
}
