import time
import board
import busio  # importing the I2C bus
import adafruit_ads1x15.ads1015 as ADS  # importing the analog digital converter named: ADS
from adafruit_ads1x15.analog_in import AnalogIn


def values():
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))


i2c = busio.I2C(board.SCL, board.SDA)  # creating the I2C bus
ads = ADS.ADS1015(i2c)  # creating the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # creating single-ended input on channel 0


print("{:>5}\t{:>5}".format('raw', 'v'))  # creating a table with raw and voltage values

while True:
    values()
    time.sleep(0.5)
