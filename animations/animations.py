from ser.keyboardserial import KeyboardSerial
import sys, time

KEYS = ['ARROW_RIGHT', 'PG_DN', 'PG_UP', 'ARROW_DOWN', 'ARROW_UP', 'DEL', 'INS', 'ARROW_LEFT',
        '\\', 'BACKSPACE', 'ENTER', 'SHIFT_RIGHT', 'CTRL_RIGHT', ']', '=', '"', '[',
        'ALT_RIGHT', '/', '-', ';', 'p', '.', 'FN', '0', 'l', 'o', ',', '9', 'k', 'i', 'SPACE_RIGHT',
        'm', '8', 'j', 'u', 'n', '7', 'h', 'y', 'b', '6', 'g', 't', 'v', '5', 'f', 'SPACE_LEFT',
        'r', 'c', '4', 'd', 'e', 'x', '3', 's', 'ALT_LEFT', 'w', 'z', '2', 'a', 'q', 'WIN', '1', 'CTRL_LEFT',
        'SHIFT_LEFT', 'CAPSLOCK', 'TAB', 'ESC']

ks = KeyboardSerial()

RED = 3
GREEN = 2
OFF = 0

def auto_snake():
    while(True):
        snake(GREEN, 1.5)
        time.sleep(.04)
        snake(RED, 1.5, 1)
        time.sleep(.04)

def manual_snake():
    option = int(input("Enter option: "))
    while (option != 9):
        snake(option, 1.5)
        option = int(input("Enter option: "))

def snake(state, seconds, dir = 0):
    delay = seconds / len(KEYS)
    if (dir == 0):
        for i in range(len(KEYS)):
            ks.update_leds({KEYS[i] : state})
            time.sleep(delay)
    else:
        for i in range(len(KEYS)-1, 0, -1):
            ks.update_leds({KEYS[i]: state})
            time.sleep(delay)

def main():
    print("Connecting to serial port on " + sys.argv[1])
    ks.connect(sys.argv[1])
    if ks.is_connected():
        print("Successfully connected")
    else:
        print("Could not connect")
        sys.exit()

    manual_snake()
    #auto_snake()

    ks.disconnect()







if __name__ == '__main__':
    main()


