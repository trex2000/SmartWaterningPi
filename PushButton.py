"""!Two push buttons are debounced.
    In case the push buttons are pressed for at least 10ms an event is defined.
"""

# Imports
import RPi.GPIO as GPIO
import asyncio

# Global Constants of the push buttons
## Debounce counter initial value.
T_DEBOUNCE_INIT_VALUE = 10  
## Sleep time.
T_SLEEP = 0.01  
## Counter was running and reached 0.
CNT_ELAPSED_VAL = 0  
## Counter was stopped and is not running.
CNT_STOPPED_VAL = 0xFFFF  
## Push Button 1 pin number.
PUSH_BUT1 = 16 
## Push Button 2 pin number.
PUSH_BUT2 = 20  
## Initial value is assigned for Push Button1's debounce counter.
debounce_counter1 = T_DEBOUNCE_INIT_VALUE
## Initial value is assigned for Push Button3's debounce counter.
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
## Defined an event for Push Button1's debounced state.
button1PressedEvent = asyncio.Event()
## Defined an event for Push Button2's debounced state.
button2PressedEvent = asyncio.Event()


# Functions
def setup_button():
    """!Setup the library to use board numbering.

    Uses the GPIO pin numbers instead of 'standard' pin numbers.
    Initializes pin PUSH_BUT1, PUSH_BUT2 as an input pin. 
    Instruct the Raspberry Pi to pull the pin high using the pull_up_down parameters.
    """

    GPIO.setwarnings(False)  # Ignore warnings for now.
    GPIO.setmode(GPIO.BCM)  # Using GPIO pin numbers.
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(PUSH_BUT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# The Push Buttons input pin's initial value rae HIGH, because we use pull up resistors.
# Pull up resistor: the pin is connect to VCC, with an open switch connection between pin and GND.
# Pull up resistor keeps the input HIGH  


def counter_running(counter):
    """!Counter is running.

    Running as long as its elapsed AND stopped.
    """

    if counter != CNT_ELAPSED_VAL and counter != CNT_STOPPED_VAL:
        return True


def counter_elapsed(counter):
    """!Counter is elapsed.

    Counter is running and reached 0.
    """
    
    return counter == CNT_ELAPSED_VAL     


def start_counter(counter, init_value):
    """!Starts counter.

    Assigns a value for the counter and starts to count.
    """
    
    counter = init_value
    return counter


def stop_counter(counter):
    """!Counter stops.

    Counter reached 0 and stopped running.
    """
    
    counter = CNT_STOPPED_VAL
    return counter


def manage_but1():
    """! Debounces Push Button1.

    Push Button1 is debounced when the button is pressed for 10ms.
    """
    
    global debounce_counter1, button1PressedEvent
    if GPIO.input(PUSH_BUT1) == 0:  # Push Button 1 pressed.
        if counter_running(debounce_counter1):  # Counter is running.  
            debounce_counter1 = debounce_counter1 - 1  
        elif counter_elapsed(debounce_counter1):  # Counter reached 0.
            debounce_counter1 = stop_counter(debounce_counter1)  # Counter stops running.
            button1PressedEvent.set()  # Push Button 1 was debounced (pressed for 10ms) and an event is set. 
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  # In case Push Button1 is depressed the counter starts again     


def manage_but2():
    """! Debounces Push Button2.

    Push Button2 is debounced when the button is pressed for 10ms.
    """
    
    global debounce_counter2, button2Pressed
    if GPIO.input(PUSH_BUT2) == 0:  # Push Button 2 is pressed.
        if counter_running(debounce_counter2):  # Counter is running.
            debounce_counter2 = debounce_counter2 - 1
        elif counter_elapsed(debounce_counter2):  # Counter reached 0.
            debounce_counter2 = stop_counter(debounce_counter2)
            button2PressedEvent.set()  # Push Button 2 was deboounced (pressed for 10ms) and an event is set.
    else:
        debounce_counter2 = start_counter(debounce_counter2, T_DEBOUNCE_INIT_VALUE)  # In case Push Button2 is depressd the counter starts again.