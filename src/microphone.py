from machine import I2S, Pin  # type: ignore

# 录音参数
SAMPLE_RATE = 44100
SAMPLE_SIZE = 16
BUFFER_SIZE = 8000
RECORD_DURATION = 3  # 录音时长（秒）


# 配置 I2S 接口用于接收 PDM 数据
def record_audio():

    i2s = I2S(
        0,
        sck=Pin(5),  # CLK
        ws=Pin(4),  # WS
        sd=Pin(6),  # DATA
        mode=I2S.RX,
        bits=SAMPLE_SIZE,
        format=I2S.MONO,
        rate=SAMPLE_RATE,
        ibuf=BUFFER_SIZE,
    )
    record = b""
    num_samples = SAMPLE_RATE * RECORD_DURATION
    bytes_per_sample = SAMPLE_SIZE // 8
    total_bytes = num_samples * bytes_per_sample

    # 读取音频数据并打印前几帧
    try:
        buf = bytearray(1024)
        print("开始录音...")
        while len(record) < total_bytes:
            num_bytes = i2s.readinto(buf)
            if num_bytes > 0:
                record += buf[:num_bytes]
        print("录音完成，共 {} 字节".format(len(record)))
        return record
    finally:
        i2s.deinit()
