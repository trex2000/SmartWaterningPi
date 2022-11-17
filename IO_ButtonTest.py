import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(16) == LOW:
        print('button was pushed')
    if GPIO.input(20) == LOW:
        print('button was pushed')
