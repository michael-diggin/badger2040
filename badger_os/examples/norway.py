import badger2040
import json
import gc
import random


gc.collect()

# LETS START FROM SCRATCH

TOTAL_QUOTES = int(5)
text_file = "/translations/norway.txt"

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

TEXT_PADDING = 4
TEXT_WIDTH = WIDTH - TEXT_PADDING - TEXT_PADDING
TEXT_SIZE = 0.55

FONT = "sans"
FONT_THICKNESS = 2

text_spacing = int(34 * TEXT_SIZE)
# Create a new Badger and set it to update MEDIUM.
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_MEDIUM)
display.set_font(FONT)
display.set_thickness(FONT_THICKNESS)


def display_random_translation():
    display.set_pen(15)
    display.set_thickness(FONT_THICKNESS)
    display.clear()
    # Open the quotes file.
    translations = open(text_file, "r")

    n = random.randint(0, TOTAL_QUOTES)
    for _ in range(n):
        translations.readline()

    current_json = json.loads(translations.readline())
    # Read a full line and split it into words.
    norwegian_words = current_json["norwegian"].split(" ")
    english_words = current_json["english"].split(" ")

    lines = []
    latest_line = ""
    for word in norwegian_words:
        latest_line_length = display.measure_text(latest_line + word, TEXT_SIZE)
        if latest_line_length >= TEXT_WIDTH:
            lines.append(latest_line)
            latest_line = ""
        latest_line += word
        latest_line += " "

    lines.append(latest_line)
    lines.append("")
    latest_line = ""
    for word in english_words:
        latest_line_length = display.measure_text(latest_line + word, TEXT_SIZE)
        if latest_line_length >= TEXT_WIDTH:
            lines.append(latest_line)
            latest_line = ""
        latest_line += word
        latest_line += " "

    lines.append(latest_line)


    for i, line in enumerate(lines):
        y = int(i * text_spacing) + int(text_spacing // 2) + TEXT_PADDING
        display.set_pen(0)
        display.text(line, TEXT_PADDING, y, TEXT_WIDTH, TEXT_SIZE)
    display.update()


# Main program loop
changed = True
while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    if display.pressed(badger2040.BUTTON_A):
        changed = True

    if changed:
        display_random_translation()

        changed = False

    display.halt()