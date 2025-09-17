import time

import network  # type: ignore


def connect():
    ssid = "Wokwi-GUEST"
    password = ""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Connecting WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")

    print(f"\nConnected on IP: {wlan.ifconfig()[0]}")


if __name__ == "__main__":
    connect()
