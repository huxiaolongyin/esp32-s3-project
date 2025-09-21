import time

from machine import I2C, Pin  # type: ignore

import mqtt
import wifi
from config import Config
from display import Display
from microphone import record_audio
from speaker import play_audio
from utils import button_click

button40 = Pin(Config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)  # GPIO40 接按钮，按下时接地

# 屏幕显示
i2c = I2C(scl=Pin(Config.I2C_SCL_PIN), sda=Pin(Config.I2C_SDA_PIN))
display = Display(i2c)


# 回调函数：收到服务器回复时触发
def on_message(topic, payload):
    if topic == Config.MQTT_TOPIC_RESPONSE[0]:
        print(f"ASR识别: {payload.decode()}")
    elif topic == Config.MQTT_TOPIC_RESPONSE[1]:
        print(f"LLM回复: {payload.decode()}")
    elif topic == Config.MQTT_TOPIC_RESPONSE[2]:
        print(f"TTS音频长度: {len(payload)} 字节")
        play_audio(payload)


# 主程序
def main():
    # 连接 WIFI
    wifi.connect(Config.SSID, Config.WIFI_PWD, display)
    client = mqtt.connect()

    # 设置消息回调（接收 AI 回复）
    client.set_callback(on_message)
    for topic in Config.MQTT_TOPIC_RESPONSE:
        client.subscribe(topic)

    print(f"🔔 Subscribed to the reply topic")

    # 添加重连状态标记
    # mqtt_connected = True

    while True:
        try:
            # 检查按钮是否按下
            if button_click(button40):
                display.microphone("listening")
                audio_data = record_audio()
                client.publish(Config.MQTT_TOPIC_REQUEST, audio_data)
                print(f"📤 A request has been sent")

                # 等待按钮释放
                while button40.value() == 0:
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
                client.subscribe(Config.MQTT_TOPIC_RESPONSE)
                print(f"🔔 Subscribed to the reply topic")
            except Exception as reconnect_error:
                print(f"❌ Reconnect failed: {reconnect_error}")
                time.sleep(5)  # 重连失败后等待更长时间


# 启动主程序
if __name__ == "__main__":
    main()
