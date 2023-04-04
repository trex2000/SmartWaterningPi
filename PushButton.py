# Imports
import RPi.GPIO as GPIO
import asyncio

# Global Constants 
## Debounce counter initial value
T_DEBOUNCE_INIT_VALUE = 10  
## Sleep time
T_SLEEP = 0.01  
## Counter was running and reached 0
CNT_ELAPSED_VAL = 0  
## Counter was stopped and is not running
CNT_STOPPED_VAL = 0xFFFF  
## Push button 1 pin number
PUSH_BUT1 = 16 
## Push button 2 pin number
PUSH_BUT2 = 20  
## Initial values is assigned for the first push button's debounce counter 
debounce_counter1 = T_DEBOUNCE_INIT_VALUE
## Initial values is assigned for the second push button's debounce counter 
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
## Defined an event for the first push button's debounced state
button1PressedEvent = asyncio.Event()
## Defined an event for the second push button's debounced state
button2PressedEvent = asyncio.Event()


# Functions
def setup_button():

    """!Setup the library to use board numbering.

    Uses the GPIO pin numbers instead of 'standard' pin numbers, initialize pin PUSH_BUT1, PUSH_BUT2 as an input pin. 
    Instruct the Raspberry Pi to pull the pin high using the pull_up_down parameters.
    """

    ## Ignore warning for now
    GPIO.setwarnings(False)
    ## Using the GPIO pin numbers instead of 'standard' pin numbers
    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(PUSH_BUT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def counter_running(counter):

    """!Counter is running.

    @param counter   The debounce counter.
    """

    if (counter != CNT_ELAPSED_VAL) and (counter != CNT_STOPPED_VAL):
        return True


def counter_elapsed(counter):
    
    """!Counter is elapsed.

    @param counter   The debounce counter.
    """
    
    return counter == CNT_ELAPSED_VAL


def start_counter(counter, init_value):
    
    """!Starts counter.

    @param counter   The debounce counter.
    @param init_values   The debounce counter.
    """
    
    counter = init_value
    return counter


def stop_counter(counter):
    
    """!Counter stops.

    @param counter   The debounce counter
    """
    
    counter = CNT_STOPPED_VAL
    return counter


def manage_but1():

    """! Debounces push button 1.

    The push button is debounced when the button is pressed for 10ms.
    """
    
    global debounce_counter1, button1PressedEvent
    if GPIO.input(PUSH_BUT1) == 0:  # push button 1 pressed
        if counter_running(debounce_counter1):  
            debounce_counter1 = debounce_counter1 - 1  
        elif counter_elapsed(debounce_counter1):
            debounce_counter1 = stop_counter(debounce_counter1)
            button1PressedEvent.set()  # push button pressed for 10 ms 
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  # if the push button is depress the
        # counter will start again     


def manage_but2():
    
    """! Debounces push button 2.

    The push button is debounced when the button is pressed for 10ms.
    """
    
    global debounce_counter2, button2Pressed
    if GPIO.input(PUSH_BUT2) == 0:  # push button 2 is pressed
        if counter_running(debounce_counter2):  
            debounce_counter2 = debounce_counter2 - 1
        elif counter_elapsed(debounce_counter2):
            debounce_counter2 = stop_counter(debounce_counter2)
            button2PressedEvent.set()  # push button is pressed for 10ms and
    else:
        debounce_counter2 = start_counter(debounce_counter2, T_DEBOUNCE_INIT_VALUE)  # if the push button is depress the
        # counter will start again     
