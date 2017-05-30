import sys, time
from ser.keyboardserial import KeyboardSerial


TARGET = "the quick brown fox jumped over the lazy dog"

ks = KeyboardSerial()

ks.autoconnect()
if ks.is_connected():
    print("Successfully connected")

last = '1'
for c in TARGET.lower():
    #ks.update_leds({last: 1})
	if (last == ' '):
		ks.update_leds({'SPACE_LEFT': 1})
		ks.update_leds({'SPACE_RIGHT': 1})
	else:
		key = KeyboardSerial.KEYS[KeyboardSerial.CHAR_MAP[last]]
		ks.update_leds({key: 1})
	if (c == ' '):
		ks.update_leds({'SPACE_LEFT': 2})
		ks.update_leds({'SPACE_RIGHT': 2})
	else:
		key = KeyboardSerial.KEYS[KeyboardSerial.CHAR_MAP[c]]
		ks.update_leds({key: 2})
	last = c
	time.sleep(1)
	
ks.disconnect()
