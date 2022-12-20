import RPi.GPIO as GPIO
import asyncio

T_DEBOUNCE_INIT_VALUE = 50  # debounce counter initial value
T_SLEEP = 0.01  # sleep time
CNT_ELAPSED_VAL = 0  # counter was running and reached 0
CNT_STOPPED_VAL = 0xFFFF  # counter was stopped and is not running
PUSH_BUT1 = 16  # push button 1 pin number
PUSH_BUT2 = 20  # push button 2 pin number
LED1 = 26  # LED 1 pin number
LED2 = 19  # LED 2 pin number

debounce_counter1 = T_DEBOUNCE_INIT_VALUE
debounce_counter2 = T_DEBOUNCE_INIT_VALUE
led1_state = False  # LED1 is off
led2_state = False  # LED2 is off


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

def counter_running(counter):
    if (counter != CNT_ELAPSED_VAL) and (counter != CNT_STOPPED_VAL):
        return True


def counter_elapsed(counter):
    return counter == CNT_ELAPSED_VAL


def start_counter(counter, init_value):
    counter = init_value
    return counter


def stop_counter(counter):
    counter = CNT_STOPPED_VAL
    return counter


async def manage_but1():
    global debounce_counter1
    global led1_state
    print('manage_but1 was called')
    if GPIO.input(PUSH_BUT1) == 0:  # button is pressed
        if counter_running(debounce_counter1):  # if the button is pressed for 5s and
            debounce_counter1 = debounce_counter1 - 1
        elif counter_elapsed(debounce_counter1):
            debounce_counter1 = stop_counter(debounce_counter1)
            print('counter 5s elapsed')
            if led1_state == False:
                GPIO.output(LED1, GPIO.HIGH)
                led1_state = True
            elif led1_state == True:
                GPIO.output(LED1, GPIO.LOW)
                led1_state = False
    else:
        debounce_counter1 = start_counter(debounce_counter1, T_DEBOUNCE_INIT_VALUE)  # if you depress the button the
        # counter will be again 500


async def manage_but2():
    global debounce_counter2
    global led2_state
    print('manage_but2 was called')
    if GPIO.input(PUSH_BUT2) == 0:  # button is pressed
        if counter_running(debounce_counter2):  # if the button is pressed for 5s and
            debounce_counter2 = debounce_counter2 - 1
        elif counter_elapsed(debounce_counter2):
            debounce_counter2 = stop_counter(debounce_counter2)
            print('counter 5s elapsed')
            if led2_state == False:
                GPIO.output(LED2, GPIO.HIGH)
                led2_state = True
            elif led2_state == True:
                GPIO.output(LED2, GPIO.LOW)
                led2_state = False
    else:
        debounce_counter2 = start_counter(debounce_counter2, T_DEBOUNCE_INIT_VALUE)  # if you depress the button the
        # counter will be again 500


async def led_toggling_1():
    while True:
        await manage_but1()
        await asyncio.sleep(1)


async def led_toggling_2():
    while True:
        await manage_but2()
        await asyncio.sleep(1)


setup()

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(led_toggling_1())
    asyncio.ensure_future(led_toggling_2())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
