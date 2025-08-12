from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.rgb import RGB
from kmk.handlers.sequences import send_string

import usb_cdc

keyboard = KMKKeyboard()

# Basic 3x4 matrix for ANAVI Macro Pad 12 (3 rows x 4 columns)
keyboard.col_pins = (1, 2, 3, 4)
keyboard.row_pins = (5, 6, 7)

keyboard.diode_orientation = keyboard.DIODE_COL2ROW

# RGB underglow - WS2812B LEDs
rgb = RGB(pixel_pin=8, num_pixels=12, hue_default=0)
keyboard.modules.append(rgb)

# Keymap placeholder — just use one dummy key for now
keyboard.keymap = [
    [KC.NO] * 12  # 12 keys; we only use key 0
]

# Initial LED state: green
rgb.set_pixel(0, (0, 255, 0))

# Serial status tracker
email_alert = False

# Listen to serial input over USB
def check_serial():
    global email_alert
    if usb_cdc.data.in_waiting:
        msg = usb_cdc.data.read(usb_cdc.data.in_waiting).decode().strip()
        if msg == "EMAIL":
            email_alert = True
            rgb.set_pixel(0, (255, 0, 0))  # Red
        elif msg == "NOEMAIL":
            email_alert = False
            rgb.set_pixel(0, (0, 255, 0))  # Green

# Attach background hook to check serial every cycle
def before_matrix_scan():
    check_serial()

keyboard.before_matrix_scan = before_matrix_scan

# Spotlight + Mail launcher using KMK's send_string
def launch_mail():
    # CMD + SPACE to open Spotlight
    keyboard.press(KC.LGUI, KC.SPACE)
    keyboard.release(KC.LGUI, KC.SPACE)

    # Small delay (Spotlight can be a little sleepy)
    import supervisor
    supervisor.ticks_ms()
    supervisor.sleep(0.4)

    # Type 'Mail' and press Enter
    send_string("Mail\n")(keyboard)

# Handle key press: index 0 = top-left key
def custom_key_handler(key, is_pressed):
    if key == 0 and is_pressed:
        launch_mail()
        return False  # Skip default KC.NO
    return True

keyboard.key_down_handler = custom_key_handler

# Go time
keyboard.go()
