import time

import machine  # type: ignore

# I2S 配置
SAMPLE_RATE = 24000
BUF_LEN = 4096

i2s = machine.I2S(
    0,
    sck=machine.Pin(25),  # BCK
    ws=machine.Pin(26),  # LRCK (Word Select)
    sd=machine.Pin(27),  # DIN (Serial Data)
    mode=machine.I2S.TX,
    bits=16,
    format=machine.I2S.MONO,
    rate=SAMPLE_RATE,
    ibuf=BUF_LEN,
)


def play_audio(wav_bytes: bytes):
    try:
        # 跳过 WAV 头部（通常前44字节）
        audio_data = wav_bytes[44:]

        # 分块写入 I2S 缓冲区
        chunk_size = 2048
        offset = 0
        while offset < len(audio_data):
            chunk = audio_data[offset : offset + chunk_size]
            i2s.write(chunk)
            offset += chunk_size
    except Exception as e:
        print(f"[Speaker] 播放失败: {e}")
    finally:
        time.sleep(0.5)  # 等待播放完成
