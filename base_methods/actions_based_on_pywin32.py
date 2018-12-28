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
from base_methods.__parameters__ import VK_CODE
import win32clipboard
import random


def click(x, y):
    """Give a click on the screen at position (x, y)

    :param x: x-axis
    :param y: y-axis
    :return: None
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def right_click(x, y):
    """Give a right click on the screen at position (x, y)

    :param x: x-axis
    :param y: y-axis
    :return: None
    """
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def double_click(x, y):
    """Give a double clicks on the screen at position (x, y)

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


def click_in_list(click_list, time_list, press_time_list):
    """Click a sequence mouse buttons by the time intervals given in time_list.

    The size of click_list should be the size of time_list plus 1. i.e. len(click_list) = len(time_list) + 1

    :param click_list: the list contains mouse buttons to be clicked. Which could be either 'left' or 'right'.
    :type: list
    :param time_list: the time interval between keys.
    :type: list
    :return: None
    """
    # TODO


def press(key):
    """Press a certain key on keyboard

    :param key: the key string
    :type: string
    :return: None
    """
    key_code = VK_CODE[key]
    win32api.keybd_event(key_code, 0, 0, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def press_two(key1, key2):
    """Press two keys on keyboard at the same time.

    Which could be used to press shortcuts combination such as ctrl + c

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


def press_in_list(press_list, time_list, press_time_list):
    """Press a sequence key buttons by the time intervals given in time_list.

    The size of click_list should be the size of time_list plus 1. i.e. len(press_list) = len(time_list) + 1

    :param press_list: the list contains mouse buttons to be clicked. Which should be the key names.
    :type: list
    :param time_list: the time interval between keys.
    :type: list
    :return: None
    """
    # TODO

def set_clipboard(text):
    """Set the clipboard to certain text

    :param text: the text to be set to clipboard
    :type: str
    :return: None
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()


if __name__ == "__main__":
    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)
    win32api.Beep(3000, 100)
