import win32gui
import win32api
import win32con

import base_methods as gh
from PIL import ImageGrab, Image
from bilibili_downloader.__bilibili_parameters__ import *
import time
import sys
import numpy as np
from base_methods.para_initializer import read_parameters
from base_methods.__parameters__ import VK_CODE

from chrome_game_player.__chrome_parameters__ import FullScreenPara


def grab_dinosaur_pic():
    return gh.perceptions_based_on_pywin32.screenshot_certain_place(FullScreenPara().DINOSAUR_POSITION).convert("L")


def grab_detecting_area():
    return gh.perceptions_based_on_pywin32.screenshot_certain_place(FullScreenPara().detect_area).convert("L")


def divide_pictures(image, dividing_step):
    """dividing picture based on given step

    For something left and not enough to generate a new picture, will be deprecated
    :param dividing_step: in pixels
    :return:
    """
    step_x, step_y = dividing_step
    result = []
    np_image = np.array(image)

    for i in range(step_x, np_image.shape[0] + 1, step_x):
        for j in range(step_y, np_image.shape[1] + 1, step_y):
            result.append(np_image[i - step_x:i, j - step_y:j])
    return result


def jump():
    key_code = VK_CODE["spacebar"]
    win32api.keybd_event(key_code, 0, 0, 0)
    time.sleep(0.1)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)


def grab_background():
    return gh.perceptions_based_on_pywin32.screenshot_certain_place(FullScreenPara().BACK_GROUND).convert("L")


def optimise_grab_func(detect_area, background_area):
    screen_shot = ImageGrab.grab().convert("L")
    screen_shot = np.array(screen_shot)

    ((left, top), (right, bottom)) = detect_area
    detect_area_im = Image.fromarray(screen_shot[top: bottom, left: right])
    ((left, top), (right, bottom)) = background_area
    background_area_im = Image.fromarray(screen_shot[top: bottom, left: right])

    return detect_area_im, background_area_im


if __name__ == "__main__":
    image = gh.perceptions_based_on_pywin32.screenshot_certain_place(FullScreenPara().detect_area)
    image.show()