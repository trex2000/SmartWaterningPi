"""!Records the soils moisture and displays on OLED. 
"""

# Imports
import time
import datetime
import adafruit_ads1x15.ads1015 as ADS  # Digital-analog converter as ADS.
import board
import busio  # I2C bus.
from adafruit_ads1x15.analog_in import AnalogIn
from getpass import getpass  
from mysql.connector import connect, Error 
import RPi.GPIO as GPIO
import adafruit_ssd1306 
from PIL import Image, ImageDraw, ImageFont


# Global Constants of the soil moisture sensor
## Creating the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
## Creating the ADC object using the I2C bus.
ads = ADS.ADS1015(i2c)  
##  Creating single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)  
## Setting hostname for PhpMyAdmin connection
HOSTNAME = 'localhost'
## Input PhpMyAdmin username to connect.
USERNAME = input('Enter your username: ')
## Input PhpMyAdmin password to connect.
PASSWORD = getpass('Enter your password: ')
## Setting the database on PhpMyAdmin.
DATABASE = 'smartwatering'
## The soil moisture sensor's name.
device_name = 'ADS 1X15'
##  The date when the data was recorded. 
now = datetime.datetime.now()
## The date format year:month:day hour:minute:second. 
date = now.strftime('%Y-%m-%d %H:%M:%S')
## Raw value
raw_value = chan.value
## The raw value converted to percentage.
percentage = int(100 * 8000 / int(raw_value))
## Converted the integer into a string with %.
converted_percentage = format(percentage, 'd') + '%'
## The values are classificated.
if chan.value > 18400:
    classification = 'dry'
elif 8000 < chan.value < 18400:
    classification = 'moist'
elif chan.value < 8000:
    classification = 'wet'

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
## The oled display will be redrawn if it's True. 
redrawNeeded_soilmoisturefile = True


#Functions
def insert_soil_moisture_table(device_name, date, raw_value, converted_percentage, classification):
    """!Inserts data to PhpMyAdmin tables.

    After succesful connection inserts the requested data to PhpMyAdmin's SOIL_MOISTURE table.
    Displays on OLED the current moisture of the soil. 
    """
    #Global constants 
    global HOSTNAME, USERNAME, PASSWORD, DATABASE, redrawNeeded_soilmoisturefile, PADDING
    try:
        # Establishing a connection.
        with connect(                  
                host=HOSTNAME,           
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
        ) as connection:
            # Inserting records in the table by passing the INSERT query to cursor.execute().
            # This should accept the MySQL query and execute it on the connected MySQL database.
            soil_moisture_query = "INSERT INTO SOIL_MOISTURE (DEVICE_NAME, DATE, RAW_VALUE, PERCENTAGE, CLASSIFICATION)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            soil_moisture_records = (device_name, date, raw_value, converted_percentage, classification)
            with connection.cursor() as cursor:
                # Passing the query and records to cursor.execute(), which performs the required execution.
                cursor.execute(soil_moisture_query, soil_moisture_records)
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # Closing the cursor and resets all results.
        connection.close()  # The connection object return to the connection pool.
    if redrawNeeded_soilmoisturefile:
        # Displays the current moisture value in percentage on OLED 
        redrawNeeded_soilmoisturefile = False
        oled.fill(0)
        image = Image.new('1', (WIDTH, HEIGHT))  
        draw = ImageDraw.Draw(image)
        oled.show()
        draw.text((PADDING, PADDING + 10), 'Current moisture\n of the soil:', font= ImageFont.truetype('DejaVuSerif.ttf', 13), fill=255)
        draw.text((PADDING + 75, PADDING + 28), converted_percentage, font= ImageFont.truetype('DejaVuSerif.ttf', 13), fill=255)
        oled.image(image)
        oled.show()
        