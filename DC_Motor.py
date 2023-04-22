"""!Turns on the DC motor.
"""

#Imports
import RPi.GPIO as GPIO
from time import sleep

#Global Constants
## Input one that controls the H-bridge.
IN1 = 17
## Input two that controls the H-bridge
IN2 = 27
## Input for motor A that controls the PWM.
ENA = 13
## Setting the frequency.
pwm = GPIO.PWM(ENA, 1000)
## Input the answer.
answer = input('To run the motor forward press "r".\n To tun the motor backward press "b".')


#Functions
def DCmotor_setup():
    """!Setup the library to use board numbering.
    
    Uses the GPIO pin numbers instead of 'standard' pin numbers.
    Initializez the IN1 and IN2, which controls the spining direction, their initial value is set low.
    Initializez the ENA output, which controls the speed.
    """

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)   
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup(ENA, GPIO.OUT) 


def run_forward():
    """!The motor spins forward.
    """

    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)


def run_backward():
    """!The motor spins backward.
    """

    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)


DCmotor_setup()
# The duty cycle is set to 50 which will make the motor run at 50% speed.
pwm.start(50)

while True:
    print(answer)
    if answer == 'r':
        run_forward()
    else:
        run_backward()
    sleep(10)