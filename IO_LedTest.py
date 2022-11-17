import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarning(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(19, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(26, GPIO.HIGH)
    sleep(5)
    GPIO.output(26, GPIO.LOW)
    sleep(5)
    GPIO.output(19, GPIO.HIGH)
    sleep(5)
    GPIO.output(19, GPIO.LOW)
    sleep(5)
    