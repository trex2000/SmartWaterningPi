import RPi.GPIO as GPIO
from time import sleep

IN1 = 17  # assigning the pin numbers
IN2 = 27
ENA = 13


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)  # IN1 and IN2 controls the direction in which the motor will spin
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)  # their initial values are assigned as low
GPIO.setup(ENA, GPIO.OUT)  # controls the speed of the motor
pwm = GPIO.PWM(ENA, 1000)  # the frequency is set to 100Hz
pwm.start(50)  # and the duty cycle is set to 50 which will make the motor run at 50% speed


def run_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)


def run_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)


answer = input('To run the motor forward press "r".\n To tun the motor backward press "b".')

while True:
    print(answer)
    if answer == 'r':
        run_forward()
    else:
        run_backward()
    sleep(10)

