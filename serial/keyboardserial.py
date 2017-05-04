import serial

## Keyboard information
KEYS = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']

## Command codes for the keyboard
CMD_LEDS = 0    # update the state of the leds
CMD_CAPS = 1    # retrieve the capacative sensor data
ACK = 0

## LED state values
LED_OFF = 0
LED_GREEN = 1
LED_RED = 2
LED_ORANGE = 3

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
        # Opens a serial port
        try:
            self.ser = serial.Serial(port, baudrate=BAUD)
        except serial.SerialException:
            print("Failed to connect to port " + port)
            return False
        return True

    # Take a dict of key->LED_STATE and sends the
    # updated state over the serial connection
    def update_leds(self, led_states):
        if not self.is_connected():
            return False
        # Write the command code and number of k,v pairs
        self.ser.write(CMD_LEDS)        
        # Update the internal key array
        for i, key in enumerate(KEYS):
            if key in led_states:
                self.key_states[i] = led_states[key]
        # Send the sequence of states
        print("Sending state sequence of length " + str(len(KEYS)))
        for state in self.key_states:
            self.ser.write(state)
        self.ser.flush()
        # print("Waiting for ACK")
        # # wait for an ACK byte before returning
        # return self.ser.read() == ACK
            
    def get_sensor_data(self):
        if not self.is_connected():
            return False
        # Write the command code
        self.ser.write(CMD_CAPS)
        # Wait for the ACK byte
        if self.ser.read() is not ACK:
            print("Invalid ACK from keyboard")
            return False
        # Get the number of sensors
        sensor_len = self.ser.read()
        sensors = []
        for i in range(sensor_len):
            sensors.append(self.ser.read())
        if self.ser.read() is not ACK:
            print("Expected ACK after reading sensors")
            return False
        return sensors
