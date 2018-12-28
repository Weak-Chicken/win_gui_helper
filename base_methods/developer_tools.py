from PIL import ImageGrab, Image


def main_color_detect(image_path):
    """Return the main color of given image and its ratio in the whole picture

    :param image_path: the path of image to be detected
    :tyoe: str
    :return: the main color and the ratio
    :rtype: ((R, G, B), ratio)
    """
    # TODO


def delete_color(original_image_path, result_path, color_to_delete):
    """Delete one color from the given picture and produce a new picture

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
    pass
