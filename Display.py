import board  # import board pins
import busio
import adafruit_ssd1306  # import the SSD1306 module.
from PIL import Image, ImageDraw, ImageFont
import time

OLED_ADDRESS = 0x3c  # the I2C address of the OLED display
WIDTH = 128  # width size of the display
HEIGHT = 64  # height size of the display
PADDING = 1  # 5 bit space created inside the border, this is also the top of the left corner

i2c = busio.I2C(board.SCL, board.SDA)  # create the I2C instance
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)

i = 1

# initializing the OLED display
# first two parameters: the pixel width, height
# last parameter: the I2C address of the device


def highlight_DHT22():
    global PADDING
    global oled

    # clearing the display
    oled.fill(0)
    oled.show()
    # time.sleep(5)

    # creating a blank image for drawing
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # load the default font
    font = ImageFont.load_default()

    # Drawing on the blank image:
    # first parameter: top left corner where the text going to start
    # second parameter: the text
    # third parameter: the font you are using
    # fourth parameter: color to use for the text
    draw.text((PADDING, PADDING), '~SMART WATERING MENU~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. DHT22 Logging <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Moisture Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Automatic Watering', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Manual Watering', font=font, fill=255)

    oled.image(image)  # display image
    oled.show()


def highlight_Moisture():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    # time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~SMART WATERING MENU~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. DHT22 Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. Moisture Logging <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Automatic Watering', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Manual Watering', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Automatic_Watering():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    # time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~SMART WATERING MENU~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. DHT22 Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Moisture Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Automatic Watering <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Manual Watering', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Manual_Watering():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    # time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~SMART WATERING MENU~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. DHT22 Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Moisture Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Automatic Watering', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Manual Watering <', font=font, fill=255)

    oled.image(image)
    oled.show()


smart_watering = {
    1: highlight_DHT22,
    2: highlight_Moisture,
    3: highlight_Automatic_Watering,
    4: highlight_Manual_Watering
}


def choose_option():
    global i
    userInput = input("write 'a': ")
    if userInput == 'a':
        smart_watering[i]()
    # time.sleep(5)


while True:
    if i <= len(smart_watering):
        choose_option()
    else:
        i = 0
    i = i + 1
