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


#  ======================================================functions======================================================
def set_focus_to_bilibili_app(name):
    hwndMain = win32gui.FindWindow(None, name)
    win32gui.SetForegroundWindow(hwndMain)


def find_pic(start_picture):
    if gh.basicpe.search_given_picture_in_area(start_picture, ((0, 0), (200, 100))):
        return True
    else:
        return False


def scroll_to_the_bottom():
    gh.complexac.scroll_to_the_end(((0, 115), (1920, 1080)), "down", "mouse_wheel")


reach_the_top = gh.complexac.reach_the_top


def download_one_line():  # main function
    def click_into_one_element():
        # search_box_size = list(SINGLE_EPISODE_SIZE)

        _, _, (cursor_x, cursor_y) = win32gui.GetCursorInfo()
        # Auto produced
        # while not gh.complexac.move_mouse_to_detect_change_only_two_points(search_box_size, direction='left') is None:
        #     print(win32gui.GetCursorPos())
        #
        #     # gap some pixels, it is not necessary to search all points
        #     _, _, (cursor_x, cursor_y) = win32gui.GetCursorInfo()
        changed = False
        while not changed:
            time.sleep(0.5)
            screen_1 = gh.basicpe.screenshot_certain_place(((0, 0), (1920, 1080)))
            win32api.SetCursorPos((int(cursor_x - (SINGLE_EPISODE_SIZE[0]) - 60), cursor_y))
            time.sleep(0.1)
            gh.complexac.click_here()
            screen_2 = gh.basicpe.screenshot_certain_place(((0, 0), (1920, 1080)))
            print(gh.basicpe.comparing_two_pictures(screen_1, screen_2))
            if gh.basicpe.comparing_two_pictures(screen_1, screen_2) < 1:
                changed = True
            else:
                _, _, (cursor_x, cursor_y) = win32gui.GetCursorInfo()

        print("out")
        time.sleep(0.5)

    def click_download_button():
        if gh.complexac.search_given_picture_in_area_and_move_mouse_to(download_button, ((1040, 1020), (1920, 1080))):
            gh.complexac.click_here()
        else:
            raise ValueError("No download button")

    def multiple_episode():
        if gh.basicpe.search_given_picture_in_area(select_all_button, ((1041, 1020), (1920, 1080))):
            return True
        else:
            return False

    def click_all_select_button():
        if gh.complexac.search_given_picture_in_area_and_move_mouse_to(select_all_button, ((1040, 1020), (1920, 1080))):
            gh.complexac.click_here()
            gh.complexac.search_given_picture_in_area_and_move_mouse_to(confirm_button, ((1040, 1020), (1920, 1080)))
            gh.complexac.click_here()
        else:
            raise ValueError("No select all button")

    def click_download_confirmation_button():
        # if gh.basicpe.search_given_picture_in_area(download_page, ((700, 400), (1200, 680)), full_screen=True):
            if gh.complexac.search_given_picture_in_area_and_move_mouse_to(start_download_button, ((790, 440), (1130, 650))):
                gh.complexac.click_here()
            else:
                raise ValueError("No start downloading button")
        # else:
        #     raise ValueError("No download page")

    def go_back_to_upper_page():
        if gh.complexac.search_given_picture_in_area_and_move_mouse_to(back_button, ((0, 0), (70, 70))):
            gh.complexac.click_here()

    for i in range(EPISODE_PER_LINE):
        click_into_one_element()
        click_download_button()
        if multiple_episode():
            print("multiple")
            click_all_select_button()
        # Then Download page will be shown
        print("downloading")
        click_download_confirmation_button()
        time.sleep(0.5)
        go_back_to_upper_page()


def go_to_upper_line():
    # TODO
    pass
