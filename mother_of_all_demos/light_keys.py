import sys, time
from keyboardserial import KeyboardSerial


TARGET = "the quick brown fox jumped over the lazy dog"

def turn_off:
	# turn off all leds

	
	
ks = KeyboardSerial()

print("Connecting to serial port on " + sys.argv[1])
ks.connect(sys.argv[1])
if ks.is_connected():
    print("Successfully connected")

for c in TARGET:
	ks.update_leds({c: 2})
	time.sleep(1000)
	
ks.disconnect()