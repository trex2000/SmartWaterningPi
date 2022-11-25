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

debounce_counter = 500
led1_state = False  # LED1 is off

while True:
    if GPIO.input(16) == 0:
        print('Button 1 was pressed')  # button is pressed
        if debounce_counter == 0 and led1_state == False:  # if the button is pressed for 5s and
            GPIO.output(26, GPIO.HIGH)                    # the LED is off than it is going to turn on
            led1_state = True
        elif debounce_counter == 0 and led1_state == True:  # if the LED is already on and
            GPIO.output(26, GPIO.LOW)                      # the button is pressed for 5s the LED is going to
            led1_state = False                              # turn off
        else:
            debounce_counter = debounce_counter - 1
            print(debounce_counter)
            print(led1_state)
    else:
        debounce_counter = 500  # if you depress the button the counter will be again 500
    sleep(.01)
