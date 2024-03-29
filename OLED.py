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


# initializing the OLED display
# first two parameters: the pixel width, height
# last parameter: the I2C address of the device


def highlight_DHT22_Logging():
    global PADDING
    global oled

    # clearing the display
    oled.fill(0)
    oled.show()
    time.sleep(5)

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


def highlight_Moisture_Logging():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

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
    time.sleep(5)

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
    time.sleep(5)

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


def highlight_DHT22_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. Logging <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Current Temperature', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current Humidity', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. Current Temperature <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current Humidity', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Current Temperature', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Current Humidity <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_opt4():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Current Temperature', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current Humidity', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. Logging <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Current Value', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. Current Value <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. Logging', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. Current Value', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Automatic_Watering_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Automatic Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. ON <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Automatic_Watering_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Automatic Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON ', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. OFF <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Automatic_Watering_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Automatic Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON ', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Current State <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Automatic_Watering_opt4():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Automatic Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Manual_Watering_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Manual Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. ON <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Manual_Watering_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Manual Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. OFF <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Manual_Watering_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Manual Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Current State <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Manual_Watering_opt4():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Manual Watering~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_Logging_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. ON <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_Logging_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. OFF <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_Logging_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Current State <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_DHT22_Logging_opt4():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~DHT22 Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_Logging_opt1():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '> 1. ON <', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_Logging_opt2():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '> 2. OFF <', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_Logging_opt3():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '> 3. Current State <', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '4. Back', font=font, fill=255)

    oled.image(image)
    oled.show()


def highlight_Moisture_Logging_opt4():
    global PADDING
    global oled

    oled.fill(0)
    oled.show()
    time.sleep(5)

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    draw.text((PADDING, PADDING), '~Moisture Logging~', font=font, fill=255)
    draw.text((PADDING, PADDING + 20), '1. ON', font=font, fill=255)
    draw.text((PADDING, PADDING + 30), '2. OFF', font=font, fill=255)
    draw.text((PADDING, PADDING + 40), '3. Current State', font=font, fill=255)
    draw.text((PADDING, PADDING + 50), '> 4. Back <', font=font, fill=255)

    oled.image(image)
    oled.show()
