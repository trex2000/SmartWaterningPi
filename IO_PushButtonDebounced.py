import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)  # 26 and 19 pin is set as an output
GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)  # the two pins initial value is set to low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # the input pin initial value is HIGH, we use pull up resistor

# pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
# pull up resistor keeps the input HIGH

led1_state = False  # means that the LED is off
led2_state = False

while True:
    if GPIO.input(16) == 0:  # the button was pushed, pin is connected to the GND (0/LOW/False)
        if led1_state == False:
            GPIO.output(26, GPIO.HIGH)
            led1_state = True  # the LED is on
            sleep(.5)
        else:
            GPIO.output(26, GPIO.LOW)
            led1_state = False
            sleep(.5)
    if GPIO.input(20) == 0:
        if led2_state == False:
            GPIO.output(19, GPIO.HIGH)
            led2_state = True
            sleep(.5)
        else:
            GPIO.output(19, GPIO.LOW)
            led2_state = False
            sleep(.5)