import time
import json
import badger2040
import badger_os
from qr_util import draw_qr_file

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 23
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.6

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_BADGE = {
    "company": "mustelid inc",
    "name": "H. Badger",
    "detail1_title": "RP2040",
    "detail1_text": "2MB Flash",
    "detail2_title": "E ink",
    "detail2_text": "296x128px",
    "image": "badge-image.bin",
}


# ------------------------------
#      Utility functions
# ------------------------------

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

def draw_badge(badge):
    display.pen(0)
    display.clear()

    # Load badge image
    BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
    
    try:
        open(badge.get("image"), "rb").readinto(BADGE_IMAGE)
    except OSError:
        try:
            import badge_image
            BADGE_IMAGE = bytearray(badge_image.data())
            del badge_image
        except ImportError:
            pass
    # Draw badge image
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Uncomment this if a white background is wanted behind the company
    # display.pen(15)
    # display.rectangle(1, 1, TEXT_WIDTH, COMPANY_HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("serif")
    display.thickness(3)
    display.text(badge.get("company"), LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(4)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(badge.get("name"), name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(badge.get("name"), (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 4, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(3)
    name_length = display.measure_text(badge.get("detail1_title"), DETAILS_TEXT_SIZE)
    display.text(badge.get("detail1_title"), LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    
    required_space_width = DETAIL_SPACING if badge.get("detail1_title") else 0 # do not add space if no detail title
    display.text(badge.get("detail1_text"), LEFT_PADDING + name_length + required_space_width, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(3)
    name_length = display.measure_text(badge.get("detail2_title"), DETAILS_TEXT_SIZE)
    display.text(badge.get("detail2_title"), LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    
    required_space_width = DETAIL_SPACING if badge.get("detail2_title") else 0 # do not add space if no detail title
    display.text(badge.get("detail2_text"), LEFT_PADDING + name_length + required_space_width, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)


def load_badge_contents(badge):
    company = badge.get("company")       # "mustelid inc"
    name = badge.get("name")           # "H. Badger"
    detail1_title = badge.get("detail1_title") # "RP2040"
    detail1_text = badge.get("detail1_text")  # "2MB Flash"
    detail2_title = badge.get("detail2_title") # "E ink"
    detail2_text = badge.get("detail2_text")  # "296x128px"
    
    # Truncate all of the text (except for the name as that is scaled)
    company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)

    detail1_title = truncatestring(detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail1_text = truncatestring(detail1_text, DETAILS_TEXT_SIZE,
                                  TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))

    detail2_title = truncatestring(detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail2_text = truncatestring(detail2_text, DETAILS_TEXT_SIZE,
                                  TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))


def display_contact_info(badge, index):
    contact_info_list = badge.get("contact")
    contact_info = contact_info_list[index]
    codetext = [contact_info.get("link"), contact_info.get("platform"), contact_info.get("handle")]
    draw_qr_file(codetext, display)

# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Open the badge file
try:
    badge_stream = open("badge.json", "r")
    badge_list = json.load(badge_stream)
except OSError:
    with open("badge.json", "w") as f:
        f.write(json.dumps([DEFAULT_BADGE]))
        f.flush()
    badge_stream = open("badge.json", "r")
    badge_list = json.load(badge_stream)

current_badge_index = 0
current_badge = badge_list[current_badge_index]
load_badge_contents(current_badge)

# ------------------------------
#       Main program
# ------------------------------

draw_badge(current_badge)
display.update()

while True:
    if display.pressed(badger2040.BUTTON_A):
        display_contact_info(current_badge, 0)
        display.update()
        time.sleep(4)

        draw_badge(current_badge)
        display.update()
        
    if display.pressed(badger2040.BUTTON_B):
        display_contact_info(current_badge, 1)
        display.update()
        time.sleep(4)

        draw_badge(current_badge)
        display.update()
        
    if display.pressed(badger2040.BUTTON_C):
        display_contact_info(current_badge, 2)
        display.update()

        draw_badge(current_badge)
        display.update()
    
    if display.pressed(badger2040.BUTTON_UP) and len(badge_list) > 1:
        # move to the previous badge
        if current_badge_index > 0:
            current_badge_index -= 1
        else:
            current_badge_index = len(badge_list) - 1
            
        current_badge = badge_list[current_badge_index]
        load_badge_contents(current_badge)
        draw_badge(current_badge)
        
        display.update()
        
    if display.pressed(badger2040.BUTTON_DOWN) and len(badge_list) > 1:
        # move to the next badge
        if current_badge_index < len(badge_list) - 1:
            current_badge_index += 1
        else:
            current_badge_index = 0
        
        current_badge = badge_list[current_badge_index]
        load_badge_contents(current_badge)
        draw_badge(current_badge)
        
        display.update()
