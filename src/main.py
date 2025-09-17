# examples/03 wifi/main.py
import time

from machine import I2C, Pin  # type: ignore

import mqtt
from microphone import record_audio
from speaker import play_audio
# import ssd1306
import wifi


# 设备信息
device_id = "esp32-001"  # 替换为你的设备ID

# === 用户输入提示 ===
USER_PROMPT = "Hello"  # 可替换为传感器数据、按钮触发等

MQTT_TOPIC_REQUEST = f"ai/{device_id}/request".encode()  # 发送请求的主题
MQTT_TOPIC_RESPONSE = [f"ai/{device_id}/asr".encode(),f"ai/{device_id}/llm".encode(),f"ai/{device_id}/tts".encode(), ] # 接收回复的主题

button = Pin(40, Pin.IN, Pin.PULL_UP)  # GPIO01 接按钮，按下时接地

# 屏幕显示
# i2c = I2C(scl=Pin(18), sda=Pin(19))
# display = ssd1306.SSD1306_I2C(128, 64, i2c)

audio_buffer = b""


# 回调函数：收到服务器回复时触发
def on_message(topic, payload):
    if topic == MQTT_TOPIC_RESPONSE[0]:
        print(f"ASR识别: {payload.decode()}")
    elif topic == MQTT_TOPIC_RESPONSE[1]:
        print(f"LLM回复: {payload.decode()}")
    elif topic == MQTT_TOPIC_RESPONSE[2]:
        print(f"TTS音频长度: {len(payload)} 字节")
        play_audio(payload)


# 主程序
def main():
    wifi.connect()
    client = mqtt.connect()
    # 设置消息回调（接收 AI 回复）
    client.set_callback(on_message)
    for topic in MQTT_TOPIC_RESPONSE:
        client.subscribe(topic)

    print(f"🔔 Subscribed to the reply topic")

    # 添加重连状态标记
    mqtt_connected = True

    while True:
        try:
            # 检查按钮是否按下
            if button.value() == 0:  # 按钮按下
                # 防抖处理
                time.sleep(0.1)
                if button.value() == 0:  # 确认按钮确实按下
                    audio_data = record_audio()
                    # 发送一次测试请求
                    # request_data = {"prompt": USER_PROMPT}
                    client.publish(MQTT_TOPIC_REQUEST, audio_data)
                    print(f"📤 A request has been sent")

                    # 等待按钮释放
                    while button.value() == 0:
                        time.sleep(0.01)

            # 非阻塞地检查 MQTT 消息
            client.check_msg()

            # 短暂延时，避免过度占用 CPU
            time.sleep(0.1)

        except Exception as e:
            print(f"⚠️ MQTT error: {e}")
            print("🔄 Reconnect MQTT...")

            try:
                client.disconnect()
            except:
                pass

            time.sleep(2)

            try:
                client = mqtt.connect()
                client.set_callback(on_message)
                client.subscribe(MQTT_TOPIC_RESPONSE)
                print(f"🔔 Subscribed to the reply topic")
            except Exception as reconnect_error:
                print(f"❌ Reconnect failed: {reconnect_error}")
                time.sleep(5)  # 重连失败后等待更长时间


# 启动主程序
if __name__ == "__main__":
    main()
