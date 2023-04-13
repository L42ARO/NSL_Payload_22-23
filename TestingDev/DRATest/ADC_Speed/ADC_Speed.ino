const int analogPin = A0;
const int baudRate = 500000;
unsigned long startTime;
int counter = 0;

void setup() {
  Serial.begin(500000);
  Serial.println("test");
  startTime = micros();
  ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
  ADCSRA &= ~(1 << ADPS0);
  
}
bool esc=false;
void loop() {

  if(esc){
    return;
  }
  
  if (counter >= 10000) {
    unsigned long elapsedTime = micros() - startTime;
    float sampleRate = counter / (elapsedTime / 1000000.0);
    Serial.println();
    Serial.print("Sample rate: ");
    Serial.print(sampleRate);
    Serial.println(" Hz");
    //counter = 0;
    startTime = micros();
    esc=true;
    return;
  }
  int analogValue = analogRead(analogPin);
  Serial.write((byte*)&analogValue, sizeof(analogValue));
  counter++;
}
