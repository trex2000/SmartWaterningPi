import time
import datetime
import adafruit_ads1x15.ads1015 as ADS  # importing the analog digital converter named: ADS
import board
import busio  # importing the I2C bus
from adafruit_ads1x15.analog_in import AnalogIn
from getpass import getpass  # importing the getpass module that prompts the user for a password without echoing
from mysql.connector import connect, Error  # importing the Python MySQL connector to interact with a PhpMyAdmin database

i2c = busio.I2C(board.SCL, board.SDA)  # creating the I2C bus
ads = ADS.ADS1015(i2c)  # creating the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # creating single-ended input on channel 0

# settings for PhpMyAdmin connection
HOSTNAME = 'localhost'
USERNAME = input('Enter your username: ')
PASSWORD = getpass('Enter your password: ')
DATABASE = 'smartwatering'


def insert_soil_moisture_table(device_name, date, raw_value, percentage, classification):
    global HOSTNAME  # using the globally defined variable
    global USERNAME
    global PASSWORD
    global DATABASE
    try:  # using a "try … except" block to catch and print any exceptions that might encounter
        with connect(                    # establishing a connection
                host=HOSTNAME,           # this function takes in the "host", "user", "password", "database" parameters
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
        ) as connection:
            # to insert records in the table, you need to pass the INSERT query to cursor.execute(),
            # which accepts a MySQL query and executes the query on the connected MySQL database
            soil_moisture_query = "INSERT INTO SOIL_MOISTURE (DEVICE_NAME, DATE, RAW_VALUE, PERCENTAGE, CLASSIFICATION)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            soil_moisture_records = (device_name, date, raw_value, percentage, classification)
            with connection.cursor() as cursor:
                # passing the query and records to cursor.execute(), which performs the required execution
                cursor.execute(soil_moisture_query, soil_moisture_records)
                # the MySQL connector does not autocommit transactions, must use the connection.commit() statement
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # closes the cursor, resets all results
        connection.close()  # the connection object return to the connection pool


try:
    while True:
        device_name = 'ADS 1X15'    # the soil moisture sensor's name
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')    # datetime with h:m:s
        raw_value = chan.value
        percentage = int(100 * 8000 / int(raw_value))
        if chan.value > 18400:
            classification = 'dry'
        elif 8000 < chan.value < 18400:
            classification = 'moist'
        elif chan.value < 8000:
            classification = 'wet'
        insert_soil_moisture_table(device_name, date, raw_value, format(percentage, 'd') + '%', classification)
        time.sleep(5)
except(IOError, TypeError) as e:
    print(e)
except KeyboardInterrupt:
    print('stopping')
