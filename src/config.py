class Config:
    # 设备信息
    device_id = "esp32-001"  # 替换为你的设备ID
    SSID = "TP-LINK_630A"
    WIFI_PWD = "13141314"
    MQTT_TOPIC_REQUEST = f"ai/{device_id}/request".encode()  # 发送请求的主题
    MQTT_TOPIC_RESPONSE = [
        f"ai/{device_id}/asr".encode(),
        f"ai/{device_id}/llm".encode(),
        f"ai/{device_id}/tts".encode(),
    ]  # 接收回复的主题
    BUTTON_PIN = 40  # GPIO40 接按钮，按下时接地
    I2C_SCL_PIN = 42
    I2C_SDA_PIN = 41
