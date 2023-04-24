"""! @mainpage Smart Watering System

@brief This system uses sensors to measure the actual moisture of the soil and digital temperature and humidity sensor to measure 
the surrounding air.
The system also has an OLED display which displays the menu of the system. You can check out the current moisture of the soil, temperature,
humidity and also turn on or off the automatic watering based on the soil moisture data. 
The data from the sensors are logged into an SQL database.
"""

"""!Displays the menu and the current values, statuses.
"""


# Imports
import os  
import asyncio 
import board    
import busio
import RPi.GPIO as GPIO
import adafruit_ssd1306 
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from mysqlx import Error
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
## 1 bit space created inside the border.
PADDING = 1
## Created I2C instance.
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)
## Parsed the xml file.
tree = ET.parse('SmartWateringMenu.xml')
root = tree.getroot()
## The base font of the menu. 
font = ImageFont.truetype('DejaVuSerif.ttf', 10)
## Selected items font on the menu.
highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)
## Menu's page index.
menuPage = 0
## Selected item's index on the menu.
selectedItem = 0 
## The oled display will be redrawn if it's True. 
redrawNeeded = True
## Longer sleep time.
T_LONG_SLEEP = 10 # 10 second
## Set init value of measured humidity.
currentHum = -10000
## Set init value of measured temperature.
currentTemp = -10000
## Set init value of measured moisture.
currentMoist = -10000
## Define event loop.
loop = asyncio.get_event_loop()
## State of the humidity sensor.
stateHum = 'Deactivated'
## The humidity sensor is off, doesn't collect records.
runningHumiditySensor = False
## State of the moisture sensor.
stateMoist = 'Deactivated'
## The Moisture sensor is off, doesn't collect records.
runningMoistureSensor = False


#Functions
def setup():
    """!Ghaters the modules setups
    """
    setup_button()


def main_menu():
        """!Navigating throught the menu
        
        The connected OLED displays the menu with the currently active menu point which is highlighted.
        Push Button1 shall be used to navigate through the menu and Push Button2 to select an option which will navigate to another menu or
        runs a function. 
        """   

        # Global values 
        global font, highlighted, menuPage, selectedItem, button1PressedEvent, redrawNeeded
        ## Number of elements in the main_menu.
        numberOfElements = len(root[menuPage])
        ## Last item in the menu.
        lastElement = int(numberOfElements) - 1  # After indexes there is less element. 
        if redrawNeeded:  # Redraws the OLED.
            redrawNeeded = False 
            oled.fill(0)
            image = Image.new('1', (WIDTH, HEIGHT))  
            draw = ImageDraw.Draw(image)
            oled.show()  # OLED display is cleared.
            for i in range(0, numberOfElements):
                if i == selectedItem:  # The selected item should be highlighted.
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=highlighted, fill=255)
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[menuPage][i].text, font=font, fill=255)
            oled.image(image)
            oled.show()  # Shows the menu with the active menu point highlighted.
        if button1PressedEvent.is_set():  # Checks if event was fired.      
            if selectedItem < lastElement:  # If the button is pressed (and the selected item is less than the last element)
                #then the selected item should be the next one.
                selectedItem = selectedItem + 1
                redrawNeeded = True  # Redraw is needed, otherwise the menu overwrites itself over and over again.
            else:  # If the selected item is the last one, and you press Push Button 1, the next selected item will be the first element.
                selectedItem = 0 
                redrawNeeded = True
        button1PressedEvent.clear()  # The event is marked as 'not set' via this function.
        if button2PressedEvent.is_set():  # Checks if the event was fired. 
            # Checks if the selected item is not the last one.             
            if selectedItem != lastElement: 
                if root[menuPage][selectedItem].get('callable')=='true':  # If the item is callable, it calls and displays the data.
                    ## Records from different sensors, which will be displayed in the future.                   
                    recordToDisplay = RunSelectedFunction()
                    oled.fill(0)
                    image = Image.new('1', (WIDTH, HEIGHT))  
                    draw = ImageDraw.Draw(image)
                    oled.show() 
                    draw.text((PADDING, PADDING), recordToDisplay, font=highlighted, fill=255)
                    draw.text((PADDING, PADDING + 30), '2. Exit', font=font, fill=255)
                    oled.image(image)
                    oled.show()            
                else:  # If not callable dislpays the next menu.
                    nextMenuItemToFind=root[menuPage][selectedItem].text
                    for j in range(0, numberOfElements):
                        if root[j].get('title')  == nextMenuItemToFind:
                            menuPage = j
                            selectedItem = 0  # The first item on the list is selected.
                            redrawNeeded = True
                            break
            else:  # If the last item is selected the OLED displays the previous menu page.
                selectedItem = menuPage - 1  # The selected item is the one which submenu was opened.
                menuPage = 0
                redrawNeeded = True  
            if root[menuPage][selectedItem].text == '5. Power off':  # If the Power off is selected the os should shut down.
                oled.fill(0)
                oled.show()
                os.system('sudo poweroff')                     
        button2PressedEvent.clear()  # The event is marked as 'not set' via this function.


        
def RunSelectedFunction():
    """!Calls the functions.

    If the selected item's text in the current page is equal to the given string than runs the approriate function from a different module.
    This functions return a value, that's why this functions are defined as a variable which are also returned.  
    """

    global currentTemp, currentHum, currentMoist, stateHum, stateMoist, runningHumiditySensor, runningMoistureSensor
    if root[menuPage][selectedItem].text == '2. Current temperature':
        currentTemp = get_TemperatureRecord()
        if currentTemp == -10000: 
            currentTemp = 'N/A'
        return f'1. Sensor\n value: {currentTemp}'
    elif root[menuPage][selectedItem].text == '3. Current humidity':
        currentHum = get_HumidityRecord()
        if currentHum == -10000: 
            currentHum = 'N/A'
        return f'1. Sensor\n value: {currentHum}'
    elif root[menuPage][selectedItem].text == '2. Current moisture':
        currentMoist = get_SoilMoistureRecord()
        if currentMoist == -10000: 
            currentMoist = 'N/A'
        return f'1. Sensor\n value: {currentMoist}'
    elif root[menuPage][selectedItem].text == '1. Logging T/H':
        if runningHumiditySensor == False:
            runningHumiditySensor = True
            stateHum = 'Activated'
        else:
            runningHumiditySensor = False
            stateHum = 'Deactivated'
        return f'1. {stateHum}'
    elif root[menuPage][selectedItem].text == '1. Logging moisture':
        if runningMoistureSensor == False:
            runningMoistureSensor = True
            stateMoist = 'Activated'
        else:
            runningMoistureSensor = False
            stateMoist = 'Deactivated'
        return f'1. {stateMoist}'


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

    The humidity sensor collects and inserts records in case when is activated.
    """

    #Global values
    global runningHumiditySensor
    while True:
        if runningHumiditySensor == True:
            insert_HumidityRecords(device_name, date, temperature_f, temperature_c, humidity)
        await asyncio.sleep(T_LONG_SLEEP)


async def async_task_insert_SoilMoistureRecords():
    """!Define a coroutine for inserting moisture records that takes in a future.

    The moisture sensor collects and inserts records in case when is activated.
    """

    #Global values
    global runningMoistureSensor
    while True:
        if runningMoistureSensor == True:
            insert_SoilMoistureRecords(device_name, date, raw_value, percentage, classification)
        await asyncio.sleep(T_LONG_SLEEP)


async def async_task_manage_main_menu():
    """!Define a coroutine for main menu that takes in a future.
    """

    while True:
        main_menu()
        await asyncio.sleep(T_SLEEP)


setup()

# Subsequently starts asyncio based event loop and have it run indefinitely until the program comes to an end
try:
    asyncio.ensure_future(async_task_manageButton1())
    asyncio.ensure_future(async_task_manageButton2())
    asyncio.ensure_future(async_task_insert_HumidityRecords())
    asyncio.ensure_future(async_task_insert_SoilMoistureRecords())
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
except ConnectionError:
    oled.fill(0)
    image = Image.new('1', (WIDTH, HEIGHT))  
    draw = ImageDraw.Draw(image)
    oled.show() 
    draw.text((PADDING, PADDING), '1. SQL connection not found', font=highlighted, fill=255)
    draw.text((PADDING, PADDING + 10), '2. Exit', font=font, fill=255)
    oled.image(image)
    oled.show() 
finally:
    print("Closing Loop")
    loop.close()