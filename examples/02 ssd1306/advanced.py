"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Raspberry Pi Pico SSD1306 OLED Display (MicroPython)     ┃
┃                                                          ┃
┃ A program to display Raspberry Pi logo, text, and a      ┃
┃ simple timer animation on an SSD1306 OLED display        ┃
┃ connected to a Raspberry Pi Pico.                        ┃
┃                                                          ┃
┃ Copyright (c) 2023 Anderson Costa                        ┃
┃ GitHub: github.com/arcostasi                             ┃
┃ License: MIT                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import utime

pix_res_x = 128
pix_res_y = 32


def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]

    if not i2c_addr:
        print("No I2C Display Found")
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))

    return i2c_dev


def display_logo(oled):
    # Display the Raspberry Pi logo on the OLED
    # icon_data = bytearray(['0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff', '0xff'])
    buffer = bytearray(
        b"\x00\x00\x00\x00\x00\x00\x1f\x80\x60\x60\x0f\x00\x19\x80\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00"
    )
    fb = framebuf.FrameBuffer(buffer, 12, 12, framebuf.MONO_HLSB)

    oled.fill(0)
    oled.blit(fb, 104, 0)
    oled.show()


def display_text(oled):
    # Display text on the OLED
    oled.text("Raspberry Pi", 5, 5)
    oled.text("Pico", 5, 15)
    oled.show()


def display_anima(oled):
    # Display a simple timer animation on the OLED
    start_time = utime.ticks_ms()

    while True:
        elapsed_time = (utime.ticks_diff(utime.ticks_ms(), start_time) // 1000) + 1

        # Clear the specific line by drawing a filled black rectangle
        oled.fill_rect(5, 40, oled.width - 5, 8, 0)

        oled.text("Timer:", 5, 30)
        oled.text(str(elapsed_time) + " sec", 5, 40)
        oled.show()
        utime.sleep_ms(1000)


def main():
    i2c_dev = init_i2c(scl_pin=42, sda_pin=41)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    display_logo(oled)
    display_text(oled)
    display_anima(oled)


if __name__ == "__main__":
    main()
