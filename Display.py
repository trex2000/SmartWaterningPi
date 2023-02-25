import board  # import board pins
import busio
import adafruit_ssd1306  # import the SSD1306 module.
from PIL import Image, ImageDraw, ImageFont
import time
import xml.etree.ElementTree as ET

OLED_ADDRESS = 0x3c  # the I2C address of the OLED display
WIDTH = 128  # width size of the display
HEIGHT = 64  # height size of the display
PADDING_L = 1  # 5 bit space created inside the border, left side
PADDING_T = 1   # 5 bit space inside the border, top side

i2c = busio.I2C(board.SCL, board.SDA)  # create the I2C instance
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)

tree = ET.parse('smart_watering_menu.xml')  # parsed the xml file
root = tree.getroot()
i = 0


for i in (0, 4):
    oled.fill(0)
    oled.show()

    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('DejaVuSerif.ttf', 10)
    highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)

    draw.text((PADDING_L, PADDING_T + (i*10)), root[0][i].text, font=font, fill=255)
    #draw.text((PADDING_L, PADDING_T + 10), root[0][1].text, font=font, fill=255)
    #draw.text((PADDING_L, PADDING_T + 20), root[0][2].text, font=font, fill=255)
    #draw.text((PADDING_L, PADDING_T + 30), root[0][2].text, font=font, fill=255)
    #draw.text((PADDING_L, PADDING_T + 40), root[0][4].text, font=font, fill=255)

    oled.image(image)
    oled.show()









