import time

import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")

print("正在连接 WiFi...")
while not wlan.isconnected():
    time.sleep(1)
    print(".", end="")

print(f"\n连接成功！IP: {wlan.ifconfig()[0]}")
