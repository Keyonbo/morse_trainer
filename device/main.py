from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from time import ticks_ms, ticks_diff, sleep_ms

# ==================================
# MORSE TRAINER v1.3
# ==================================

# ===== HARDWARE =====

# Main Morse button
button = Pin(14, Pin.IN, Pin.PULL_UP)

# Reset button
reset_button = Pin(16, Pin.IN, Pin.PULL_UP)

# LED indicator
led = Pin(17, Pin.OUT)
led.value(0)

# Buzzer
buzzer = PWM(Pin(15), freq=2000)
buzzer.duty_u16(0)

# OLED Display
i2c = I2C(
    0,
    sda=Pin(0),
    scl=Pin(1),
    freq=100000,
    timeout=500000
)

oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# ===== MORSE ALPHABET =====

MORSE = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",

    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9"
}

# ===== TIMING =====

DOT_THRESHOLD = 200
LETTER_GAP = 700
WORD_GAP = 1700

# ===== STATE =====

sequence = ""
message = ""

pressed_before = False
reset_was_pressed = False

press_start = 0
last_release = None

# ===== DISPLAY =====

def update_display():
    oled.fill(0)

    oled.text("MORSE TRAINER", 0, 0)
    oled.text("CODE: " + sequence[:10], 0, 16)
    oled.text("MESSAGE:", 0, 30)

    visible = message[-32:]

    oled.text(visible[:16], 0, 42)
    oled.text(visible[16:], 0, 54)

    oled.show()


# ===== RESET FUNCTION =====

def reset_message():
    global sequence
    global message
    global pressed_before
    global press_start
    global last_release

    sequence = ""
    message = ""

    pressed_before = False
    press_start = 0
    last_release = None

    # Stop audio
    buzzer.duty_u16(0)

    # Turn off LED
    led.value(0)

    update_display()

    print("MESSAGE CLEARED")


# ===== INITIALIZATION =====

update_display()

print("MORSE TRAINER v1.3")
print("SYSTEM READY")

# ===== MAIN LOOP =====

while True:

    now = ticks_ms()

    pressed = button.value() == 0
    reset_pressed = reset_button.value() == 0

    # ===== RESET BUTTON =====

    if reset_pressed:

        if not reset_was_pressed:
            reset_message()

        reset_was_pressed = True

        buzzer.duty_u16(0)
        led.value(0)

        sleep_ms(10)
        continue

    reset_was_pressed = False

    # ===== LED INDICATOR =====

    # LED follows Morse button state
    if pressed:
        led.value(1)
    else:
        led.value(0)

    # ===== MORSE BUTTON PRESSED =====

    if pressed and not pressed_before:

        # Detect word gap
        if (
            last_release is not None
            and not sequence
            and message
            and not message.endswith(" ")
            and ticks_diff(now, last_release) >= WORD_GAP
        ):
            message += " "
            update_display()

        press_start = now

        # Start sound
        buzzer.duty_u16(32768)

    # ===== MORSE BUTTON RELEASED =====

    elif not pressed and pressed_before:

        # Stop sound
        buzzer.duty_u16(0)

        duration = ticks_diff(now, press_start)

        if duration >= 25:

            if duration < DOT_THRESHOLD:
                sequence += "."
            else:
                sequence += "-"

            last_release = now

            update_display()

    # ===== LETTER DECODING =====

    if (
        not pressed
        and sequence
        and last_release is not None
        and ticks_diff(now, last_release) >= LETTER_GAP
    ):

        letter = MORSE.get(sequence, "?")

        message += letter

        print(sequence, "->", letter)
        print("MESSAGE:", message)

        sequence = ""

        update_display()

    pressed_before = pressed

    sleep_ms(5)
