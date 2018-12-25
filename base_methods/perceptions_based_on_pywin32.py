"""
This windows-python operating program is built based on pywin32. Which is a great python library.
"""

import time
import win32api
import win32gui
import win32ui
from PIL import ImageGrab
import win32con
from ctypes import windll

import numpy as np
from __parameters__ import VK_CODE
import win32clipboard
import random


# Set the screenshot based on the DPI of the client
user32 = windll.user32
user32.SetProcessDPIAware()


def get_clipboard():
    """
    Get the text in the clipboard

    :return: the text in clipboard
    :type: str
    """
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


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


def full_screen_checker(name, resolution_x, resolution_y):
    """
    Check selected window is in full-screen mode or not.
    It performs the checking process by comparing the size of the window to the resolution of the monitor.
    :param name: the name of selected window
    :type: str
    :param resolution_x: the resolution of the monitor
    :type: int
    :param resolution_y: the resolution of the monitor
    :type: int
    :return: whether the selected window is in full-screen or not
    :type: Boolean
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


# -----------------------------------------For Research Purpose-----------------------------------------
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
    print(full_screen_checker("New Tab - Google Chrome", 1920, 1080))
    # full_screen_checker("哔哩哔哩动画")
    sp_im = ImageGrab.grab()
    sp_im.save("test.png")
