# img_to_.py
from PIL import Image


def png_to_framebuf_mono_hlsb(
    png_path, width=24, height=24, threshold=128, invert=False, debug=False
):
    # 打开图像并统一处理为 RGBA 模式
    img = Image.open(png_path).convert("RGBA")

    # 创建白色背景图来替代透明区域
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(background, img)

    # 调整图像大小为目标尺寸
    img = img.resize((width, height))

    # 转换为灰度图
    img = img.convert("L")

    buf = bytearray()

    # 遍历每一行
    for y in range(img.height):
        row_byte = 0
        for x in range(img.width):
            gray = img.getpixel((x, y))
            # invert 控制前景/背景
            pixel = 0 if gray < threshold else 1
            if invert:
                pixel = 1 - pixel  # 反转颜色
            row_byte = (row_byte << 1) | pixel
            if (x + 1) % 8 == 0:
                buf.append(row_byte)
                row_byte = 0
        # 处理不足8位的尾部
        if img.width % 8 != 0:
            # 左移补齐到字节边界
            row_byte <<= 8 - (img.width % 8)
            buf.append(row_byte)

    result_bytes = bytes(buf)

    if debug:
        print("Visual representation:")
        bytes_per_row = (width + 7) // 8
        for y in range(height):
            byte_start = y * bytes_per_row
            row_bytes = result_bytes[byte_start : byte_start + bytes_per_row]
            bits = []
            for b in row_bytes:
                for i in range(7, -1, -1):
                    bits.append((b >> i) & 1)
            bits = bits[:width]
            print("".join("█" if bit else " " for bit in bits))

    return result_bytes


def format_as_byte_string(data):
    """将 bytes 转换为 Python 字节字符串格式"""
    return "b'" + "".join(f"\\x{b:02x}" for b in data) + "'"


# 使用方式
if __name__ == "__main__":
    # 示例：输出 18x18 图像
    data = png_to_framebuf_mono_hlsb(
        "icons8-wifi-24.png",
        width=12,
        height=12,
        threshold=100,
        invert=True,
        debug=True,
    )
    formatted = format_as_byte_string(data)
    print("\nFormatted byte string:")
    print(formatted)
