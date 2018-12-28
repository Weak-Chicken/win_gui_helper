import win32gui

import base_methods as gh
from PIL import ImageGrab, Image
from bilibili_downloader.__bilibili_parameters__ import *


#  ======================================================parameters=====================================================
threshold_change_ratio = 0.9


#  ======================================================variables======================================================
start_picture = ImageGrab.grab()
watch_later_start_picture = Image.open(im_path)  # TODO


#  ======================================================functions======================================================
reach_the_top = gh.complexac.reach_the_top


def download_one_line():  # main function
    for i in range(EPISODE_PER_LINE):
        click_into_one_element()
        click_download_button()
        if multiple_episode:
            click_all_select_button()
        # Then Download page will be shown
        click_download_comfirmation_button()
        go_back_to_upper_page()


def scroll_to_the_bottom():
    gh.complexac.scroll_to_the_end()  # TODO


def click_into_one_element():
    search_box_offset = (SINGLE_EPISODE_SIZE[0], SINGLE_EPISODE_SIZE[1] / 2)
    search_box_size = SINGLE_EPISODE_SIZE
    (cursor_x, cursor_y) = (SCREEN_RESOLUTION[0], BOTTOM_LINE_EPISODE_CENTER)

    # Auto produced
    search_box = (search_box_offset, search_box_size)
    while gh.complexac.move_mouse_to_detect_change_only_two_points(search_box, (cursor_x, cursor_y)) < \
            threshold_change_ratio:
        _, _, (cursor_x, cursor_y) = win32gui.GetCursorInfo()
    gh.complexac.click_here()


def click_download_button():
    # TODO
    if gh.complexac.search_given_picture_in_area_and_move_mouse(download_button):
        gh.complexac.click_here()


def multiple_episode():
    # TODO
    if gh.basicpe.search_given_picture_in_area(download_page):
        return False
    else:
        return True


def click_all_select_button():
    # TODO
    if gh.complexac.search_given_picture_in_area_and_move_mouse(select_all_button):
        gh.complexac.click_here()


def click_download_comfirmation_button():
    # TODO
    if gh.basicpe.search_given_picture_in_area(download_page):
        if gh.complexac.search_given_picture_in_area_and_move_mouse(download_comfirmation_button):
            gh.complexac.click_here()


def go_back_to_upper_page():
    gh.basicac.press('browser_back')


def go_to_upper_line():
    # TODO
    pass
