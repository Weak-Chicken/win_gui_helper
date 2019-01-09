import win32gui
import win32api

import base_methods as gh
from PIL import ImageGrab, Image
from bilibili_downloader.__bilibili_parameters__ import *
import time
import sys
from base_methods.para_initializer import read_parameters
from base_methods.__parameters__ import VK_CODE

# ====================================================path operation====================================================
import os
cwd = os.getcwd()
while os.path.basename(cwd) != PROJECT_NAME:
    cwd = os.path.dirname(cwd)

cwd_name = PROJECT_NAME
working_folder = sys.path[0]

PRODUCED_PARAMETERS, CUSTOM_PARAMETERS = read_parameters(cwd_name, working_folder)

#  ======================================================parameters=====================================================
back_button = PRODUCED_PARAMETERS["button_positions"]["back_button"]
confirm_button = PRODUCED_PARAMETERS["button_positions"]["confirm_button"]
download_button = PRODUCED_PARAMETERS["button_positions"]["download_button"]
select_all_button = PRODUCED_PARAMETERS["button_positions"]["select_all_button"]
start_download_button = PRODUCED_PARAMETERS["button_positions"]["start_download_button"]


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


def click_and_wait(picture, wait_time=0.8, try_times=3):
    try_counts = 0
    similarity = gh.complexac.take_action_to_detect_change(
        ((0, 0), (1920, 1080)),
        gh.complexac.click_center_of_a_picture,
        wait_time,
        True,
        picture)
    while similarity > 0.975:
        try_counts += 1
        print("counting!", similarity)
        if try_counts >= try_times:
            print("action {0} with parameters {1} not found and being escaped".format(
                "click_center_of_a_picture", picture))
            return -1
    return 0


def download_one_line(cursor_pos=None):
    if cursor_pos is None:
        while win32api.GetKeyState(VK_CODE["enter"]) >= 0:
            time.sleep(0.1)

    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)

    if cursor_pos is None:
        episode = list(win32api.GetCursorPos())
    else:
        episode = cursor_pos

    pos_left_top = PRODUCED_PARAMETERS["button_positions"]["pos_left_top"][0]

    while episode[0] > pos_left_top[0]:
        episode_copy = episode
        if click_and_wait((episode, episode_copy)) == -1:
            continue

        if click_and_wait(download_button) == -1:
            click_and_wait(back_button)
            continue
        if gh.basicpe.search_given_picture_in_area(select_all_button_picture, ((900, 900), (1920, 1080))):
            click_and_wait(select_all_button)
            click_and_wait(confirm_button)
        click_and_wait(start_download_button)
        click_and_wait(back_button)
        episode[0] -= CUSTOM_PARAMETERS["large_episode_size"][0]

    win32api.SetCursorPos((1920, 540))
    episode[0] += CUSTOM_PARAMETERS["large_episode_size"][0] * CUSTOM_PARAMETERS["column_num"]
    return episode


def download_one_rest(cursor_pos):
    if cursor_pos is None:
        while win32api.GetKeyState(VK_CODE["enter"]) >= 0:
            time.sleep(0.1)

    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)

    if cursor_pos is None:
        episode = list(win32api.GetCursorPos())
    else:
        episode = cursor_pos
        episode[1] -= CUSTOM_PARAMETERS["large_episode_size"][1]
    pos_left_top = PRODUCED_PARAMETERS["button_positions"]["pos_left_top"][0]

    while episode[1] > pos_left_top[1]:
        while episode[0] > pos_left_top[0]:
            episode_copy = episode
            if click_and_wait((episode, episode_copy)) == -1:
                continue

            if click_and_wait(download_button) == -1:
                click_and_wait(back_button)
                continue
            if gh.basicpe.search_given_picture_in_area(select_all_button_picture, ((900, 900), (1920, 1080))):
                click_and_wait(select_all_button)
                click_and_wait(confirm_button)
            click_and_wait(start_download_button)
            click_and_wait(back_button)
            episode[0] -= CUSTOM_PARAMETERS["large_episode_size"][0]
        episode[0] += CUSTOM_PARAMETERS["large_episode_size"][0] * CUSTOM_PARAMETERS["column_num"]
        episode[1] -= CUSTOM_PARAMETERS["large_episode_size"][1]
