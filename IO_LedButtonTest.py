import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)  # 26 and 19 pin is set as an output
GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)  # the two pins initial value is set to low (off)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # the input pin initial value is HIGH, we use pull up resistor
# pull up resistor: connect between a pin and VCC, with an open switch connected between pin and GND
# pull up resistor keeps the input HIGH

if GPIO.input(16) == 0:  # when the pin is false (LOW state) the button is pushed
    GPIO.output(26, GPIO.HIGH)  # turns on an LED
else:
    GPIO.output(26, GPIO.LOW)  # turns off the LED
if GPIO.input(20) == 0:
    GPIO.output(19, GPIO.HIGH)
else:
    GPIO.output(19, GPIO.LOW)
