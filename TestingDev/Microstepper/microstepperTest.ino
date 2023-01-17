void setup() {
pinMode(1 , OUTPUT);
pinMode(2, OUTPUT);
pinMode(3 , OUTPUT);
pinMode(4, OUTPUT);

pinMode(5 , OUTPUT);
pinMode(6, OUTPUT);
pinMode(7 , OUTPUT);
pinMode(8, OUTPUT);

}
void loop() {


  float floatTime = float(millis());
  float A = (sin((floatTime * 0.03) )) * 255;
  float B = (sin((floatTime * 0.03) + 1.5708)) * 255;
  analogWrite(1, max(0, A));
  analogWrite(2, max(0,-A));
  analogWrite(3, max(0, B));
  analogWrite(4, max(0,-B));

  analogWrite(5, max(0, A));
  analogWrite(6, max(0,-A));
  analogWrite(7, max(0, B));
  analogWrite(8, max(0,-B));
  

delay(1000);
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
  /*
}

delay(1);


}
