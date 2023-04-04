"""! @mainpage Smart Watering System

@brief rovid leirasa a projektnek 
"""

"""! @package MenuDisplay.py

@brief rovid leiras a modulerol
"""


# Imports
import asyncio
import board
import busio
import RPi.GPIO as GPIO
import adafruit_ssd1306 
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from PushButton import *


# Global Constants of the OLED display
## The I2C address of the display
OLED_ADDRESS = 0x3c
## Widht size of the display
WIDTH = 128
## Height size of the display
HEIGHT = 64
## 5 bit space created inside the border
PADDING = 1
## Created I2C instance
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)
## Parsed the xml file
tree = ET.parse('smart_watering_menu.xml')
root = tree.getroot()
## The base font of the menu 
font = ImageFont.truetype('DejaVuSerif.ttf', 10)
## Selected item is highlighted on the menu
highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)
## Menu index
menu = 0
## Selected item on the menu
selectedItem = 0 
## The oled display will be redrawn if it's True 
redrawNeeded = True 


def setup():
    setup_button()


def main_menu():   
        global font, highlighted, menu, selectedItem, button1PressedEvent, redrawNeeded
        numberOfElement = len(root[menu])  # number of elements in the main_menu
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
        if button1PressedEvent.is_set():    #check if event was fired        
            if selectedItem < numberOfElement:  # if the button is pressed (and the selected item is less than the number of elements)
                # then the selected item should be the next one
                selectedItem = selectedItem + 1
                redrawNeeded = True  # redraw is needed, otherwise the menu overwrites itself over and over again
            else:
                selectedItem = 0  # if the selected item is the last one, and you press the button than the next selected item should be the first element
                redrawNeeded = True
        button1PressedEvent.clear()

        
async def async_task_manageButton1():
    while True:
        manage_but1()
        await asyncio.sleep(T_SLEEP)


async def async_task_manageButton2():
    while True:
        manage_but2()
        await asyncio.sleep(T_SLEEP)


async def async_task_manage_main_menu():
    while True:
        main_menu()
        await asyncio.sleep(T_SLEEP)


setup()

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(async_task_manageButton1())
    asyncio.ensure_future(async_task_manageButton2())
    asyncio.ensure_future(async_task_manage_main_menu())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()