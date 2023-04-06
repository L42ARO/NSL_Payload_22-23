#define PTT_PIN 2 // PTT control pin
#define PD_PIN 7 // PD pin

void setup() {
  //delay(500); // Add a delay of 500ms at the beginning of the setup function
  pinMode(PTT_PIN, OUTPUT); // Set the PTT pin as an output
  pinMode(PD_PIN, OUTPUT); // Set the PD pin as an output
  digitalWrite(PD_PIN, HIGH); // Set the PD pin to a high state
  digitalWrite(PTT_PIN, HIGH); // Set the module to RX mode initially
  Serial.begin(9600); // Set the baud rate for the serial monitor
  delay(500);
}

void loop() {
  // Switch to TX mode and send the command to the module
  digitalWrite(PTT_PIN, LOW); // Set the module to TX mode
  delay(20); // Add a delay of 20ms to switch to TX mode
  Serial.write("AT+DMOCONNECT \r\n"); // Send the command to the module

  // Switch back to RX mode and wait for a response from the module
  digitalWrite(PTT_PIN, HIGH); // Set the module to RX mode
  delay(20); // Add a delay of 20ms to switch to RX mode
  while (Serial.available() == 0) {}
  delay(20); // Give the module some time to send all the data
  while (Serial.available() > 0) {
    // Read the response from the module
    char incomingByte = Serial.read();
    Serial.print(incomingByte);
  }
}
