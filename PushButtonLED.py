"""!LED toggling.
    In case the push buttons are pressed for at least 10ms the corresponding LED shall turned on or off.
"""

# Imports
import RPi.GPIO as GPIO

# Global Constants of the push buttons
## Debounce counter initial value
T_DEBOUNCE_INIT_VALUE = 50  
## Sleep time
T_SLEEP = 5  
## Counter was running and reached 0
CNT_ELAPSED_VAL = 0  
## Counter was stopped and is not running
CNT_STOPPED_VAL = 0xFFFF  
## Initial values is assigned for the first push button's debounce counter 
debounce_counter1 = T_DEBOUNCE_INIT_VALUE
## Initial values is assigned for the second push button's debounce counter 
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
## Push button 1 pin number.
PUSH_BUT1 = 16
## Push button 2 pin number.
PUSH_BUT2 = 20  
## LED 1 pin number.
LED1 = 26 
## LED 2 pin number.
LED2 = 19  
## LED1 is off.
led1_state = False 
## LED2 is off
led2_state = False  


def setup():
    """!Setup the library to use board numbering.

    Uses the GPIO pin numbers instead of 'standard' pin numbers.
    Initialize pin LED1 and LED2 as an output, and their initial value are set as low (LEDs are turned off).
    Initialize pin PUSH_BUT1, PUSH_BUT2 as an input pin. 
    Instruct the Raspberry Pi to pull the pin high using the pull_up_down parameters.
    """

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)  # 26 and 19 pin is set as an output
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)  # the two pins initial value is set to low (off)
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
    GPIO.setup(PUSH_BUT2, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # the input pin initial value is HIGH, we use pull up resistor
# pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
# pull up resistor keeps the input HIGH


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
    """! Turns ON and OFF LED1.

    The push button is debounced when the button is pressed for 10ms and the LED turns ON if it was off and vice-versa.
    """

    global debounce_counter1, led1_state
    if GPIO.input(PUSH_BUT1) == 0:  # Push Button is pressed
        if counter_running(debounce_counter1):  # The counter starts to running down
            debounce_counter1 = debounce_counter1 - 1
        elif counter_elapsed(debounce_counter1): 
            debounce_counter1 = stop_counter(debounce_counter1)
            if led1_state == False:
                GPIO.output(LED1, GPIO.HIGH)
                led1_state = True
            elif led1_state == True:
                GPIO.output(LED1, GPIO.LOW)
                led1_state = False
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  

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