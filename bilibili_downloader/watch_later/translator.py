import win32gui
import win32api

import base_methods as gh
from PIL import ImageGrab, Image
from bilibili_downloader.__bilibili_parameters__ import *
import time
import sys
from base_methods.para_initializer import read_parameters

# ====================================================path operation====================================================
import os
cwd = os.getcwd()
while os.path.basename(cwd) != PROJECT_NAME:
    cwd = os.path.dirname(cwd)

cwd_name = PROJECT_NAME
working_folder = sys.path[0]

PRODUCED_PARAMETERS, CUSTOM_PARAMETERS = read_parameters(cwd_name, working_folder)

#  ======================================================parameters=====================================================
threshold_change_ratio_for_episode = 0.1


#  ======================================================variables======================================================
watch_later_start_picture = Image.open(os.path.join(working_folder, "pics", "dynamic_searching", "start_page.png"))
select_all_button_picture = Image.open(os.path.join(cwd, "pics", "buttons", "select_all_button.png"))


#  ======================================================functions======================================================
def set_focus_to_bilibili_app(name):
    hwndMain = win32gui.FindWindow(None, name)
    win32gui.SetForegroundWindow(hwndMain)


def find_pic(start_picture):
    if gh.basicpe.search_given_picture_in_area(start_picture, ((0, 0), (200, 100)), full_screen=True):
        return True
    else:
        return False


def scroll_to_the_bottom():
    gh.complexac.scroll_to_the_end(((0, 115), (1920, 1080)), "down", "mouse_wheel")


reach_the_top = gh.complexac.reach_the_top


def download_one_page():
    def click_and_wait(picture, wait_time=0.5, try_times=3):
        try_counts = 0
        while gh.complexac.take_action_to_detect_change(
                ((0, 0), (1920, 1080)),
                gh.complexac.click_center_of_a_picture,
                wait_time,
                True,
                picture) > 0.845:
            try_counts += 1
            print("counting!")
            if try_counts >= try_times:
                print("action {0} with parameters {1} not found and being escaped".format(
                    "click_center_of_a_picture", picture))
                return -1
        return 0

    back_button = PRODUCED_PARAMETERS["button_positions"]["back_button"]
    confirm_button = PRODUCED_PARAMETERS["button_positions"]["confirm_button"]
    download_button = PRODUCED_PARAMETERS["button_positions"]["download_button"]
    select_all_button = PRODUCED_PARAMETERS["button_positions"]["select_all_button"]
    start_download_button = PRODUCED_PARAMETERS["button_positions"]["start_download_button"]
    for episode in CUSTOM_PARAMETERS["episode_positions"]:
        if click_and_wait(episode) == -1:
            continue

        if click_and_wait(download_button) == -1:
            click_and_wait(back_button)
            continue
        if gh.basicpe.search_given_picture_in_area(select_all_button_picture, ((1040, 1020), (1920, 1080))):
            click_and_wait(select_all_button)
            click_and_wait(confirm_button)
        click_and_wait(start_download_button)
        click_and_wait(back_button)
