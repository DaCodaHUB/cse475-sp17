import sys
from keyboardserial import KeyboardSerial

ks = KeyboardSerial()

print("Connecting to serial port on " + sys.argv[1])
ks.connect(sys.argv[1])
if ks.is_connected():
        print("Successfully connected")
print(ks.update_leds({'a': 5, 'j': 2, 'f': 1}))
print(ks.get_sensor_data())
ks.disconnect()
