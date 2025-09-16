# mqtt_server.py - 部署在云服务器或 Raspberry Pi 上

import json
import os
import time
from datetime import datetime

import paho.mqtt.client as mqtt
from openai import OpenAI

# === 配置区域 ===
MQTT_BROKER = "112.124.69.152"  # 你的 Ubuntu 服务器 IP
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "esp32s3/request"
MQTT_TOPIC_RESPONSE = "esp32s3/response"

# OpenAI API 配置（推荐使用环境变量，避免泄露）
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY", "sk-wedekzslvzzgekpxgqepyrebwklmysvsphdubyffmurjxkjj"
)
OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
OPENAI_MODEL = "Qwen/Qwen2.5-32B-Instruct"

# 初始化 OpenAI 客户端
OpenAIclient = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# MQTT 客户端实例
client = mqtt.Client(client_id="openai-gateway-server")


def log(msg):
    """带时间戳的日志输出"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def on_connect(client, userdata, flags, rc):
    """MQTT 连接成功回调"""
    if rc == 0:
        log(f"✅ 成功连接到 MQTT 服务器 {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC_REQUEST)
        log(f"🔔 订阅主题: {MQTT_TOPIC_REQUEST}")
    else:
        log(f"❌ MQTT 连接失败，错误码: {rc}")


def on_disconnect(client, userdata, rc):
    """MQTT 断开连接回调"""
    log(f"⚠️ MQTT 已断开连接，退出码: {rc}，正在重连...")
    time.sleep(3)
    client.reconnect()


def on_message(client, userdata, msg):
    """处理收到的请求消息"""
    if msg.topic == MQTT_TOPIC_REQUEST:
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)
            prompt = data.get("prompt", "").strip()

            if not prompt:
                raise ValueError("请求内容为空")

            log(f"📩 收到请求: {prompt}")

            # 调用 OpenAI
            response = OpenAIclient.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                timeout=10,
            )
            reply = response.choices[0].message.content.strip()

            print(reply)

            # 发送响应回 ESP32
            client.publish(MQTT_TOPIC_RESPONSE, reply)
            log(f"📤 已回复: {reply}")

        except json.JSONDecodeError:
            error_msg = "错误: 请求不是有效的 JSON"
            log(f"❌ {error_msg}")
            client.publish(MQTT_TOPIC_RESPONSE, error_msg)
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            log(f"❌ {error_msg}")
            client.publish(MQTT_TOPIC_RESPONSE, error_msg)


# 设置回调函数
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 尝试连接 MQTT
log("🚀 启动 MQTT-OpenAI 网关...")
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        log(f"⚠️ 连接失败: {e}，3秒后重试...")
        time.sleep(3)
