import serial

## Keyboard information
KEYS = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']

## Command codes for the keyboard
CMD_LEDS = 1    # update the state of the leds
CMD_CAPS = 2    # retrieve the capacative sensor data
ACK = 64

## LED state values
LED_OFF = 1
LED_GREEN = 2
LED_RED = 3
LED_ORANGE = 4

BAUD = 9600

class KeyboardSerial:
    def __init__(self):
        self.key_states = [LED_OFF for led in range(len(KEYS))]
        self.ser = None

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def connect(self, port):
        # Close any old connections
        if self.ser is not None:
            if self.ser.is_open:
                self.ser.close()
        # Opens a serial port with a 1s timeout
        try:
            self.ser = serial.Serial(port, baudrate=BAUD)
        except serial.SerialException:
            print("Failed to connect to port " + port)
            return False
        # Wait for initial ACK to verify serial init
        if self.ser.read() != bytes([ACK]):
            return False
        return True

    def disconnect(self):
        if self.is_connected():
            self.ser.close()

    # Sends a byte over serial and waits for ACK byte
    def send(self, byte):
        if not self.is_connected():
            return False
        self.ser.write(bytes([byte]))
        return True

    # Take a dict of key->LED_STATE and sends the
    # updated state over the serial connection
    def update_leds(self, led_states):
        if not self.is_connected():
            return False
        # Write the command code and number of k,v pairs
        self.send(CMD_LEDS)        
        # Update the internal key array
        for i, key in enumerate(KEYS):
            if key in led_states:
                self.key_states[i] = led_states[key]
        # Send the sequence of states
        print("Sending state sequence of length " + str(len(KEYS)))
        for state in self.key_states:
            self.send(state)
        print("Waiting for ACK")
        # wait for an ACK byte before returning
        return self.ser.read() == bytes([ACK])
            
    def get_sensor_data(self):
        if not self.is_connected():
            return False
        # Write the command code
        self.send(CMD_CAPS)
        # Get the number of sensors
        sensor_len = int.from_bytes(self.ser.read(), byteorder='big')
        print(str(sensor_len) + " sensors to read")
        sensors = []
        for i in range(sensor_len):
            cap_data = int.from_bytes(self.ser.read(), byteorder='big')
            sensors.append(cap_data)
        if self.ser.read() != bytes([ACK]):
            print("Expected ACK after reading sensors")
            return False
        return sensors
