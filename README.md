# 简介
这是一个大模型和硬件结合的快速搭建原型，目的是构建一个可交互的人工智能
硬件:
  1. `ESP32-S3-DevKitC-1` 开发板（搭载 ESP32-S3-N16R8 芯片）
  2. `INMP441` 麦克风
  3. 扬声器
  4. 0.91寸 OLED显示屏

硬件开发: micropython 固件

大模型: 
  - 文本、TTS、ASR都为第三方服务

软件服务
  - python 开发接收和处理 MQTT 消息

# 快速开始

- 准备固件
  下载链接: https://micropython.org/download/ESP32_GENERIC_S3/
- 刷写固件

```bash
uv pip install esptool

# windows 换成实际接口
# 清除开发板旧数据
esptool --chip esp32s3 --port COM4 erase_flash
# 把新的 MicroPython 固件烧录到开发板里
esptool --chip esp32s3 --port COM4 --baud 921600 write_flash -z 0x0000 firmware/ESP32_GENERIC_S3-20250911-v1.26.1.bin

# Linux 则端口不一样
```

- 安装插件(VSCode 配置环境)

1. RT-Thread MicroPython

- 测试

```python
# 终端执行
import machine
led = machine.Pin(2, machine.Pin.OUT)
led.value(1)  # 点亮 LED
print("Hello from MicroPython on ESP32-S3!")
```

# 架构

```shell
# 快速原型版
录音 (ESP32)
   ↓ (MQTT)
接收音频 (Python服务)
   ↓
唤醒词检测 (本地)
   ↓
ASR云服务 (转为文本)
   ↓ (MQTT)
显示文本 (ESP32 OLED)
   ↓
LLM云服务 (生成回复)
   ↓
TTS云服务 (转为语音)
   ↓ (MQTT)
播放语音 + 显示文本 (ESP32)
```