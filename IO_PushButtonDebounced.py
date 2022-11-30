import RPi.GPIO as GPIO
from time import sleep

T_DEBOUNCE_INIT_VALUE = 500  # debounce counter initial value
PUSH_BUT1 = 16  # push button 1 pin number
PUSH_BUT2 = 20  # push button 2 pin number
LED1 = 26  # LED 1 pin number
LED2 = 19  # LED 2 pin number
T_SLEEP = 0.01  # sleep time


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)  # 26 and 19 pin is set as an output
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)  # the two pins initial value is set to low (off)
    GPIO.setup(PUSH_BUT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
    GPIO.setup(PUSH_BUT2, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # the input pin initial value is HIGH, we use pull up resistor


# pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
# pull up resistor keeps the input HIGH

setup()  # initialising the input and output ports

debounce_counter1 = T_DEBOUNCE_INIT_VALUE
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
led1_state = False  # LED1 is off
led2_state = False  # LED2 is off

while True:
    if GPIO.input(PUSH_BUT1) == 0:  # button is pressed
        if debounce_counter1 == 0:  # if the button is pressed for 5s and
            print('counter elapsed')
            debounce_counter1 = T_DEBOUNCE_INIT_VALUE
            if led1_state == False:
                GPIO.output(LED1, GPIO.HIGH)
                led1_state = True
            elif led1_state == True:
                GPIO.output(LED1, GPIO.LOW)
                led1_state = False
        else:
            debounce_counter1 = debounce_counter1 - 1
    else:
        debounce_counter1 = T_DEBOUNCE_INIT_VALUE  # if you depress the button the counter will be again 500
    sleep(T_SLEEP)
