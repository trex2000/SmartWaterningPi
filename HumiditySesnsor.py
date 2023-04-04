import time
import datetime
import board
import adafruit_dht
from getpass import getpass  # importing the getpass module that prompts the user for a password without echoing
from mysql.connector import connect, Error  # importing the Python MySQL connector to interact with a PhpMyAdmin database


# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)


# settings for PhpMyAdmin connection
HOSTNAME = 'localhost'
USERNAME = input('Enter your username: ')
PASSWORD = getpass('Enter your password: ')
DATABASE = 'smartwatering'


def insert_humidity_table(device_name, date, temperature_f, temperature_c, humidity):
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
            humidity_query = "INSERT INTO HUMIDITY (DEVICE_NAME, DATE, TEMPERATURE_F, TEMPERATURE_C, HUMIDITY)" \
                                  "VALUES (%s, %s, %s, %s, %s)"
            humidity_records = (device_name, date, temperature_f, temperature_c, humidity)
            with connection.cursor() as cursor:
                # passing the query and records to cursor.execute(), which performs the required execution
                cursor.execute(humidity_query, humidity_records)
                # the MySQL connector does not autocommit transactions, must use the connection.commit() statement
                connection.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()  # closes the cursor, resets all results
        connection.close()  # the connection object return to the connection pool


try:
    while True:
        device_name = 'DHT22'    # the soil moisture sensor's name
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')    # datetime with h:m:s
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = int(dhtDevice.humidity)
        insert_humidity_table(device_name, date, format(temperature_f, '.1f') + '°F', format(temperature_c, '.1f') + '°C', format(humidity, 'd') + '%')
        time.sleep(5)
except(IOError, TypeError) as e:
    print(e)
except KeyboardInterrupt:
    print('stopping')
