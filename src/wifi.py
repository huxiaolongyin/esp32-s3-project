import time

import network  # type: ignore


def connect(ssid: str, password: str, display_obj=None):
    """连接 WiFi 并在 OLED 上显示连接状态"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # 显示“连接中”动画
    if display_obj:
        display_obj.wifi("connecting")

    print("Connecting WiFi...")
    wlan.connect(ssid, password)

    retries = 0
    while not wlan.isconnected() and retries < 20:
        if display_obj:
            display_obj.wifi("connecting")
        else:
            time.sleep(1)
        retries += 1
        print(".", end="")

    if wlan.isconnected():
        print("✅ WiFi connected")
        print(f"\nConnected on IP: {wlan.ifconfig()[0]}")
        # 显示连接成功图标
        if display_obj:
            display_obj.wifi("connected")
    else:
        print("❌ Failed to connect to WiFi")
        # 显示连接失败图标
        if display_obj:
            display_obj.wifi("error")
        raise Exception("Could not connect to WiFi")
