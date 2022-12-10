import time
import board
import busio  # importing the I2C bus
import adafruit_ads1x15.ads1015 as ADS  # importing the analog digital converter named: ADS
from adafruit_ads1x15.analog_in import AnalogIn


def values():
    if chan.voltage > 2.400:
        print('The soil is dry!')
    elif 1.700 < chan.voltage < 2.400:
        print('The soil is moist')
    elif chan.voltage < 1.700:
        print('The soil is too wet')


i2c = busio.I2C(board.SCL, board.SDA)  # creating the I2C bus
ads = ADS.ADS1015(i2c)  # creating the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # creating single-ended input on channel 0


while True:
    values()
    time.sleep(0.5)
