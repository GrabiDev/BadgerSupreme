import badger2040
import qrcode
import time
import os
import badger_os

code = qrcode.QRCode()


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code, display):
    size, module_size = measure_qr_code(size, code)
    display.pen(15)
    display.rectangle(ox, oy, size, size)
    display.pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def draw_qr_file(codetext, display):
    code_text = codetext[0]
    title_text = codetext[1]
    detail_text = codetext[2].encode().decode("unicode-escape").split("\n")

    # Clear the Display
    display.pen(15)  # Change this to 0 if a white background is used
    display.clear()
    display.pen(0)

    code.set_text(code_text)
    size, _ = measure_qr_code(128, code)
    left = top = int((badger2040.HEIGHT / 2) - (size / 2))
    draw_qr_code(left, top, 128, code, display)

    left = 128 + 5

    display.thickness(2)
    display.text(title_text, left, 20, 1)
    display.thickness(1)

    top = 70
    for line in detail_text:
        display.text(line, left, top, 0.6)
        top += 20
