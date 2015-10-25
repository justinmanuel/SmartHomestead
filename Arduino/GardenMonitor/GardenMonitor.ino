int index = 0;
char frame[20];
char prevByte;

void sendMoisture();

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
    
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial1.available() > 0)
  {
    byte inByte = Serial1.read();
    if ( inByte == 1)
    {
      int moisture = analogRead(1);
      Serial1.print(moisture, DEC);
    }
    else if( inByte == 2 )
    {
      byte state = digitalRead(2);
      Serial1.print(state);
    }
    else if ( inByte == 3) digitalWrite(2, HIGH);
    else if ( inByte == 4) digitalWrite(2, LOW);
  }
}
