#include "draManager.h"

bool DRA::HandShake(){
    Serial.end();
    Serial.begin(500000);
    while (!Serial) {;} // wait for serial port to connect
    digitalWrite(PD_PIN, HIGH); // Set the PD pin to a high state
    delay(500);
    Serial.println("Handshake Started");
    SendCommand("AT+DMOCONNECT \r\n");
    String msg = GetMessage();
    Serial.println(msg);
    if(msg=="+DMOCONNECT:0\r\n"){ return true;}
    else{return false;}
}

bool DRA::SetFrequency(){
    //Serial.println("Freq Sent");
    SendCommand("AT+DMOSETGROUP=1,150.0000,145.0000,0000,1,0000\r\n");
    String msg = GetMessage();
    //Serial.println(msg);
    if(msg=="+DMOSETGROUP:0\r\n"){ return true; }
    return false;
}

bool DRA::SetVolume(){
    SendCommand("AT+DMOSETVOLUME=5\r\n");
    String msg = GetMessage();
    Serial.println(msg);
    if(msg == "+DMOSETVOLUME:0\r\n"){ return true;}
    return false;
}

void DRA::SendCommand(String cmd){
    // Switch to TX mode and send the command to the module
    digitalWrite(PTT_PIN, LOW); // Set the module to TX mode
    delay(20); // Add a delay of 20ms to switch to TX mode
    dra.write(cmd.c_str(), cmd.length()); // Send the command to the module
}

String DRA::GetMessage(){
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

void DRA::squelch_Loop(){
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
    int reading = analogRead(A0);
    if (squelch) {
        //Serial.println(reading);
        unsigned long currentTime = micros();
        byte high_byte = reading >> 8;
        byte low_byte = reading & 0xFF;
        Serial.write(high_byte);
        Serial.write(low_byte);
        lastPrintTime = currentTime;
        curr_sr+=1;
    }
}

bool DRA::SetFilter(){
    SendCommand("AT+SETFILTER=0,0,0\r\n");
    String msg = GetMessage();
    Serial.println(msg);
    delay(200);
    if(msg=="+DMOSETFILTER:0\r\n"){
      return true;
    }
    return false;
}