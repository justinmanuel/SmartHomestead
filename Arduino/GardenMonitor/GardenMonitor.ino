int index = 0;
char frame[20];
char prevByte;
int solenoidPin = 8;
int LEDPin = 10;

void sendMoisture();

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
  pinMode(solenoidPin, OUTPUT);
  pinMode(LEDPin, OUTPUT);
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
      byte state = digitalRead(solenoidPin);
      Serial1.print(state);
    }
    else if ( inByte == 3) digitalWrite(solenoidPin, HIGH);
    else if ( inByte == 4) digitalWrite(solenoidPin, LOW);
    else if ( inByte == 5)
    {
      byte state = digitalRead(LEDPin);
      Serial1.print(state);
    }
    else if ( inByte == 6) digitalWrite(LEDPin, HIGH);
    else if ( inByte == 7) digitalWrite(LEDPin, LOW);
  }
}
