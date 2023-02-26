import board  # import board pins
import busio
import adafruit_ssd1306  # import the SSD1306 module.
from PIL import Image, ImageDraw, ImageFont
import time
import xml.etree.ElementTree as ET

OLED_ADDRESS = 0x3c  # the I2C address of the OLED display
WIDTH = 128  # width size of the display
HEIGHT = 64  # height size of the display
PADDING = 1  # 5 bit space created inside the border, left top corner

i2c = busio.I2C(board.SCL, board.SDA)  # create the I2C instance
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=OLED_ADDRESS)

tree = ET.parse('smart_watering_menu.xml')  # parsed the xml file
root = tree.getroot()


def main_menu():
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('DejaVuSerif.ttf', 10)  # the menu is displayed on oled with the base font
    highlighted = ImageFont.truetype('DejaVuSerif-Bold.ttf', 11)  # selected item is highlighted in the displayed menu
    numberOfElement = len(root[0])  # number of elements in the main_menu
    selectedItem = 0  # first item selected in the menu
    redrawNeeded = True  # the oled display will be redrawn

    while True:
        if redrawNeeded:
            redrawNeeded = False
            oled.fill(0)
            oled.image(image)
            oled.show()  # OLED is cleared
            for i in range(0, numberOfElement):
                if i == selectedItem:  # the selected item should be highlighted
                    draw.text((PADDING, PADDING + (i * 10)), root[0][i].text, font=highlighted, fill=255)
                    oled.image(image)
                    oled.show()
                else:
                    draw.text((PADDING, PADDING + (i * 10)), root[0][i].text, font=font, fill=255)
                    oled.image(image)
                    oled.show()
        userInput = input('write a to navigate: ')
        if userInput == 'a':
            if selectedItem < numberOfElement:  # if the button is pressed (and the selected item is less than the number of elements)
                # then the selected item should be the next one
                selectedItem = selectedItem + 1
                redrawNeeded = True  # redraw is needed, otherwise the menu overwrites itself over and over again
            else:
                selectedItem = 0  # if the selected item is the last one, and you press the button than the next selected item should be the first element
        time.sleep(0.1)


main_menu()
