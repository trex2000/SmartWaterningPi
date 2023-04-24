"""!LED toggling.

In case the push buttons are pressed for at least 50ms the corresponding LED shall turned on or off.
"""

# Imports
import RPi.GPIO as GPIO
from time import sleep

# Global Constants of the push buttons
## Debounce counter initial value.
T_DEBOUNCE_INIT_VALUE = 50  
## Sleep time.
T_SLEEP = 0.01  
## Counter was running and reached 0.
CNT_ELAPSED_VAL = 0  
## Counter was stopped and is not running.
CNT_STOPPED_VAL = 0xFFFF  
## Initial value is assigned for Push Button1's debounce counter. 
debounce_counter1 = T_DEBOUNCE_INIT_VALUE
## Initial value is assigned for Push Button2's debounce counter. 
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
## Push Button1 pin number.
PUSH_BUT1 = 16
## Push Button2 pin number.
PUSH_BUT2 = 20  
## LED1 pin number.
LED1 = 26 
## LED2 pin number.
LED2 = 19  
## LED1 state (turned off).
led1_state = False 
## LED2 state (turned off).
led2_state = False  


def setup():
    """!Setup the library to use board numbering.

    Uses the GPIO pin numbers instead of 'standard' pin numbers.
    Initializes pin LED1 and LED2 as an output, and their initial value are set low (LEDs are turned off).
    Initializes pin PUSH_BUT1, PUSH_BUT2 as an input pin. 
    Instruct the Raspberry Pi to pull the pin high using the pull_up_down parameters.
    """

    GPIO.setwarnings(False)  # Disable warnings.
    GPIO.setmode(GPIO.BCM)  # GPIO pin numbers.
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)   
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
    GPIO.setup(PUSH_BUT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

# The Push Buttons input pin's initial value rae HIGH, because we use pull up resistors.
# Pull up resistor: the pin is connect to VCC, with an open switch connection between pin and GND.
# Pull up resistor keeps the input HIGH


def counter_running(counter):
    """!Counter is running.

    Runs as long as its not elapsed and stopped.
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

    Counter reached 0 and stops running.
    """
    
    counter = CNT_STOPPED_VAL
    return counter


def manage_but1():
    """! Turns ON and OFF LED1.

    The push button is debounced when the button is pressed for 10ms and the LED turns ON if it was off and vice-versa.
    """

    global debounce_counter1, led1_state
    if GPIO.input(PUSH_BUT1) == 0:  # Push Button is pressed.
        if counter_running(debounce_counter1):  # The counter starts to running down.
            debounce_counter1 = debounce_counter1 - 1
        elif counter_elapsed(debounce_counter1):  # When the counter reaches 0 it will stop.  
            debounce_counter1 = stop_counter(debounce_counter1)  # And the counter value will be 0.
            if led1_state == False:  # If the LED is off then it will turned on.
                GPIO.output(LED1, GPIO.HIGH)
                led1_state = True
            elif led1_state == True:  # Othervise it will turned off.
                GPIO.output(LED1, GPIO.LOW)
                led1_state = False
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  # If you depressed the Push Buton the counter will start again.  

def manage_but2():
    """! Turns ON and OFF LED2.

    The push button is debounced when the button is pressed for 10ms and the LED turns ON if it was off and vice-versa.
    """

    global debounce_counter2, led2_state
    if GPIO.input(PUSH_BUT2) == 0:  
        if counter_running(debounce_counter2): 
            debounce_counter2 = debounce_counter2 - 1
        elif counter_elapsed(debounce_counter2):
            debounce_counter2 = stop_counter(debounce_counter2)
            if led2_state == False:
                GPIO.output(LED2, GPIO.HIGH)
                led2_state = True
            elif led2_state == True:
                GPIO.output(LED2, GPIO.LOW)
                led2_state = False
    else:
        debounce_counter2 = start_counter(debounce_counter2, T_DEBOUNCE_INIT_VALUE)  


setup()  
while True:
    manage_but1()
    manage_but2()
    sleep(T_SLEEP)