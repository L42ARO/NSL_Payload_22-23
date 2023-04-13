#include <SoftwareSerial.h>

SoftwareSerial dra(9,12);
#define PTT_PIN 2 // PTT control pin
#define PD_PIN 7 // PD pin
#define SQ_PIN 8 //Squelch pin
//#define HL_PIN 9



volatile bool squelch = false;
int draState = 0; // Variable to store the state of the DRA
//bool squelch = false;
bool interruptsStart = false;
volatile unsigned long lastPrintTime = 0;
volatile unsigned long squelch_start = 0;
volatile unsigned long curr_sr = 0;
void setup() {
  Serial.begin(500000); // Set the baud rate for the serial monitor
  ADMUX |= (1<< REFS0);
  ADCSRA |= (1 << ADPS2);// | (1 << ADPS1) | (1 << ADPS0);
  ADCSRA |= (1 << ADEN);
  
  //ADCSRA &= ~(bit (ADPS0) | bit (ADPS1) | bit (ADPS2)); // clear prescaler bits
  //ADCSRA |= bit (ADPS2); // set prescaler to 2 (highest ADC clock frequency)
  //ADCSRA |= bit (ADEN); // enable ADC
   while (!Serial) {
    ; // wait for serial port to connect
  }
  DRA_Setup();
  //Serial.write("<");
}

void loop() {
  //digitalWrite(PD_PIN, HIGH); // Set the PD pin to a high state
  if(draState==4){
/*    if(interruptsStart){
      return;
    }*/
    int sq_out = digitalRead(SQ_PIN);
    if(sq_out == LOW && !squelch){
      squelch_start = micros();
      curr_sr = 0;
      squelch = true;
    }else if(sq_out == HIGH && squelch){
      unsigned long time_taken = micros()-squelch_start;
      double sampling_rate = 1000000.0 * curr_sr / time_taken;
      Serial.write("<");
      Serial.print("Time: ");
      Serial.println(time_taken);
      Serial.print("Samples: ");
      Serial.println(curr_sr);
      Serial.print("Rate: ");
      Serial.println(sampling_rate);
      Serial.write(">");
      squelch = false;
    }  
    //Serial.print(sq_out*100);
    //Serial.print(",");
    uint16_t reading = analogReadDirect();
    //int reading = analogReadDirect();
    
  if (squelch) {
    //Serial.println(reading);
    unsigned long currentTime = micros();
    if (currentTime - lastPrintTime >= 120 || true) { // Print the data every 120 microseconds (8300 samples per second)
      
      //byte high_byte = reading >> 8;
      //byte low_byte = reading & 0xFF;
      //Serial.write(high_byte);
      //Serial.write(low_byte);
      Serial.write((byte*)&reading, sizeof(reading));
      lastPrintTime = currentTime;
      curr_sr+=1;
    }
  }
    /*cli(); // Disable interrupts
    TCCR1A = 0; // Clear timer control register A
    TCCR1B = 0; // Clear timer control register B
    TCNT1 = 0; // Clear timer counter
    OCR1A = 71; // Set compare value (208 us @ 16 MHz clock)
    TCCR1B |= (1 << WGM12); // Configure timer in CTC mode
    TCCR1B |= (1 << CS10); // Set prescaler to 1 (16 MHz clock)
    TIMSK1 |= (1 << OCIE1A); // Enable timer compare interrupt
    sei(); // Enable interrupts*/
    return;
  }
  else if(draState == 0){ // If the DRA is in the OFF state
    if(HandShake()){ // If the handshake is successful
      draState = 1; // Set the DRA state to ON
    }
  }
  else if(draState == 1){ // If the DRA is in the ON state
    if(SetFrequency()){
      draState = 2;
    }
  }
  else if(draState==2){
    if(SetVolume()){
      draState=3;
    }
  }
  else if(draState==3){
    if(SetFilter()){
      draState=4;
      Serial.write(">");
    }
  }
}
ISR(TIMER1_COMPA_vect) {
  
}

// Function to read the analog input using direct port access
inline int analogReadDirect() {
  // Select the ADC channel and set the reference voltage
  //ADMUX = (pin & 0x07) | (1 << REFS0);
  ADMUX = (ADMUX & 0xF0) | (0 & 0x0F);
  // Enable the ADC and start the conversion
  //ADCSRA |= (1 << ADEN) | (1 << ADSC);
  // Wait for the conversion to finish
  //while (ADCSRA & (1 << ADSC));
  ADCSRA |= (1 >> ADSC);
  while (bit_is_set(ADCSRA, ADSC));
  // Return the raw ADC value
  uint16_t adc_value=ADC;
  return adc_value;
}
bool SetFilter(){
  SendCommand("AT+SETFILTER=0,0,0\r\n");
  String msg = getMessage();
  Serial.println(msg);
  delay(200);
  if(msg=="+DMOSETFILTER:0\r\n"){
    return true;
  }
  return false;
}

bool SetVolume(){
  SendCommand("AT+DMOSETVOLUME=5\r\n");
  String msg = getMessage();
  Serial.println(msg);
  if(msg == "+DMOSETVOLUME:0\r\n"){
    return true;
  }
  return false;
}

bool SetFrequency(){
  //Serial.println("Freq Sent");
  SendCommand("AT+DMOSETGROUP=1,150.0000,144.9000,0000,1,0000\r\n");
  String msg = getMessage();
  //Serial.println(msg);
  if(msg=="+DMOSETGROUP:0\r\n"){
    return true;
  }
  return false;
}

bool HandShake(){
  Serial.println("Handshake Started");
  SendCommand("AT+DMOCONNECT \r\n");
  String msg = getMessage();
  Serial.println(msg);
  if(msg=="+DMOCONNECT:0\r\n"){
    return true;
  }
  else{
    return false;
  }
}

void SendCommand(String cmd){
  // Switch to TX mode and send the command to the module
  digitalWrite(PTT_PIN, LOW); // Set the module to TX mode
  delay(20); // Add a delay of 20ms to switch to TX mode
  dra.write(cmd.c_str(), cmd.length()); // Send the command to the module
}

String getMessage(){
  // Switch back to RX mode and wait for a response from the module
  digitalWrite(PTT_PIN, HIGH); // Set the module to RX mode
  delay(20); // Add a delay of 20ms to switch to RX mode
  while (dra.available() == 0) {}
  delay(20); // Give the module some time to send all the data
  String message = "";
  while (dra.available() > 0) {
    // Read the response from the module
    char incomingByte = dra.read();
    message += incomingByte;
  }
  delay(500);
  return message;
}

void DRA_Setup(){
  pinMode(PTT_PIN, OUTPUT); // Set the PTT pin as an output
  pinMode(PD_PIN, OUTPUT); // Set the PD pin as an output
  //pinMode(HL_PIN, OUTPUT);
  pinMode(SQ_PIN, INPUT);
  digitalWrite(PD_PIN, HIGH); // Set the PD pin to a high state
  digitalWrite(PTT_PIN, HIGH); // Set the module to RX mode initially
  //analogWrite(HL_PIN, 150);
  delay(500);
  dra.begin(9600);
}
