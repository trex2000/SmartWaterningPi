import RPi.GPIO as GPIO
import asyncio

T_DEBOUNCE_INIT_VALUE = 10  # debounce counter initial value
T_SLEEP = 0.01  # sleep time
CNT_ELAPSED_VAL = 0  # counter was running and reached 0
CNT_STOPPED_VAL = 0xFFFF  # counter was stopped and is not running
PUSH_BUT1 = 16  # push button 1 pin number
PUSH_BUT2 = 20  # push button 2 pin number

debounce_counter1 = T_DEBOUNCE_INIT_VALUE
debounce_counter2 = T_DEBOUNCE_INIT_VALUE


#define 2 events for the button debounced state
button1PressedEvent = asyncio.Event()
button2PressedEvent = asyncio.Event()



def setup_button():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
    GPIO.setup(PUSH_BUT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # the input pin initial value is HIGH, we use pull up resistor
    # pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
    # pull up resistor keeps the input HIGH


def counter_running(counter):
    if (counter != CNT_ELAPSED_VAL) and (counter != CNT_STOPPED_VAL):
        return True


def counter_elapsed(counter):
    return counter == CNT_ELAPSED_VAL


def start_counter(counter, init_value):
    counter = init_value
    return counter


def stop_counter(counter):
    counter = CNT_STOPPED_VAL
    return counter


def manage_but1():
    global debounce_counter1, button1PressedEvent
    if GPIO.input(PUSH_BUT1) == 0:  # button is pressed
        if counter_running(debounce_counter1):  # if the button is pressed for 50ms a
            debounce_counter1 = debounce_counter1 - 1
        elif counter_elapsed(debounce_counter1):
            debounce_counter1 = stop_counter(debounce_counter1)
            button1PressedEvent.set()
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  # if you depress the button the
        # counter will be again 50ms        


def manage_but2():
    global debounce_counter2, button2Pressed
    if GPIO.input(PUSH_BUT2) == 0:  # button is pressed
        if counter_running(debounce_counter2):  # if the button is pressed for 5s and
            debounce_counter2 = debounce_counter2 - 1
        elif counter_elapsed(debounce_counter2):
            debounce_counter2 = stop_counter(debounce_counter2)
            button2PressedEvent.set()
    else:
        debounce_counter2 = start_counter(debounce_counter2, T_DEBOUNCE_INIT_VALUE)  # if you depress the button the
        # counter will be again 500        






