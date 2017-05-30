import sys, time
from ser.keyboardserial import KeyboardSerial

ks = KeyboardSerial()

print("Connecting to serial port on " + sys.argv[1])
ks.connect(sys.argv[1])
if ks.is_connected():
    print("Successfully connected")
		
while True:
	data = ks.get_sensor_data()
	# DO DATA PROCESSING
	ks.update_leds({'a': data[0], 's': data[1], 'd': data[2], 'f': data[3], 'j': data[4], 'k': data[5], 'l': data[6], ';': data[7]})
	time.sleep(0.05)
	
ks.disconnect()
