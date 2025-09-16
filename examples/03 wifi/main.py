# examples/03 wifi/main.py
import time
import network
from umqtt.simple import MQTTClient
import json

# === WiFi 配置 ===
WIFI_SSID = "TP-LINK_630A"
WIFI_PASSWORD = "13141314"

# === MQTT 配置 ===
MQTT_BROKER = "112.124.69.152"  # 你的 Ubuntu 服务器 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32s3_client"  # 唯一客户端 ID
MQTT_TOPIC_REQUEST = b"esp32s3/request"  # 发送请求的主题
MQTT_TOPIC_RESPONSE = b"esp32s3/response"  # 接收回复的主题

# === 用户输入提示 ===
USER_PROMPT = "Hello, what's the weather like today?"  # 可替换为传感器数据、按钮触发等


# 连接 WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print(".", end="")
        print(f"\n✅ WiFi Connection successful!IP: {wlan.ifconfig()[0]}")


# 连接 MQTT
def connect_mqtt():
    print("Connecting to MQTT broker...")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("✅ MQTT Connection successful!")
    return client


# 回调函数：收到服务器回复时触发
def on_message(topic, msg):
    print(f"📥 Received an AI reply: {msg.decode()}")


# 主程序
def main():
    connect_wifi()
    client = connect_mqtt()

    # 设置消息回调（接收 AI 回复）
    client.set_callback(on_message)
    client.subscribe(MQTT_TOPIC_RESPONSE)
    print(f"🔔 Subscribed to the reply topic: {MQTT_TOPIC_RESPONSE.decode()}")

    # 发送一次测试请求（可改为定时或按键触发）
    request_data = {"prompt": USER_PROMPT}
    client.publish(MQTT_TOPIC_REQUEST, json.dumps(request_data))
    print(f"📤 A request has been sent: {request_data}")

    # 循环监听回复（非阻塞）
    while True:
        try:
            client.check_msg()  # 检查是否有新消息
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ MQTT error: {e}")
            print("🔄 Reconnect MQTT...")
            client.disconnect()
            time.sleep(2)
            client = connect_mqtt()
            client.set_callback(on_message)
            client.subscribe(MQTT_TOPIC_RESPONSE)


# 启动主程序
if __name__ == "__main__":
    main()
