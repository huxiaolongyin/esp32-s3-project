import time

from machine import Pin  # type: ignore


def button_click(pin: Pin) -> bool:
    if pin.value() == 0:  # 按钮按下
        # 防抖处理
        time.sleep(0.05)
        if pin.value() == 0:  # 确认按钮确实按下
            print("Button clicked!")
            return True
    return False
