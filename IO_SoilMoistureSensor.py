import time
import datetime
import adafruit_ads1x15.ads1015 as ADS  # importing the analog digital converter named: ADS
import board
import busio  # importing the I2C bus
from adafruit_ads1x15.analog_in import AnalogIn
from getpass import getpass
from mysql.connector import connect, Error

i2c = busio.I2C(board.SCL, board.SDA)  # creating the I2C bus
ads = ADS.ADS1015(i2c)  # creating the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # creating single-ended input on channel 0


def insert_soil_moisture_table(device_name, date, raw_value, percentage, classification):
    try:
        with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database='smartwatering'
        ) as connection:
            soil_moisture_query = "INSERT INTO SOIL_MOISTURE (DEVICE_NAME, DATE, RAW_VALUE, PERCENTAGE, CLASSIFICATION)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            soil_moisture_records = (device_name, date, raw_value, percentage, classification)
            with connection.cursor() as cursor:
                print('cursor')
                cursor.execute(soil_moisture_query, soil_moisture_records)
                print('executed')
                connection.commit()
                print('commited')
    except Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


try:
    while True:
        record_id = 3
        device_name = 'ADS 1X15'
        date = datetime.datetime.now()
        raw_value = 3  # int(chan.value())
        percentage = 3  # 100 * 8000 / raw_value
        classification = 'class'
        insert_soil_moisture_table(device_name, date, raw_value, percentage, classification)
        time.sleep(5)
except(IOError, TypeError) as e:
    print(e)
except KeyboardInterrupt:
    print('stopping')
