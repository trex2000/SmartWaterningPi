from machine import Pin, I2c
import ssd1306

i2c = I2C(sda=Pin(2), scl=Pin(3))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text('Hello!', 0, 0, 1)
display.show()