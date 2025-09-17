import base64
import os
import time

import numpy as np
import pyaudio
from dashscope import audio


def transcribe_tts(text: str) -> bytes:
    audio_bytes = b""
    responses = audio.qwen_tts.SpeechSynthesizer.call(
        # 仅支持qwen-tts系列模型，请勿使用除此之外的其他模型
        model="qwen-tts-latest",
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY", "sk-09986c3ceb3842569f0b22cb158f34f2"),
        text=text,
        voice="Cherry",
        stream=True,
    )
    for chunk in responses:
        audio_string = chunk["output"]["audio"]["data"]
        wav_bytes = base64.b64decode(audio_string)
        audio_bytes += wav_bytes
    return audio_bytes


def play_audio_stream(wav_bytes: bytes, p: pyaudio.PyAudio | None = None, stream=None):
    if not wav_bytes:
        print("音频数据为空，跳过播放")
        return

    try:
        audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
        if stream:
            stream.write(audio_np.tobytes())
        time.sleep(0.5)
    except Exception as e:
        print(f"播放音频失败: {e}")


def play_text_list(text_list):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    try:
        for text in text_list:
            print(f"正在合成并播放: {text}")
            wav_bytes = transcribe_tts(text)
            play_audio_stream(wav_bytes, p, stream)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":

    text = "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。"
    text_list = text.split("，")
    play_text_list(text_list)
