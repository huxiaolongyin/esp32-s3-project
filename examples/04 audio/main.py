from machine import I2S, Pin  # type: ignore
import math
import time

# 配置 I2S 接口
i2s = I2S(
    0,  # I2S ID
    sck=Pin(15),  # 位时钟 BCLK
    ws=Pin(16),  # 帧时钟 LRC/WS
    sd=Pin(7),  # 数据输入 DIN
    mode=I2S.TX,  # 发送模式
    bits=16,  # 位深度
    format=I2S.MONO,  # 单声道
    rate=22050,  # 采样率
    ibuf=4000,  # 内部缓冲区大小
)


# 生成一小段正弦波 PCM 数据（每次只生成一小块）
def generate_sine_chunk(freq=440, chunk_size=1024, sample_rate=22050, amplitude=1000):
    wave = bytearray()
    for i in range(chunk_size):
        value = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
        wave.append(value & 0xFF)
        wave.append((value >> 8) & 0xFF)
    return bytes(wave)


# 播放音频（流式）
try:
    total_samples = 22050 * 2  # 2秒
    chunk_size = 1024
    for _ in range(0, total_samples, chunk_size):
        chunk = generate_sine_chunk(freq=523, chunk_size=chunk_size)
        i2s.write(chunk)
finally:
    i2s.deinit()
