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

user32 = windll.user32
user32.SetProcessDPIAware()


def click(x, y):
    """
    Give a click on the screen at position (x, y)

    :param x: x-axis
    :param y: y-axis
    :return: None
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def double_click(x, y):
    """
    Give a click on the screen at position (x, y)

    :param x: x-axis
    :param y: y-axis
    :return: None
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def press(key):
    """
    Press a certain key

    :param key: the key string
    :type: string
    :return: None
    """
    key_code = VK_CODE[key]
    win32api.keybd_event(key_code, 0, 0, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_two(key1, key2):
    """
    Press two keys at the same time. Which could be used to press combination like ctrl + c

    :param key1: the key 1 string
    :param key2: the key 2 string
    :return: None
    """
    key_code1 = VK_CODE[key1]
    key_code2 = VK_CODE[key2]
    win32api.keybd_event(key_code1, 0, 0, 0)
    win32api.keybd_event(key_code2, 0, 0, 0)
    win32api.keybd_event(key_code1, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(key_code2, 0, win32con.KEYEVENTF_KEYUP, 0)


def get_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


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


def key_board_recorder():
    key_states = {}
    key_new_states = {}
    key_timers = {}

    for i in range(0xFF):
        key_states[str(i)] = win32api.GetKeyState(i)  # Button down = 0 or 1. Button up = -127 or -128
        key_new_states[str(i)] = win32api.GetKeyState(i)  # Button down = 0 or 1. Button up = -127 or -128
        key_timers[str(i)] = 0

    while True:
        for i in range(0xFF):
            key_new_states[str(i)] = win32api.GetKeyState(i)  # Refresh key states

            if key_new_states[str(i)] != key_states[str(i)]:
                key_states[str(i)] = key_new_states[str(i)]

                this_key = [key for key, value in VK_CODE.items() if value == i]
                if len(this_key) > 0:
                    this_key = this_key[0]

                if key_states[str(i)] < 0:
                    if this_key in VK_CODE.keys():
                        temp_res = "Pressed," + this_key
                        if i == 0x01 or i == 0x00:
                            _, _, cursor_pos = win32gui.GetCursorInfo()
                            temp_res += "," + str(cursor_pos)
                            with open("running_record", "a") as file:
                                file.write(temp_res)
                                file.write("\n")
                        else:
                            with open("running_record", "a") as file:
                                file.write(temp_res)
                                file.write("\n")
                        key_timers[str(i)] = time.time()
                    else:
                        print('Unknown' + ' pressed')
                else:
                    if this_key in VK_CODE.keys():
                        temp_res = "Released," + this_key + "," + str((time.time() - key_timers[str(i)]))
                        if i == 0x01 or i == 0x00:
                            _, _, cursor_pos = win32gui.GetCursorInfo()
                            temp_res += "," + str(cursor_pos)
                            with open("running_record", "a") as file:
                                file.write(temp_res)
                                file.write("\n")
                        else:
                            with open("running_record", "a") as file:
                                file.write(temp_res)
                                file.write("\n")
                    else:
                        print('Unknown' + ' released')


def reproduce_operation_from_file(path):
    key_timers = {}
    to_be_released_buttons = []

    for i in VK_CODE.keys():
        key_timers[i] = 0

    with open(path, "r") as file:
        all_records = file.read()

    records_split = all_records.split("\n")

    for record in range(len(records_split)):
        command = records_split[record].split(",")

        if command[0] == "Pressed":
            if command[1] == "mouse_left" or command[1] == "mouse_right":
                pass
            else:
                win32api.keybd_event(VK_CODE[command[1]], 0, 0, 0)
                key_timers[command[1]] = time.time()
        elif command[0] == "Released":
            if command[1] == "mouse_left" or command[1] == "mouse_right":
                pass
            else:
                if time.time() - key_timers[command[1]] > float(command[2]):
                    win32api.keybd_event(VK_CODE[command[1]], 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    to_be_released_buttons.append(record)
        else:
            print("Unknown command detected, original commend is", ":", records_split[record])

        for record in to_be_released_buttons:
            if command[1] == "mouse_left" or command[1] == "mouse_right":
                pass
            else:
                if time.time() - key_timers[command[1]] > float(command[2]):
                    win32api.keybd_event(VK_CODE[command[1]], 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    to_be_released_buttons.append(record)
    # while(len)

if __name__ == "__main__":
    # key_board_recorder()
    reproduce_operation_from_file("running_record")