const byte CMD_LEDS = 1;
const byte CMD_CAPS = 2;
const byte ACK = 64;
const byte NUM_KEYS = 19;
const byte NUM_CAPS = 2;

const byte LED_OFF = 1;
const byte LED_GREEN = 2;
const byte LED_RED = 3;
const byte LED_ORANGE = 4;

byte leds[NUM_KEYS];

int cap_pins[] = {4, 5};
const int ledPin = 13;

#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
  int i;
  for (i = 0; i < NUM_KEYS; i = i + 1) {
    leds[i] = LED_OFF;
  }
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  Serial.write(ACK);
  mySerial.begin(9600);
  mySerial.println("Debugging");
}

byte res = 0;
int i;
int capValue = 0;

void loop() {
  if (Serial.available() > 0) {
    res = Serial.read();
    mySerial.println("Command code: ");
    mySerial.println(res, DEC);
    if (res == CMD_LEDS) {
      mySerial.println("Reading key data");
      for (i = 0; i < NUM_KEYS; i = i + 1) {
        leds[i] = Serial.read();
      }
      mySerial.println("Done reading key data");
      Serial.write(ACK);
      // Print LED states for debugging
      for (i = 0; i < NUM_KEYS; i = i + 1) {
        mySerial.print(leds[i], DEC);
        mySerial.print(' ');
      }
      mySerial.println();
    } else if (res == CMD_CAPS) {
      mySerial.println("Sending sensor data");
      Serial.write(NUM_CAPS);
      for (i = 0; i < NUM_CAPS; i = i + 1) {
        capValue = analogRead(cap_pins[i]);
        mySerial.println(capValue);
        // clamp the sensor value into a byte
        Serial.write(map(capValue, 0, 1023, 0, 255));
      }
      Serial.write(ACK);
    }
    //mySerial.write(ACK);
  }
  delay(100);

}
