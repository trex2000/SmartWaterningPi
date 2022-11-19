import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)  # 26 and 19 pin is set as an output
GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)  # the two pins initial value is set to low (off)

while True:
    GPIO.output(26, GPIO.HIGH)  # turns on the two pins, the pins are made to provide power of 3.3volts
    GPIO.output(19, GPIO.HIGH)
    sleep(5)  # pauses the Python program for 5 seconds
    GPIO.output(26, GPIO.LOW)  # turns off the two pins,the pins are no longer supplying any power
    GPIO.output(19, GPIO.LOW)
    sleep(5)
