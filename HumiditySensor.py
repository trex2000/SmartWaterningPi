"""!Records the humidity and temperature
"""

# Imports
import time
import datetime
import board
import adafruit_dht
from mysql.connector import connect, Error  # importing the Python MySQL connector to interact with a PhpMyAdmin database


# Global Constants  
## Initialise the dht device, with data pin connected to.
dhtDevice = adafruit_dht.DHT22(board.D4)
## The DHT sensor measures the data.
measure_data =dhtDevice.measure()
## Setting hostname for PhpMyAdmin connection
HOSTNAME = 'localhost'
## Input PhpMyAdmin username to connect.
USERNAME = 'szidonia'
## Input PhpMyAdmin password to connect.
PASSWORD = 'bomba98'
## Setting the database on PhpMyAdmin.
DATABASE = 'smartwatering'
## The humidity sensor's name.
device_name = 'DHT22'
##  The date when the data was recorded. 
now = datetime.datetime.now()
## The date format year:month:day hour:minute:second. 
date = now.strftime('%Y-%m-%d %H:%M:%S')  
## Temperature in degrees Celsius , integer format.
int_temperature_c = dhtDevice.temperature
## Temperature in degrees Celsius converted into a string with °C
temperature_c = format(int_temperature_c, '.1f') + '°C'
## Temperature in degrees Fahrenheit , integer format.
int_temperature_f = int_temperature_c * (9 / 5) + 32
## Temperature in degrees Fahrenheit converted into a string with °F
temperature_f = format(int_temperature_f, '.1f') + '°F'
## Humidity, int format.
int_humidity = int(dhtDevice.humidity)
## Humidity converted into a string with %.
humidity = format(int_humidity, 'd') + '%'
## Current humidity.
current_humidity = 0
## Current temperature
current_temperature = 0

# Functions 
def insert_HumidityRecords(device_name, date, temperature_f, temperature_c, humidity):
    """!Inserts data to PhpMyAdmin tables.
    
    After succesful connection inserts the requested data to PhpMyAdmin's HUMIDITY table.
    """
    #Global constants
    global HOSTNAME, USERNAME, PASSWORD, DATABASE  
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
            humidity_query = "INSERT INTO HUMIDITY (DEVICE_NAME, DATE, TEMPERATURE_F, TEMPERATURE_C, HUMIDITY)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            humidity_records = (device_name, date, temperature_f, temperature_c, humidity)
            with connection.cursor() as cursor:
                # Passing the query and records to cursor.execute(), which performs the required execution
                cursor.execute(humidity_query, humidity_records)
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # Closing the cursor, resets all results.
        connection.close()  # The connection object return to the connection pool.


def get_HumidityRecord():
    """!Gets the last humidity record from SQL database.

    After succeful connection gets the last record of humidity from PhpMyAdmin 'HUMIDITY' table. 
    This record will be defined as a variable.  
    """
    #Global constants 
    global HOSTNAME, USERNAME, PASSWORD, DATABASE, current_humidity
    try:
        # Establishing a connection.
        with connect(                  
                host=HOSTNAME,           
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
        ) as connection:
            # Selecting the last record from the table by passing the standrad MySQL querys to execute.
            humidity_record = "SELECT HUMIDITY FROM HUMIDITY ORDER BY RECORD_ID DESC LIMIT 1"
            with connection.cursor() as cursor:
                cursor.execute(humidity_record)
                last_humidityRecord = cursor.fetchone()
                converted_lastHumidityRecord = ''.join(last_humidityRecord)  # Converting the last record into str else it will be tuple
                current_humidity = converted_lastHumidityRecord
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # Closing the cursor and resets all results.
        connection.close()  # The connection object return to the connection pool.


def get_TemperatureRecord():
    """!Gets the last humidity record from SQL database.

    After succeful connection gets the last record of temperature from PhpMyAdmin 'TEMPERATURE_C' table. 
    This record will be defined as a variable.  
    """
    #Global constants 
    global HOSTNAME, USERNAME, PASSWORD, DATABASE, current_temperature
    try:
        # Establishing a connection.
        with connect(                  
                host=HOSTNAME,           
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
        ) as connection:
            # Selecting the last record from the table by passing the standrad MySQL querys to execute.
            humidity_record = "SELECT TEMPERATURE_C FROM HUMIDITY ORDER BY RECORD_ID DESC LIMIT 1"
            with connection.cursor() as cursor:
                cursor.execute(humidity_record)
                last_temperatureRecord = cursor.fetchone()
                converted_lastTemperatureRecord = ''.join(last_temperatureRecord)  # Converting the last record into str else it will be tuple
                current_temperature = converted_lastTemperatureRecord
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # Closing the cursor and resets all results.
        connection.close()  # The connection object return to the connection pool.