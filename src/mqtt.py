from umqtt.simple import MQTTClient  # type: ignore

# MQTT 配置
MQTT_BROKER = "112.124.69.152"  # 你的 Ubuntu 服务器 IP
MQTT_PORT = 7983
MQTT_CLIENT_ID = "esp32s3_client"  # 唯一客户端 ID
MQTT_USERNAME = "esp32"
MQTT_PASSWORD = "Esp32@0920"


# 连接 MQTT
def connect():
    print("Connecting to MQTT broker...")

    client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USERNAME,
        password=MQTT_PASSWORD,
    )
    client.connect()
    print("✅ MQTT Connection successful!")
    return client
