import serial

## Command codes for the keyboard
CMD_LEDS = 0    # update the state of the leds
CMD_CAPS = 1    # retrieve the capacative sensor data
ACK = 0

## LED state values
LED_OFF = 0
LED_GREEN = 1
LED_RED = 2
LED_ORANGE = 3

class KeyboardSerial:
    def __init__(self):
        self.ser = None

    def is_connected():
        return self.ser is not None and self.ser.is_open

    def connect(port):
        # Close any old connections
        if self.ser is not None:
            if self.ser.is_open:
                self.ser.close()
        # Opens a serial port
        try:
            self.ser = serial.Serial(port)
        except serial.SerialException:
            print("Failed to connect to port " + port)
            return False
        return True

    def update_leds(led_states):
        if not self.is_connected():
            return False
        # Write the command code and number of k,v pairs
        ser.write(CMD_LEDS)        
        ser.write(len(led_states))
        # write the state information
        for (key, state) in led_states:
            ser.write(key)
            ser.write(state)
        # wait for an ACK byte before returning
        return ser.read() == ACK
            
    def get_sensor_data():
        if not self.is_connected():
            return False
        # Write the command code
        ser.write(CMD_CAPS)
        # Wait for the ACK byte
        if ser.read() is not ACK:
            print("Invalid ACK from keyboard")
            return False
        # Get the number of sensors
        sensor_len = ser.read()
        sensors = []
        for i in range(sensor_len):
            sensors.append(ser.read())
        if ser.read() is not ACK:
            print("Expected ACK after reading sensors")
            return False
        return sensors
