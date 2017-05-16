import sys, time
from keyboardserial import KeyboardSerial

ks = KeyboardSerial()

print("Connecting to serial port on " + sys.argv[1])
ks.connect(sys.argv[1])
if ks.is_connected():
        print("Successfully connected")
start = time.time()
ks.update_leds({'a': 5, 'j': 2, 'f': 1})
end = time.time()
print(end - start)
print(ks.get_sensor_data())
ks.disconnect()
