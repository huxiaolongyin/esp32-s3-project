# openai_mqtt_bridge.py - 部署在云服务器或 Raspberry Pi 上

import json
import os

import paho.mqtt.client as mqtt
from openai import OpenAI

# 配置
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "esp32s3/request"
MQTT_TOPIC_RESPONSE = "esp32s3/response"


OpenAIclient = OpenAI(
    api_key="sk-wedekzslvzzgekpxgqepyrebwklmysvsphdubyffmurjxkjj",
    base_url="https://api.siliconflow.cn/v1",
)


# MQTT 回调：收到请求时调用 OpenAI
def on_message(client, userdata, msg):
    if msg.topic == MQTT_TOPIC_REQUEST:
        try:
            data = json.loads(msg.payload.decode())
            prompt = data.get("prompt", "")
            print(f"📩 收到请求: {prompt}")

            response = OpenAIclient.chat.completions(
                model="Qwen/Qwen2.5-32B-Instruct",
                messages=[{"role": "user", "content": prompt}],
            )
            reply = response.choices[0].message.content.strip()

            # 发回响应
            client.publish(MQTT_TOPIC_RESPONSE, reply)
            print(f"📤 已回复: {reply}")

        except Exception as e:
            print(f"❌ 处理失败: {e}")
            client.publish(MQTT_TOPIC_RESPONSE, f"错误: {str(e)}")


# 连接 MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC_REQUEST)

print("🚀 MQTT-OpenAI 网关启动中...")
client.loop_forever()
