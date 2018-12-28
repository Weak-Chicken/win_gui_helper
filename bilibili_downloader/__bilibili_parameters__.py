from PIL import Image


# ====================================================load pictures=====================================================
im_mouse_hover = Image.open("pics/mouse_hover.png")

# ====================================================layout related====================================================
SCREEN_RESOLUTION = (1920, 1080)
EPISODE_PER_LINE = 3
BOTTOM_LINE_EPISODE_UPPER_BOUNDARY = 855
BOTTOM_LINE_EPISODE_LOWER_BOUNDARY = 1015
MAX_LINES_DISPLAYED_NOT_EFFECTED = 4


# Auto calculated. No need for modifying
BOTTOM_LINE_EPISODE_CENTER = (BOTTOM_LINE_EPISODE_LOWER_BOUNDARY - BOTTOM_LINE_EPISODE_UPPER_BOUNDARY) / 2 \
                             + BOTTOM_LINE_EPISODE_UPPER_BOUNDARY

SINGLE_EPISODE_SIZE = im_mouse_hover.size


if __name__ == "__main__":
    print("=========================================__bilibili_parameters__=========================================")
    print("EPISODE_PER_LINE:", EPISODE_PER_LINE)
    print("BOTTOM_LINE_EPISODE_UPPER_BOUNDARY:", BOTTOM_LINE_EPISODE_UPPER_BOUNDARY)
    print("BOTTOM_LINE_EPISODE_LOWER_BOUNDARY:", BOTTOM_LINE_EPISODE_LOWER_BOUNDARY)
    print("BOTTOM_LINE_EPISODE_CENTER:", BOTTOM_LINE_EPISODE_CENTER)
    print("SINGLE_EPISODE_SIZE:", SINGLE_EPISODE_SIZE)
