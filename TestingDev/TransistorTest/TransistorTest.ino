#define E_PIN 3
void setup() {
  // put your setup code here, to run once:
  pinMode(E_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}
bool enable=true;
void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(E_PIN, enable ? HIGH:LOW);
  digitalWrite(LED_BUILTIN, enable ? HIGH:LOW);
  delay(5000);
  enable=!enable;

}
