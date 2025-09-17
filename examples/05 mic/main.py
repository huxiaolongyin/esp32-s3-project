from machine import I2S, Pin  # type: ignore
import time

# 配置 I2S 接口用于接收 PDM 数据
i2s = I2S(
    0,
    sck=Pin(5),  # CLK 引脚
    ws=Pin(4),  # WS 引脚（有时也叫 L/R）
    sd=Pin(6),  # DATA 引脚（需连接到 SD 引脚）
    mode=I2S.RX,  # 接收模式
    bits=16,  # 位深度（PDM 会被转换为 PCM）
    format=I2S.MONO,
    rate=44100,  # 采样率
    ibuf=8000,  # 内部缓冲区大小
)

# 读取音频数据并打印前几帧
try:
    buf = bytearray(1024)
    print("开始读取麦克风数据...")
    for _ in range(10):  # 读取10次
        num_bytes = i2s.readinto(buf)
        print(f"读取到 {num_bytes} 字节数据: {buf[:32]}")  # 打印前32字节
        time.sleep(0.5)
finally:
    i2s.deinit()
