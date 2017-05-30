import sys, time
from ser.keyboardserial import KeyboardSerial


TARGET = "the quick brown fox jumped over the lazy dog"

ks = KeyboardSerial()

ks.autoconnect()
if ks.is_connected():
    print("Successfully connected")

last = '1'
for c in TARGET:
    ks.update_leds({last: 1})
    ks.update_leds({c: 2})
    last = c
    time.sleep(1)
	
ks.disconnect()
