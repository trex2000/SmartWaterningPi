"""! @mainpage Smart Watering System

@brief This system uses sensors to measure the actual moisture of the soil and digital temperature and humidity sensor to measure 
the surrounding air.
The system also has an OLED display which displays the menu of the system. You can check out the current moisture of the soil, temperature,
humidity and also turn on or off the automatic watering based on the soil moisture data. 
The data from the sensors are logged into an SQL database.
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
from SoilMoistureSensor import *


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
menuPage = 0
## Selected item on the menu
selectedItem = 0 
## The oled display will be redrawn if it's True 
redrawNeeded = True 
## Longer sleep time.
T_LONG_SLEEP = 3600


def setup():
    """!Ghaters the modules setups
    """

    setup_button()


def main_menu():
        """!Navigating throught the menu
        
        The connected OLED displays the menu with the currently active menu point which is highlighted.
        Push button 1 shall be used to navigate through the menu anf push button 2 to select an option which will navigate to another menu or
        runs a function. 
        """   
        
        # Global values 
        global font, highlighted, menuPage, selectedItem, button1PressedEvent, redrawNeeded
        ## Number of elements in the main_menu
        numberOfElement = len(root[menuPage])  # Number of elements in the menu.
        indexOfElements = int(numberOfElement) - 1  # Number of indexes of the elemnt in the menu.
        if redrawNeeded:
            redrawNeeded = False
            oled.fill(0)
            image = Image.new('1', (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)
            oled.show()  # OLED display is cleared
            for i in range(0, numberOfElement):
                if i == selectedItem:  # The selected item is highlighted
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=highlighted, fill=255)
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=font, fill=255)
            oled.image(image)
            oled.show()  # Shows the menu with the acvtive menu point highlighted
        if button1PressedEvent.is_set():  # Checks if the event was fired        
            if selectedItem < indexOfElements:  # If the button is pressed (and the selected item is less than the number of elements)
                #then the selected item should be the next one
                selectedItem = selectedItem + 1
                redrawNeeded = True  # Redraw is needed, otherwise the menu will overwrite itself over and over again
            else:
                selectedItem = 0  # If the selected item is the last one, and you press push button 1 again the next selected item will be 
                #the first element.
                redrawNeeded = True
        button1PressedEvent.clear()  # The event is marked as “not set” via this function.
        if button2PressedEvent.is_set():  # Checks if the event was fired.
            menuPage = selectedItem + 1  # The OLED should display the selected items menu. 
            selectedItem = 0  # The first item on the new menu list should behighlighted.
            redrawNeeded = True
        button2PressedEvent.clear()  # The event is marked as “not set” via this function.

        
async def async_task_manageButton1():
    """!Define a coroutine for push button 1 that takes in a future.
    """    

    while True:
        manage_but1()
        await asyncio.sleep(T_SLEEP)


async def async_task_manageButton2():
    """!Define a coroutine for push button 2 that takes in a future.
    """

    while True:
        manage_but2()
        await asyncio.sleep(T_SLEEP)


async def async_task_insert_SoilMoistureRecords():
    """!Define a coroutine for inserting records that takes in a future.
    """

    while True:
        insert_SoilMoistureRecords()
        await asyncio.sleep(T_LONG_SLEEP)


async def async_task_get_SoilMoistureRecord():
    """!Define a coroutine for getting the last record that takes in a future.
    """

    while True:
        get_SoilMoistureRecord()
        await asyncio.sleep(T_SLEEP)


async def async_task_manage_main_menu():
    """!Define a coroutine for main menu that takes in a future.
    """

    while True:
        main_menu()
        await asyncio.sleep(T_SLEEP)


setup()


## Define event loop
loop = asyncio.get_event_loop()
# Subsequently starts asyncio based event loop and have it run indefinitely until the program comes to an end
try:
    asyncio.ensure_future(async_task_manageButton1())
    asyncio.ensure_future(async_task_manageButton2())
    asyncio.ensure_future(async_task_manage_main_menu())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()