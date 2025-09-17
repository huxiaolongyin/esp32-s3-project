import time
from machine import I2S, Pin


# I2S 配置
SAMPLE_RATE = 24000
BUF_LEN = 4000

def play_audio(wav_bytes: bytes):

    i2s = None

    # 每次播放都重新初始化 I2S
    try:
        # 根据 WAV 文件信息初始化 I2S
        i2s = I2S(
            0,
            sck=Pin(15),
            ws=Pin(16),
            sd=Pin(7),
            mode=I2S.TX,
            bits=16,
            format=I2S.MONO,
            rate=SAMPLE_RATE,
            ibuf=BUF_LEN,
        )

        # 跳过 WAV 头部
        audio_data = wav_bytes[44:]

        # 分块播放
        chunk_size = 2048
        offset = 0
        while offset < len(audio_data):
            chunk = audio_data[offset : offset + chunk_size]
            i2s.write(chunk)
            offset += chunk_size

        print("[Speaker] 播放完成")

    except Exception as e:
        print(f"[Speaker] 播放失败: {e}")
    finally:
        if i2s:
            i2s.deinit()
        time.sleep(0.02)