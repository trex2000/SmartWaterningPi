import RPi.GPIO as GPIO

BUTTON1 = 16
BUTTON2 = 20
GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # the input pin initial value is HIGH, we use pull up resistor


# pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
# pull up resistor keeps the input HIGH

''' When the pin is false (LOW state) the button is pushed: 
     GPIO.input(BUTTON1) == 0 
     GPIO.input(BUTTON2) == 0
'''

