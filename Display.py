import board  # import board pins
import busio
import RPi.GPIO as GPIO
import adafruit_ssd1306  # import the SSD1306 module.
from PIL import Image, ImageDraw, ImageFont
import time
import xml.etree.ElementTree as ET


T_DEBOUNCE_INIT_VALUE = 10  # debounce counter initial value
T_SLEEP = 0.01  # sleep time
CNT_ELAPSED_VAL = 0  # counter was running and reached 0
CNT_STOPPED_VAL = 0xFFFF  # counter was stopped and is not running
PUSH_BUT = 16  # push button 1 pin number
debounce_counter = T_DEBOUNCE_INIT_VALUE


OLED_ADDRESS = 0x3c  # the I2C address of the OLED display
WIDTH = 128  # width size of the display
HEIGHT = 64  # height size of the display
PADDING = 1  # 5 bit space created inside the border, left top corner

i2c = busio.I2C(board.SCL, board.SDA)  # create the I2C instance
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)

tree = ET.parse('smart_watering_menu.xml')  # parsed the xml file
root = tree.getroot()


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # using the GPIO pin numbers instead of 'standard' pin numbers
    GPIO.setup(PUSH_BUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  16, 20 is set as an input



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


def main_menu():
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('DejaVuSerif.ttf', 10)  # the menu is displayed on oled with the base font
    highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)  # selected item is highlighted in the displayed menu
    numberOfElement = len(root[0])  # number of elements in the main_menu
    selectedItem = 0  # first item selected in the menu
    redrawNeeded = True  # the oled display will be redrawn
    buttonPressed = False  # the button is not pressed
    global debounce_counter

    while True:
        if redrawNeeded:
            redrawNeeded = False
            oled.fill(0)
            oled.image(image)
            oled.show()  # OLED is cleared
            for i in range(0, numberOfElement):
                if i == selectedItem:  # the selected item should be highlighted
                    draw.text((PADDING, PADDING + (i * 10)), root[0][i].text, font=highlighted, fill=255)
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[0][i].text, font=font, fill=255)
            #finally show the image that was composed
            oled.image(image)
            oled.show()
        if GPIO.input(PUSH_BUT) == 0:  # button is pressed
            if counter_running(debounce_counter):  # if the button is pressed for 5s and
                debounce_counter = debounce_counter - 1
            elif counter_elapsed(debounce_counter):
                debounce_counter = stop_counter(debounce_counter)
                print('counter 5s elapsed')
                buttonPressed = True
        else:
            debounce_counter = start_counter(debounce_counter, T_DEBOUNCE_INIT_VALUE)  # if you depress the button the
            # counter will be again 500
        if buttonPressed == True:
            if selectedItem < numberOfElement:  # if the button is pressed (and the selected item is less than the number of elements)
                # then the selected item should be the next one
                selectedItem = selectedItem + 1
                redrawNeeded = True  # redraw is needed, otherwise the menu overwrites itself over and over again
                buttonPressed = False
            else:
                selectedItem = 0  # if the selected item is the last one, and you press the button than the next selected item should be the first element
                redrawNeeded = True
                buttonPressed = False
        time.sleep(0.1)

setup()
main_menu()
