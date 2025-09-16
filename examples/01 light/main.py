import time

from machine import Pin

led = Pin(9, Pin.OUT)  # GPIO2 接 LED

while True:
    led.value(1)  # 开灯
    time.sleep(1)
    led.value(0)  # 关灯
    time.sleep(1)
