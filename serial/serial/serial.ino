const int CMD_LEDS = 0;
const int CMD_CAPS = 1;
const int ACK = 0;
const int NUM_KEYS = 19;
const int NUM_CAPS = 2;

const int LED_OFF = 0;
const int LED_GREEN = 1;
const int LED_RED = 2;
const int LED_ORANGE = 3;

int leds[NUM_KEYS];

int cap_pins[] = {11, 10};
const int ledPin = 13;

void setup() {
  int i;
  for (i = 0; i < NUM_KEYS; i = i + 1) {
    leds[i] = LED_OFF;
  }
  pinMode(ledPin, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
}

void loop() {
  int res = 0;
  int i;
  if (Serial.available() > 0) {
    res = Serial.read();

    if (res == CMD_LEDS) {
      // Read each of the led states
      for (i = 0; i < NUM_KEYS; i = i + 1) {
        leds[i] = Serial.read();
        digitalWrite(ledPin, HIGH);
        delay(1000);
        digitalWrite(ledPin, LOW);  
        delay(1000);
      }
      while (Serial.available() > 0) {
        Serial.read();
      }
      // Send acknowledge byte
      Serial.write(ACK);
      Serial.flush();
    } else if (res == CMD_CAPS) {
      int sensorData;
      // Send the number of sensors first
      Serial.write(NUM_CAPS);
      // Send each of the sensor values
      for (i = 0; i < NUM_CAPS; i = i + 1) {
        sensorData = analogRead(cap_pins[i]);
        // Divide by four to fit into a byte
        // probably change this later
        Serial.write(sensorData / 4);
      }
      // Close it all up with an ACK
      Serial.write(ACK);
    }
  }
  delay(100);
}
