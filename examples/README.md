# 简介

这是一个使用 Python 控制硬件的入门教学项目，基于 `ESP32-S3-DevKitC-1` 开发板（搭载 ESP32-S3-N16R8 芯片），通过 MicroPython 实现对 GPIO、传感器、LED、串口等外设的编程控制。
最终刷入AI固件，实现硬件与大模型的交互

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

1. Serial Monitor
2. RT-Thread MicroPython

- 连接串口

```python
按 `Ctrl+Shift+P` → 输入 `Serial Monitor: Open` → 选择你的端口（如 `COM5`）。
波特率设置为 **115200**，回车后应看到 MicroPython 提示符 `>>>`。
```

- 测试

```python
# 终端执行
import machine
led = machine.Pin(2, machine.Pin.OUT)
led.value(1)  # 点亮 LED
print("Hello from MicroPython on ESP32-S3!")
```
