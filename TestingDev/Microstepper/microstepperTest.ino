float starttime;

void setup() {
  starttime = millis();
  
  pinMode(3 , OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(9 , OUTPUT);
  pinMode(10, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  static int count{0};
  Serial.println(++count);

  if (count >= 20){
    return;
  }
  
  float floatTime = float(millis()) - starttime;
  float A = (sin((floatTime * 0.3) )) * 255;
  float B = (sin((floatTime * 0.3) + 1.5708)) * 255;
  
  analogWrite(3, max(0, A));
  analogWrite(11, max(0,-A));
  analogWrite(9, max(0, B));
  analogWrite(10, max(0,-B));

  analogWrite(A0, max(0, A));
  analogWrite(A1, max(0,-A));
  analogWrite(A2, max(0, B));
  analogWrite(A3, max(0,-B));

  
  delay(300);
/*for(int i=0; i<20; i++){
  float floatTime = float(millis());
  float A = (sin((floatTime * 0.03) )) * 255;
  float B = (sin((floatTime * 0.03) + 1.5708)) * 255;
  analogWrite(1, max(0,-A));
  analogWrite(2, max(0,A));
  analogWrite(3, max(0,-B));
  analogWrite(4, max(0,B));

  analogWrite(5, max(0,-A));
  analogWrite(6, max(0,A));
  analogWrite(7, max(0,-B));
  analogWrite(8, max(0,B));
  
}

delay(1);
*/

}