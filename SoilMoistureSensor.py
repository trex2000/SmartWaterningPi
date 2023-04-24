"""!Records the soils moisture. 
"""

# Imports
import datetime
import adafruit_ads1x15.ads1015 as ADS  # Digital-analog converter as ADS.
import board
import busio  # I2C bus.
from adafruit_ads1x15.analog_in import AnalogIn
from mysql.connector import connect, Error # Importing the Python MySQL connector to interact with a MySQL database


# Global Constants of the soil moisture sensor
## Creating the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
## Creating the ADC object using the I2C bus.
ads = ADS.ADS1015(i2c)  
## Creating single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)  
## Setting hostname for MySQL connection
HOSTNAME = 'localhost'
## Setting username for MySQL to connect.
USERNAME = 'szidonia'
## Setting password for MySQL to connect.
PASSWORD = 'bomba98'
## Setting the database on MySQL.
DATABASE = 'smartwatering'
## The soil moisture sensor's name.
device_name = 'ADS 1X15'
## The date when the data was recorded. 
now = datetime.datetime.now()
## The date format year:month:day hour:minute:second. 
date = now.strftime('%Y-%m-%d %H:%M:%S')
## Raw value.
raw_value = chan.value
## The raw value converted to percentage in integer format
int_percentage = int(100 * 8000 / int(raw_value))
## Converted the integer percentage into a string with %.
percentage = format(int_percentage, 'd') + '%'
## The values classified.
if chan.value > 18400:
    classification = 'dry'
elif 8000 < chan.value < 18400:
    classification = 'moist'
elif chan.value < 8000:
    classification = 'wet'


#Functions
def insert_SoilMoistureRecords(device_name, date, raw_value, percentage, classification):
    """!Inserts data to MySQL tables.

    After succesful connection inserts the requested data to MySQL's SOIL_MOISTURE table.
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
            # Inserting records in the table by passing the standard MySQL query.
            soil_moisture_query = "INSERT INTO SOIL_MOISTURE (DEVICE_NAME, DATE, RAW_VALUE, PERCENTAGE, CLASSIFICATION)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            soil_moisture_records = (device_name, date, raw_value, percentage, classification)
            with connection.cursor() as cursor:
                # Passing the query and records to execute function, which performs the required execution.
                cursor.execute(soil_moisture_query, soil_moisture_records)
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
    except ConnectionRefusedError as e:
        print(f'Error is: {e}')  # Prints the connection error if it occurs.
    finally:
        cursor.close()  # Closing the cursor and resets all results.
        connection.close()  # The connection object return to the connection pool.


def get_SoilMoistureRecord():
    """!Gets the last soil moisture record from SQL database.

    After succeful connection gets the last record of the soils moisture from MySQL 'SOIL_MOISTURE' table. 
    This record be returned.  
    """

    #Global constants 
    global HOSTNAME, USERNAME, PASSWORD, DATABASE, current_soilMoisture
    try:
        # Establishing a connection.
        with connect(                  
                host=HOSTNAME,           
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
        ) as connection:
            # Selecting the last record from the table by passing the standrad MySQL query to execute.
            soil_moisture_record = "SELECT PERCENTAGE FROM SOIL_MOISTURE ORDER BY RECORD_ID DESC LIMIT 1"
            with connection.cursor() as cursor:
                # Passing the query to execute function, which performs the required execution.
                cursor.execute(soil_moisture_record)
                last_moistureRecord = cursor.fetchone()
                converted_lastMoistureRecord = ''.join(last_moistureRecord)  # Converting the last record into str else it will be tuple.
                # The MySQL connector doesn't autocommit transactions without commit.
                connection.commit()
                return converted_lastMoistureRecord
    except ConnectionRefusedError as e:
        print(f'Error is: {e}')  # Prints the connection error if it occurs.
    finally:
        cursor.close()  # Closing the cursor and resets all results.
        connection.close()  # The connection object return to the connection pool.