from PIL import ImageGrab, Image
import numpy as np
import base_methods.actions_based_on_pywin32 as ac
import base_methods.perceptions_based_on_pywin32 as pe
import base_methods.core as core
from base_methods.__parameters__ import VK_CODE

import win32gui
import win32api
import win32con
import time


def all_colors_counts(image_path):
    """Return all colors  counts in the given image

    :param image_path: the path of image to be detected
    :type: str
    :return: the main color and the ratio
    :rtype: list, each element is in the form of (R, G, B)
    """
    im = Image.open(image_path)
    np_im = np.array(im)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here
    print("input image size:", np_im.shape)
    colors = {}

    for line in np_im:
        for pixel in line:
            color_key = str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])
            if color_key in colors:
                colors[color_key] += 1
            else:
                colors[color_key] = 1

    return colors


def main_color_detect(image_path):
    """Return the main color of given image and its ratio in the whole picture

    :param image_path: the path of image to be detected
    :type: str
    :return: the main color and the ratio
    :rtype: ((R, G, B), ratio)
    """
    im = Image.open(image_path)
    np_im = np.array(im)
    colors = all_colors_counts(image_path)

    main_color = sorted(colors.items(), key=lambda d: d[1], reverse=True)
    ratio = int(main_color[0][1]) / (np_im.shape[0] * np_im.shape[1])
    return main_color[0][0], ratio


def delete_color(original_image_path, result_path, color_to_delete, show=True, highlight_mode=False):
    """Delete or highlight one color from the given picture and produce a new picture

    When deleted, the color will be marked as BLACK. When highlight mode is enabled, the high light color will be marked
    as WHITE and the rest of the picture will be  marked as BLACK.

    :param original_image_path: the picture to be processed
    :type: str
    :param result_path: the path to store results
    :type: str
    :param color_to_delete: the color to be deleted
    :type: (R, G, B)
    :param show: show the processed picture or not
    :type: Boolean
    :param highlight_mode:
    :return: how many pixels in this picture is changed
    :rtype: (number_of_pixels, ratio_of_pixels, total_pixels_in_the_pic)
    """
    im = Image.open(original_image_path)
    np_im = np.array(im)[:, :, :3]  # sometimes PNG files can have 4 channels, which are not needed here
    print("input image size:", np_im.shape)

    for line_index in range(np_im.shape[0]):
        for pixel_index in range(np_im.shape[1]):
            if (np_im[line_index][pixel_index] == np.array(color_to_delete)).all():
                if highlight_mode:
                    np_im[line_index][pixel_index] = np.array((255, 255, 255))
                else:
                    np_im[line_index][pixel_index] = np.array((0, 0, 0))
            else:
                if highlight_mode:
                    np_im[line_index][pixel_index] = np.array((0, 0, 0))

    new_im = Image.fromarray(np_im)
    new_im.save(result_path)
    if show:
        new_im.show()


def measure_scroll_units(start_step=137):
    step = start_step
    while win32api.GetKeyState(VK_CODE["esc"]) >= 0:  # Button down = 0 or 1. Button up = -127 or -128
        if win32api.GetKeyState(VK_CODE["w"]) < 0:
            step += 1
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, step)
            print(step)
        if win32api.GetKeyState(VK_CODE["s"]) < 0:
            step -= 1
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, step)
            print(step)
        time.sleep(0.2)
    print("final step ", step)


if __name__ == "__main__":
    # print(all_colors_counts("mouse_hover.png"))
    # print(main_color_detect("mouse_hover.png"))
    # delete_color("mouse_hover.png", "mouse_hover_fixed.png", (204, 204, 204), highlight_mode=False)
    measure_scroll_units()
