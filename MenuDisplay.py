"""! @mainpage Smart Watering System

@brief This system uses sensors to measure the actual moisture of the soil and digital temperature and humidity sensor to measure 
the surrounding air.
The system also has an OLED display which displays the menu of the system. You can check out the current moisture of the soil, temperature,
humidity and also turn on or off the automatic watering based on the soil moisture data. 
The data from the sensors are logged into an SQL database.
"""

"""! @file MenuDisplay.py
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
from HumiditySensor import *
from SoilMoistureSensor import *


# Global Constants of the OLED display
## The I2C address of the display.
OLED_ADDRESS = 0x3c
## Widht size of the display.
WIDTH = 128
## Height size of the display.
HEIGHT = 64
## 5 bit space created inside the border.
PADDING = 1
## Created I2C instance.
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)
## Parsed the xml file.
tree = ET.parse('SmartWateringMenu.xml')
root = tree.getroot()
## The base font of the menu. 
font = ImageFont.truetype('DejaVuSerif.ttf', 10)
## Selected item is highlighted on the menu.
highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)
## Menu index.
menuPage = 0
## Selected item on the menu.
selectedItem = 0 
## The oled display will be redrawn if it's True. 
redrawNeeded = True
## Longer sleep time.
T_LONG_SLEEP = 10 # 10 second
## Cyclic call of function that retrieves most recent ambient values.
T_AMBIENT_LOGGING_SLEEP_VALUE = 60  # 1 minute 
## Set init value of measured humidity.
currentHum = -1
## Set init value of measured temperature.
currentTemp = -1
## Set init value of measured moisture.
currentMoist = -1


#Functions
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
        ## Number of elements in the main_menu.
        numberOfElements = len(root[menuPage]) 
        ## Last item in the menu.
        lastElement = int(numberOfElements) - 1
        if redrawNeeded:
            redrawNeeded = False
            oled.fill(0)
            image = Image.new('1', (WIDTH, HEIGHT))  
            draw = ImageDraw.Draw(image)
            oled.show()  # OLED display is cleared.
            for i in range(0, numberOfElements):
                if i == selectedItem:  # the selected item should be highlighted
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=highlighted, fill=255)
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=font, fill=255)
            oled.image(image)
            oled.show()  # Shows the menu with the active point highlighted.
        if button1PressedEvent.is_set():  # Checks if event was fired.      
            if selectedItem < lastElement:  # If the button is pressed (and the selected item is less than the number of elements)
                #then the selected item should be the next one.
                selectedItem = selectedItem + 1
                redrawNeeded = True  # Redraw is needed, otherwise the menu overwrites itself over and over again
            else:
                selectedItem = 0  # If the selected item is the last one, and you press push button 1, than the next selected item will be
                #the first element.
                redrawNeeded = True
        button1PressedEvent.clear()  # The event is marked as 'not set' via this function.
        if button2PressedEvent.is_set():  # Checks if the event was fired. 
            # Checks if the selected item is not the last one.             
            if selectedItem != lastElement: 
                if root[menuPage][selectedItem].get('callable')=='true':  # If the item is callable, it calls and displays the data.                   
                    # textToDisplay = RunSelectedFunction(root[menuPage][selectedItem].text)
                    print("it's callable")
                else:  # If not callable dislpays the next menu.
                    nextMenuItemToFind=root[menuPage][selectedItem].text
                    for j in range(0, numberOfElements):
                        if root[j].get('title')  == nextMenuItemToFind:
                            menuPage = j
                            selectedItem = 0    # The first item on the list is selected.
                            redrawNeeded = True
                            break
            else:   # If the last item is selected than displays the previous menu.
                selectedItem = menuPage - 1  # The selected item is the one which submenu was opened.
                menuPage = 0
                redrawNeeded = True                             
        button2PressedEvent.clear()  # The event is marked as 'not set' via this function.
        
        
def  RunSelectedFunction():
    global currentHum, currentTemp
    if root[menuPage][selectedItem].text == "3. Current humidity":
        currentHum = get_HumidityRecord()
        return currentHum


       #elseif (argument) == "2. Current temperature": 
        #  #return get_TemperatureRecord()
         # return currentTemp




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


async def async_task_insert_HumidityRecords():
    """!Define a coroutine for inserting humidity records that takes in a future.
    """

    while True:
        insert_HumidityRecords(device_name, date, temperature_f, temperature_c, humidity)
        await asyncio.sleep(T_LONG_SLEEP)


async def async_task_get_HumidityRecord():
    """!Define a coroutine for getting the last humidity record that takes in a future.
    """

    while True:
        global currentHum
        currentHum = get_HumidityRecord()
        await asyncio.sleep(T_AMBIENT_LOGGING_SLEEP_VALUE)      


async def async_task_get_TemperatureRecord():
    """!Define a coroutine for getting the last temperature record that takes in a future.
    """

    while True:
        currentTemp = get_TemperatureRecord()
        await asyncio.sleep(T_AMBIENT_LOGGING_SLEEP_VALUE)


async def async_task_insert_SoilMoistureRecords():
    """!Define a coroutine for inserting moisture records that takes in a future.
    """

    while True:
        insert_SoilMoistureRecords(device_name, date, raw_value, percentage, classification)
        await asyncio.sleep(T_LONG_SLEEP)


async def async_task_get_SoilMoistureRecord():
    """!Define a coroutine for getting the last moisture record that takes in a future.
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
    asyncio.ensure_future(async_task_insert_HumidityRecords())
    asyncio.ensure_future(async_task_get_HumidityRecord())
    asyncio.ensure_future(async_task_get_TemperatureRecord())
    asyncio.ensure_future(async_task_insert_SoilMoistureRecords())
    asyncio.ensure_future(async_task_get_SoilMoistureRecord())
    asyncio.ensure_future(async_task_manage_main_menu())
    loop.run_forever()
except KeyboardInterrupt:
    # With keyboard interrupt the OLED displays that the menu is paused.
    oled.fill(0)
    image = Image.new('1', (WIDTH, HEIGHT))  
    draw = ImageDraw.Draw(image)
    oled.show() 
    draw.text((PADDING + 10, PADDING + 20), 'MENU PAUSED', font=highlighted, fill=255)
    oled.image(image)
    oled.show()                                 
finally:
    print("Closing Loop")
    loop.close()