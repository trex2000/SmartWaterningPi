import time
import board
import busio  # importing the I2C bus
import adafruit_ads1x15.ads1015 as ADS  # importing the analog digital converter named: ADS
from adafruit_ads1x15.analog_in import AnalogIn


def values():
    x = 100 * 8000 / int(chan.value)
    percentage = int(x)
    if chan.value > 18400:
        print(f'The soil is {percentage}% dry.')
    elif 8000 < chan.value < 18400:
        print(f'The soil is {percentage}% moist.')
    elif chan.value < 8000:
        print(f'The soil is {percentage}% wet. ')


i2c = busio.I2C(board.SCL, board.SDA)  # creating the I2C bus
ads = ADS.ADS1015(i2c)  # creating the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0)  # creating single-ended input on channel 0


while True:
    values()
    time.sleep(2)
