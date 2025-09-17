import base64
import json

import paho.mqtt.client as mqtt
from asr_client import transcribe_asr
from llm_client import get_response
from tts_client import transcribe_tts

MQTT_BROKER = "112.124.69.152"
MQTT_PORT = 1883

# WAKE_WORD = "你好"

PUNCTUATIONS = ["，", "。", "！", "？", "；"]


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("ai/esp32-001/request")


def split_text_by_punctuation(text: str):
    """按标点符号切分文本"""
    segments = []
    segment = ""
    for char in text:
        segment += char
        if char in PUNCTUATIONS:
            segments.append(segment)
            segment = ""
    if segment:
        segments.append(segment)
    return segments


def on_message(client, userdata, msg):
    if msg.topic == "ai/esp32-001/request":
        audio_data = msg.payload
        print("Received audio data")

        audio_data = (
            r"C:\Users\Administrator\code\esp32-s3-project\src\server\welcome.mp3"
        )

        # # 唤醒词检测（简化版）
        # if not wake_word_detected(audio_data):
        #     return

        # ASR
        text = transcribe_asr(audio_data)
        print("ASR result:", text)

        client.publish("ai/esp32-001/reponse", json.dumps({"asr": text}))
        print("send to mqtt:", {"asr": text})

        # LLM
        segment = ""
        response = get_response(text)
        for res in response:
            segment += str(res)
            for punc in PUNCTUATIONS:
                if punc in segment:
                    reply, segment = segment.split(punc, 1)
                    tts_audio = transcribe_tts(reply)
                    reply += punc
                    client.publish(
                        "ai/esp32-001/reponse",
                        json.dumps({"llm": reply, "tts": tts_audio}),
                    )
        # 处理剩余文本
        if segment:
            tts_audio = transcribe_tts(segment)
            client.publish(
                "ai/esp32-001/reponse", json.dumps({"llm": segment, "tts": tts_audio})
            )

        # TTS
        # text = "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。"
        # text_list = text.split("，")
        # for t in text_list:
        #     tts_audio = transcribe_tts(t)
        #     client.publish("ai/audio/out", tts_audio)


def wake_word_detected(audio_data):
    # 简化处理：假设本地已有唤醒词检测逻辑
    return True  # 模拟唤醒成功


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
