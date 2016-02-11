int ledPin = 13;
int outPin = 10;

void setup() {
  // put your setup code here, to run once:
	pinMode(A1, INPUT_PULLUP);
	pinMode(ledPin, OUTPUT);
	pinMode(outPin, OUTPUT);
	digitalWrite(outPin, LOW);
	
}

void loop() {
  // put your main code here, to run repeatedly:
	if (digitalRead(A1)) digitalWrite(ledPin, LOW);
	else {
		digitalWrite(outPin, HIGH);
		delay(100);
		digitalWrite(outPin, LOW);
		digitalWrite(ledPin, HIGH);
		while (true);
	}
}
