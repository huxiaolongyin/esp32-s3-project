import os
import time
import wave

import paho.mqtt.client as mqtt
from asr_client import transcribe_asr
from llm_client import get_response
from PIL import Image, ImageDraw, ImageFont
from tts_client import transcribe_tts

MQTT_BROKER = "112.124.69.152"
MQTT_PORT = 1883

# WAKE_WORD = "你好"

PUNCTUATIONS = ["，", "。", "！", "？", "；"]

# 音频参数（需与 ESP32 端一致）
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
CHANNELS = 1  # MONO

# 设置字体（请确保字体文件存在）
FONT_PATH = "./font/msyh.ttf"  # 可替换为支持中文的字体
FONT_SIZE = 15
IMAGE_WIDTH = 108
IMAGE_HEIGHT = 20


# 保存音频的函数
def save_audio_as_wav(audio_data, filename):
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)
    print(f"音频已保存为: {filename}")


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


def text_to_framebuffer(text):
    # 1. 使用字体计算文本实际渲染宽度（像素）
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    # 使用 getbbox() 获取精确边界（推荐用于单行）
    bbox = font.getbbox(text)
    if bbox is None:
        width = 0
    else:
        width = bbox[2] - bbox[0]  # 右 - 左 = 实际宽度
        height = bbox[3] - bbox[1]  # 高度（用于校验）

    # 如果文本为空或宽度为0，返回空缓冲区
    if width == 0:
        return b""

    # 2. 创建图像：宽度自适应，高度固定为20
    # 为了防止字体底部裁剪，留一点上下边距
    image = Image.new("1", (width, IMAGE_HEIGHT), 0)
    draw = ImageDraw.Draw(image)
    # 居中垂直对齐（因为字体可能不是正好20高）
    y_offset = (IMAGE_HEIGHT - height) // 2
    draw.text((0, y_offset), text, font=font, fill=1)

    # 3. 转换为原始像素字节（PIL 默认是 MSB first，每行从左到右）
    raw_bytes = image.tobytes()

    # 4. ✅ 关键：将每个字节的位顺序从 MSB first → LSB first（MONO_HLSB 要求）
    # MONO_HLSB: 每个字节中，第0位是左边第一个像素，第7位是右边第8个像素
    # PIL 输出是 MSB first: 第0位是右边第8个像素
    # 所以需要位反转
    def reverse_bits(byte):
        return int("{:08b}".format(byte)[::-1], 2)

    # 对每个字节进行位反转
    hlsb_bytes = bytes(reverse_bits(b) for b in raw_bytes)

    return hlsb_bytes


def on_message(client, userdata, msg):
    if msg.topic == "ai/esp32-001/request":
        audio_data = msg.payload

        # 生成文件名（按时间命名）
        filename = f"recorded_audio_{int(time.time())}.wav"

        # 保存音频数据为 WAV 文件
        save_audio_as_wav(audio_data, filename)

        absolute_path = os.path.abspath(filename)
        print(f"Received audio data：{absolute_path}")

        # audio_data = (
        #     r"C:\Users\Administrator\code\esp32-s3-project\src\server\welcome.mp3"
        # )

        # # 唤醒词检测（简化版）
        # if not wake_word_detected(audio_data):
        #     return

        # ASR
        text = transcribe_asr(absolute_path)
        print("ASR result:", text)

        client.publish("ai/esp32-001/asr", text)
        print("send to mqtt:", text)

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
                    client.publish("ai/esp32-001/llm", text_to_framebuffer(reply))
                    client.publish("ai/esp32-001/tts", tts_audio)

        # 处理剩余文本
        if segment:
            tts_audio = transcribe_tts(segment)
            client.publish("ai/esp32-001/llm", segment)
            client.publish("ai/esp32-001/tts", tts_audio)

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
    print(repr(text_to_framebuffer("你好")))
    # print()
