from PIL import ImageGrab, Image
import numpy as np


def main_color_detect(image_path):
    """Return the main color of given image and its ratio in the whole picture

    :param image_path: the path of image to be detected
    :type: str
    :return: the main color and the ratio
    :rtype: ((R, G, B), ratio)
    """
    im = Image.open(image_path)
    np_im = np.array(im)
    print("input image size:", np_im.shape)
    colors = {}

    for line in np_im:
        for pixel in line:
            if str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2]) in colors:
                colors[str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])] += 1
            else:
                colors[str(pixel[0]) + ',' + str(pixel[1]) + ',' + str(pixel[2])] = 1

    main_color = sorted(colors.items(), key=lambda d: d[1], reverse=True)
    ratio = int(main_color[0][1]) / (np_im.shape[0] * np_im.shape[1])
    return main_color[0][0], ratio


def delete_color(original_image_path, result_path, color_to_delete):
    """Delete one color from the given picture and produce a new picture

    When deleted, the color will be marked as BLACK

    :param original_image_path: the picture to be processed
    :type: str
    :param result_path: the path to store results
    :type: str
    :param color_to_delete: the color to be deleted
    :type: (R, G, B)
    :return: how many pixels in this picture is changed
    :rtype: (number_of_pixels, ratio_of_pixels, total_pixels_in_the_pic)
    """
    # TODO
    im = Image.open(original_image_path)
    np_im = np.array(im)
    print("input image size:", np_im.shape)

    for line in range(np_im.shape[0]):
        for pixel in range(np_im.shape[1]):
            if np_im[line][pixel] == np.array(color_to_delete):
                pass


def highlight_different_color(original_image_path, result_path, color_to_highlight):
    """Highlight one color from the given picture

    The rest of the picture will be marked as black and high light color will be marked as white.

    :param original_image_path: the picture to be processed
    :type: str
    :param result_path: the path to store results
    :type: str
    :param color_to_highlight: the color to be highlighted
    :type: (R, G, B)
    :return: how many pixels in this picture is changed
    :rtype: (number_of_pixels, ratio_of_pixels, total_pixels_in_the_pic)
    """
    # TODO


if __name__ == "__main__":
    # print(main_color_detect("mouse_hover.png"))
    delete_color("mouse_hover.png", "mouse_hover_fixed.png", (204, 204, 204))
