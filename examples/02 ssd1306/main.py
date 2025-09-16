import ssd1306
from machine import I2C, Pin

i2c = I2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text("Hello Python!", 0, 0)
display.show()
