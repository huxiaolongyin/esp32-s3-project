from umqtt.simple import MQTTClient  # type: ignore

# === MQTT 配置 ===
MQTT_BROKER = "112.124.69.152"  # 你的 Ubuntu 服务器 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32s3_client"  # 唯一客户端 ID
# MQTT_TOPIC_REQUEST = b"esp32s3/request"  # 发送请求的主题
# MQTT_TOPIC_RESPONSE = b"esp32s3/response"  # 接收回复的主题


# 连接 MQTT
def connect():
    print("Connecting to MQTT broker...")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("✅ MQTT Connection successful!")
    return client
