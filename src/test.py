text_buffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x01\xe6\x1f\x88\x00\x02\x18\xc8\x7f\x02\x0cl\xa0\x1f\x06,2\x12\x02\x0e\x02\x13\x02\xce\x12\xe9?M\x12\t\x02L"\x0e\x02,"\x0c\x02,b\x12\x02\x0c\x02\x03\x02\xcc\x03\xc1\x03'

windows_width = 108
windows_height = 20
windows_bytes_per_row = windows_width // 8  # 108 // 8 = 13
expected_size = windows_bytes_per_row * windows_height  # 13 * 20 = 260

print(f"原始文本长度: {len(text_buffer)} 字节")
print(f"每行字节数: {windows_bytes_per_row} (对应 {windows_bytes_per_row * 8} 像素)")
print(f"期望总字节数: {expected_size}")
print("-" * 60)

bytes_per_row = len(text_buffer) // windows_height
# ✅ 按行分割 + 补零
rows = []
for i in range(windows_height):

    start = i * bytes_per_row
    end = start + bytes_per_row
    row = text_buffer[start:end]
    if len(row) < windows_bytes_per_row:
        row += bytearray(windows_bytes_per_row - len(row))  # 补 \x00
    rows.append(row)

# ✅ 拼接成最终 buffer
text_buffer_final = bytearray(b"".join(rows))
print(f"最终 buffer 长度: {len(text_buffer_final)} 字节 ✅")


def binary_display(data: bytearray, width: int = 104, height: int = 20):
    """
    可视化显示 bytearray 为二进制点阵图（MONO_HLSB 模式）
    每个字节代表8个像素，从左到右，LSB在左（第0位是左边第一个像素）

    Args:
        data: 输入的字节缓冲区（总长度应为 (width // 8) * height）
        width: 显示宽度（像素），默认 104（对应13字节）
        height: 显示高度（行数），默认 20
    """
    bytes_per_row = width // 8  # 每行所需字节数（向下取整）
    total_expected = bytes_per_row * height

    print(f"\n🔍 二进制点阵图（{width}×{height} 像素，{bytes_per_row} 字节/行）")
    print("  " + "─" * (width + 10))  # 分隔线

    for i in range(height):
        start = i * bytes_per_row
        row = data[start : start + bytes_per_row]

        # 构建该行的像素字符串：每个字节转8位，LSB在左（HLSB）
        pixel_line = ""
        for byte in row:
            # 从第0位（LSB）到第7位（MSB）→ 左到右
            bits = "".join("■" if (byte >> bit) & 1 else "□" for bit in range(8))
            pixel_line += bits

        # 显示行号 + 像素图
        print(f"行{i:2d}: {pixel_line}")

    print("  " + "─" * (width + 10))
    print(
        f"✅ 总字节数: {len(data)} / {total_expected}（{len(data)//bytes_per_row} 行）"
    )


binary_display(text_buffer_final)
