"""
This windows-python operating program is built based on pywin32. Which is a great python library.
"""

import time
import win32api
import win32gui
import win32ui
from PIL import ImageGrab, Image
import win32con
from ctypes import windll

import numpy as np
from base_methods.__parameters__ import VK_CODE
import win32clipboard
import random

# Set the screenshot based on the DPI of the client
user32 = windll.user32
user32.SetProcessDPIAware()


def get_clipboard():
    """Get the text in the clipboard

    :return: the text in clipboard
    :rtype: str
    """
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def full_screen_checker(name, resolution_x, resolution_y):
    """Check selected window is in full-screen mode or not.

    It performs the checking process by comparing the size of the window to the resolution of the monitor.

    :param name: the name of selected window
    :type: str
    :param resolution_x: the resolution of the monitor
    :type: int
    :param resolution_y: the resolution of the monitor
    :type: int
    :return: whether the selected window is in full-screen or not
    :rtype: Boolean
    """
    function_name = full_screen_checker.__name__ + ": "
    hwndMain = win32gui.FindWindow(None, name)

    print(function_name, "found window -", hwndMain)

    win32gui.SetForegroundWindow(hwndMain)
    left, top, right, bottom = win32gui.GetWindowRect(hwndMain)

    print(function_name, "left", left)
    print(function_name, "right", right)
    print(function_name, "top", top)
    print(function_name, "bottom", bottom)

    print(function_name, "size:", right - left, "x", bottom - top)

    if right - left >= resolution_x and bottom - top >= resolution_y:
        return True
    else:
        return False


def search_given_picture_in_area_and_give_pos(target_pic, search_area, full_screen=False, debug_mode=False, debug_pic=None):
    """Search in given area to find target picture

    This function will search in an area to find the target picture. If any part in this area is EXACTLY the same with
    the target picture, return the position. Else return None. If full_screen is set to True, this function will ignore
    search area and search the target picture through whole screen.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param search_area: the area to be searched
    :type: ((left, top), (right, bottom))
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the position of the picture, or None if not found
    :rtype: ((left, top), (right, bottom)) / None
    """
    # TODO Finish the comments
    if debug_mode:
        screen_shot = debug_pic
        if debug_pic is None:
            raise ValueError("Missing debug picture")
    else:
        screen_shot = ImageGrab.grab()
    screen_shot = np.array(screen_shot)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here
    ((left, top), (right, bottom)) = search_area
    if full_screen:
        search_window = screen_shot
    else:
        search_window = screen_shot[top: bottom, left: right]

    target = np.array(target_pic)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here

    for line_index in range(search_window.shape[0]):
        for pixel_index in range(search_window.shape[1]):
            if search_window.shape[0] - line_index > target.shape[0] and search_window.shape[1] - pixel_index > target.shape[1]:
                if (search_window[line_index][pixel_index] == target[0][0]).all():
                            if (target == search_window[line_index:line_index + target.shape[0],
                                          pixel_index: pixel_index + target.shape[1]]).all():
                                if full_screen:
                                    return (pixel_index, line_index), (pixel_index + target.shape[1], line_index + target.shape[0])
                                else:
                                    return (left + pixel_index, top + line_index), (left + pixel_index + target.shape[1], top + line_index + target.shape[0])
    return None

    # TODO Optimize this function. It now needs 3.7s to scan 1920*1080 screen

    # TODO Modify this function to threshold version


def search_given_picture_in_area(target_pic, search_area, full_screen=False):
    """Search in given area to find target picture

    This function will search in an area to find the target picture. If any part in this area is EXACTLY the same with
    the target picture, return True. Else return False. If full_screen is set to True, this function will ignore
    search area and search the target picture through whole screen.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param search_area: the area to be searched
    :type: ((left, top), (right, bottom))
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: whether the picture is in the given area
    :rtype: Boolean
    """
    res = search_given_picture_in_area_and_give_pos(target_pic, search_area, full_screen)
    if res is None:
        return False
    else:
        return True


def comparing_two_pictures(image_1, image_2):
    """Comparing two pictures and give their similarity.

    :param image_1: the picture to be compared
    :type: PIL image file
    :param image_2: the picture to be compared
    :type: PIL image file
    :return: similarity, the same points ratio in the picture. Here we define "the same" as the same color in the same
    place.
    :rtype: double
    """
    np_im1 = np.array(image_1)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here
    np_im2 = np.array(image_2)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here

    res_im = np_im1 - np_im2
    number_of_the_same = res_im.size - np.count_nonzero(res_im)
    return number_of_the_same / res_im.size


def screenshot_certain_place(screenshot_window):
    """Take screenshot from certain area

    :param screenshot_window: the position to take the screenshot
    :type: ((left, top), (right, bottom))
    :return: the screenshot
    :rtype: PIL image file
    """
    screen_shot = ImageGrab.grab()
    screen_shot = np.array(screen_shot)

    ((left, top), (right, bottom)) = screenshot_window

    if left < 0:
        left = 0
    if top < 0:
        top = 0

    if right <= left:
        raise ValueError("Right coordinates should be larger than left")
    if bottom <= top:
        raise ValueError("Bottom coordinates should be larger than top")

    result_np = screen_shot[top: bottom, left: right]

    return Image.fromarray(result_np)


# -----------------------------------------For Research Purpose-----------------------------------------
def scan_aera(scan_size, size_of_window, scan_position):
    result_list = []

    sp_left, sp_top, sp_right, sp_bottom = size_of_window

    sp_x_1 = sp_left + scan_position[0]
    sp_x_2 = sp_left + scan_position[0] + scan_size[0]
    sp_y_1 = sp_top + scan_position[1]
    sp_y_2 = sp_top + scan_position[1] + scan_size[1]

    sp_im = ImageGrab.grab()
    sp_pix = sp_im.load()

    for sp_move_y in range(sp_y_1, sp_y_2, 1):
        for sp_move_x in range(sp_x_1, sp_x_2, 1):
            # win32api.SetCursorPos((sp_move_x, sp_move_y))
            result_list.append(sp_pix[sp_move_x, sp_move_y])
            # time.sleep(0.1)
            # print(sp_pix[sp_move_x, sp_move_y])

    return result_list


def scan_aera_unchanged_in_time(scan_size, size_of_window, scan_position, time_gap):
    last_image = scan_aera(scan_size, size_of_window, scan_position)
    time.sleep(time_gap)
    present_image = scan_aera(scan_size, size_of_window, scan_position)
    if present_image == last_image:
        return True
    else:
        return False


def get_mouse_position(name):
    hwndMain = win32gui.FindWindow(None, name)
    print("hwndMain:", hwndMain)

    win32gui.SetForegroundWindow(hwndMain)

    left, top, right, bottom = win32gui.GetWindowRect(hwndMain)
    print("left", left)
    print("right", right)
    print("top", top)
    print("bottom", bottom)

    while True:
        flags, hcursor, (x, y) = win32gui.GetCursorInfo()

        print((x, y), "|True: ", (x - left, y - top))
        time.sleep(5)


def save_and_compare_pic(name, size_of_window, scan_position, scan_size):
    """
    Based on the search area given, store the certain area picture for later comparision.
    This function should be used separately and shall not be used in the main chatting program.

    :param name:
    :param size_of_window:
    :param scan_position:
    :param scan_size:
    :return:
    """
    result_list = scan_aera(size_of_window, scan_position, scan_size)
    outfile = name
    temp_res = np.array(result_list)
    np.save(outfile, np.array(result_list))


if __name__ == "__main__":
    win32api.Beep(3000, 500)

    # start = time.time()
    # target_pic = Image.open("pic_search_test.png")
    # print(search_given_picture_in_area_and_give_pos(target_pic, ((0, 0), (1920, 1080)), full_screen=False))
    # print("used time:", time.time() - start)

    # image1 = Image.open("mouse_hover.png")
    # image2 = Image.open("mouse_hover_fixed.png")
    # print(comparing_two_pictures(image1, image2))

    im = screenshot_certain_place(((100, 100), (200, 220)))
    im.show()
