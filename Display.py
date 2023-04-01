import asyncio
import board  # import board pins
import busio
import RPi.GPIO as GPIO
import adafruit_ssd1306  # import the SSD1306 module.
from PIL import Image, ImageDraw, ImageFont
import time
import xml.etree.ElementTree as ET
from Async_IO_loop import *


OLED_ADDRESS = 0x3c  # the I2C address of the OLED display
WIDTH = 128  # width size of the display
HEIGHT = 64  # height size of the display
PADDING = 1  # 5 bit space created inside the border, left top corner

i2c = busio.I2C(board.SCL, board.SDA)  # create the I2C instance
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)

tree = ET.parse('smart_watering_menu.xml')  # parsed the xml file
root = tree.getroot()


def setup():
    setup_button()


async def main_menu():
    font = ImageFont.truetype('DejaVuSerif.ttf', 10)  # the menu is displayed on oled with the base font
    highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)  # selected item is highlighted in the displayed menu
    menu = 0  # index of the menu
    numberOfElement = len(root[menu])  # number of elements in the main_menu
    selectedItem = 0  # first item selected in the menu
    redrawNeeded = True  # the oled display will be redrawn
    buttonPressed = False  # the button is not pressed

    while True:
        if redrawNeeded:
            redrawNeeded = False
            oled.fill(0)
            image = Image.new('1', (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)
            oled.show()
            # OLED is cleared
            for i in range(0, numberOfElement):
                if i == selectedItem:  # the selected item should be highlighted
                    draw.text((PADDING, PADDING + (i * 10)), root[menu][i].text, font=highlighted, fill=255)
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[menu][i].text, font=font, fill=255)
            oled.image(image)
            oled.show()
            # show image
        if await manage_but1():
            buttonPressed = True
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



setup()


async def button1_pressed():
    while True:
        await manage_but1()
        await asyncio.sleep(1)


async def button2_pressed():
    while True:
        await manage_but2()
        await asyncio.sleep(1)


async def manage_main_menu():
    while True:
        await main_menu()
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(main_menu())
    asyncio.ensure_future(button1_pressed())
    asyncio.ensure_future(button2_pressed())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()