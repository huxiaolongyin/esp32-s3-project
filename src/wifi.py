import time

import network  # type: ignore


def connect(ssid: str, password: str):
    """连接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting WiFi...")
    retries = 0
    while not wlan.isconnected() and retries < 20:
        time.sleep(1)
        retries += 1
        print(".", end="")
    if not wlan.isconnected():
        raise Exception("Could not connect to WiFi")
    print("✅ WiFi connected")
    print(f"\nConnected on IP: {wlan.ifconfig()[0]}")
