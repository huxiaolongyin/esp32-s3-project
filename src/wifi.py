import time

import network  # type: ignore


def connect():
    # ssid = "Wokwi-GUEST"
    # password=''
    ssid = "TP-LINK_630A"
    password = "13141314"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")

    print(f"\nConnected on IP: {wlan.ifconfig()[0]}")
