import time

import framebuf  # type: ignore
from machine import I2C, Pin  # type: ignore

import msyh
import ssd1306
from writer import Writer

ICON_BYTES = {
    "SMILE_20": b"\x00\x00\x00\x00\x00\x00\x01\xf8\x00\x07\x0e\x00\x0c\x03\x00\x18\x01\x80\x10\x00\x80\x33\x0c\xc0\x23\x0c\x40\x20\x00\x40\x20\x00\x40\x20\x00\x40\x33\xfc\xc0\x11\xf8\x80\x18\x01\x80\x0c\x03\x00\x07\x0e\x00\x01\xf8\x00\x00\x00\x00\x00\x00\x00",
    "SAD_20": b"\x00\x00\x00\x00\x00\x00\x01\xf8\x00\x07\x0e\x00\x0c\x03\x00\x18\x01\x80\x10\x00\x80\x30\x00\xc0\x20\x00\x40\x21\x08\x40\x20\x00\x40\x20\x00\x40\x31\xf8\xc0\x11\x98\x80\x18\x01\x80\x0c\x03\x00\x07\x0e\x00\x01\xf8\x00\x00\x00\x00\x00\x00\x00",
    "WIFI_ONE_12": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00",
    "WIFI_TWO_12": b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x19\x80\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00",
    "WIFI_12": b"\x00\x00\x00\x00\x00\x00\x1f\x80\x60\x60\x0f\x00\x19\x80\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00",
    "WIFI_ERROR_12": b"\x00\x00\x06\x00\x06\x00\x3f\xc0\xe6\x70\x46\x20\x19\x80\x10\x80\x00\x00\x06\x00\x00\x00\x00\x00",
}


class Display:
    def __init__(self, i2c, width=128, height=32):
        self.oled = ssd1306.SSD1306_I2C(width, height, i2c)
        self.oled.fill(0)
        self.writer = Writer(self.oled, msyh)

    def wifi(self, status="connected"):
        # Display WiFi icon on the OLED
        self.oled.fill_rect(0, 0, 12, 12, 0)  # 清除区域

        if status == "connecting":
            # 动态显示连接过程
            for icon in ["WIFI_ONE_12", "WIFI_TWO_12", "WIFI_12"]:
                buffer = bytearray(ICON_BYTES[icon])
                fb = framebuf.FrameBuffer(buffer, 12, 12, framebuf.MONO_HLSB)
                self.oled.fill_rect(0, 0, 12, 12, 0)
                self.oled.blit(fb, 0, 0)
                self.oled.show()
                time.sleep(0.5)  # 每个图标显示 0.5 秒
        elif status == "error":
            buffer = bytearray(ICON_BYTES["WIFI_ERROR_12"])
            fb = framebuf.FrameBuffer(buffer, 12, 12, framebuf.MONO_HLSB)
            self.oled.blit(fb, 0, 0)
            self.oled.show()
        else:
            buffer = bytearray(ICON_BYTES["WIFI_12"])
            fb = framebuf.FrameBuffer(buffer, 12, 12, framebuf.MONO_HLSB)
            self.oled.blit(fb, 0, 0)
            self.oled.show()

    def microphone(self, status="listening"):
        # Display microphone icon on the OLED
        start_x = 40
        listening_text = "聆听中..."
        playing_text = "播放中..."
        content = listening_text if status == "listening" else playing_text
        self.writer.set_textpos(self.oled, 0, start_x)
        self.writer.printstring(content)
        self.oled.show()

    def emoji(self):
        # Display emoji icon on the OLED
        self.oled.fill_rect(0, 12, 20, 20, 0)
        smile_face = bytearray(ICON_BYTES["SMILE_20"])
        fb = framebuf.FrameBuffer(smile_face, 20, 20, framebuf.MONO_HLSB)
        self.oled.blit(fb, 0, 12)
        self.oled.show()

    def scoll_text(self, text_buffer=None, delay=0.2):
        """
        传入字符串的字节形式，进行从右向左滚动显示
        Args:
            text_buffer: 字符串的字节形式（bytes/bytearray）
            delay: 每次滚动的延时，单位秒
        """
        windows_width = 108
        windows_height = 20
        windows_bytes_per_row = (windows_width) // 8  # 窗口可显示大小: 13 字节/行
        expected_size = windows_bytes_per_row * windows_height  # 260

        # 如果文本小于窗口，每行末尾补上\x00
        if len(text_buffer) <= expected_size:
            bytes_per_row = len(text_buffer) // windows_height
            rows = []
            for i in range(windows_height):

                start = i * bytes_per_row
                end = start + bytes_per_row
                row = text_buffer[start:end]
                if len(row) < windows_bytes_per_row:
                    row += bytearray(windows_bytes_per_row - len(row))  # 补 \x00
                rows.append(row)
            text_buffer = bytearray(b"".join(rows))
            fb = framebuf.FrameBuffer(
                text_buffer,
                windows_bytes_per_row * 8,
                windows_height,
                framebuf.MONO_HLSB,
            )
            self.oled.fill_rect(20, 12, windows_width, windows_height, 0)
            self.oled.blit(fb, 20, 12)
            self.oled.show()
            return


def split_into_rows(text_buffer: bytearray, height=20) -> list:
    """
    将一维 bytearray 按行拆分为 20 行的二维列表
    Args:
        text_buffer: bytearray，总长度应为 280 字节
        height: 行数，默认 20
    Returns:
        List[bytearray]：20 个元素，每个是代表一行的 bytearray
    """
    if len(text_buffer) % height != 0:
        raise ValueError(f"Buffer length {len(text_buffer)} not divisible by {height}")
    bytes_per_row = len(text_buffer) // height
    rows = []
    for i in range(height):
        start = i * bytes_per_row
        end = start + bytes_per_row
        row = text_buffer[start:end]
        rows.append(row)
    return rows


if __name__ == "__main__":
    i2c_dev = I2C(1, scl=Pin(42), sda=Pin(41), freq=200000)
    display = Display(i2c_dev)
    # display.wifi(status="error")
    text_buffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x01\xe6\x1f\x88\x00\x02\x18\xc8\x7f\x02\x0cl\xa0\x1f\x06,2\x12\x02\x0e\x02\x13\x02\xce\x12\xe9?M\x12\t\x02L"\x0e\x02,"\x0c\x02,b\x12\x02\x0c\x02\x03\x02\xcc\x03\xc1\x03'
    display.scoll_text(text_buffer)
    # display.microphone()
    # time.sleep(2)
    # display.microphone(status="playing")
    # time.sleep(2)
    # display.emoji()
    # time.sleep(1)
    # display.scoll_text()
