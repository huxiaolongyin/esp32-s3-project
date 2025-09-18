import time

from machine import I2C, Pin  # type: ignore
from writer import Writer

# import msyh  # 你转换后的字体文件
import ssd1306

# 初始化 I2C 和屏幕
i2c = I2C(0, scl=Pin(42), sda=Pin(41))
button = Pin(1, Pin.IN, Pin.PULL_UP)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# 初始化 Writer
# wri = Writer(display, msyh)

# 清屏
display.fill(0)

# 定义一个简单的 WiFi 图标（16x16 像素）
wifi_icon = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# 在屏幕上绘制 WiFi 图标
def draw_wifi_icon(x, y):
    for i in range(len(wifi_icon)):
        for j in range(len(wifi_icon[i])):
            if wifi_icon[i][j] == 1:
                display.pixel(x + j, y + i, 1)


draw_wifi_icon(56, 8)

# # 显示中文
# display.fill(0)
# Writer.set_textpos(display, 0, 0)
# wri.printstring("录音中...")
# display.show()

# time.sleep(1)

# # 显示中文
# display.fill(0)
# Writer.set_textpos(display, 0, 0)
# wri.printstring("播放中...")
# display.show()
