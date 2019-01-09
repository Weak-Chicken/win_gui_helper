import win32api
import win32gui
import win32ui
import numpy as np

import base_methods.actions_based_on_pywin32 as ac
import base_methods.perceptions_based_on_pywin32 as pe
import time
from base_methods.__parameters__ import FLAG_ERROR_NAN_COORDINATE

# TODO Create a debug mode for following functions


def _reach_the_end_core(scroll_window, scan_length, direction, try_time=5):
    """Used to support function reach_the_top and reach_the_bottom. Details could be found in these two functions.

    :param scroll_window: the scrollable window position
    :type: ((left, top), (right, bottom))
    :param scan_length: the pixels to be scanned as reference
    :type: int
    :param direction: which direction to scroll
    :type: str, either "up" or "down"
    :param try_time: how many times to try before drawing conclusion
    :type: int
    :return: whether the current page is at the top
    :rtype: Boolean
    """
    # TODO Modify to support scroll length setting
    if direction != "up" and direction != "down":
        print("Error: direction not defined")
        return False

    ((left, top), (right, bottom)) = scroll_window
    if direction == "up":
        first_im = pe.screenshot_certain_place(((left, top), (right, top + scan_length)))
    elif direction == "down":
        first_im = pe.screenshot_certain_place(((left, bottom - scan_length), (right, bottom)))

    # ac.click((right - left) / 2 + left, (bottom - top) / 2 + top)
    time.sleep(0.01)
    if direction == "up":
        ac.scroll("up")
    elif direction == "down":
        ac.scroll("down")
    time.sleep(0.3)

    if direction == "up":
        second_im = pe.screenshot_certain_place(((left, top), (right, top + scan_length)))
    elif direction == "down":
        second_im = pe.screenshot_certain_place(((left, bottom - scan_length), (right, bottom)))

    if first_im == second_im:
        for i in range(try_time):
            # ac.click((right - left) / 2 + left, (bottom - top) / 2 + top)
            if direction == "up":
                ac.scroll("up")
            elif direction == "down":
                ac.scroll("down")

            if direction == "up":
                ith_im = pe.screenshot_certain_place(((left, top), (right, top + scan_length)))
            elif direction == "down":
                ith_im = pe.screenshot_certain_place(((left, bottom - scan_length), (right, bottom)))

            if ith_im != first_im:
                return False
        return True
    else:
        time.sleep(0.1)
        if direction == "up":
            ac.scroll("down")
        elif direction == "down":
            ac.scroll("up")
        return False


def reach_the_top(scroll_window, scan_length, try_time=5):
    """Return whether the current page is at the top. The user needs to illustrate where is the scrollable window and
    how many pixels down.

    The function provide the results based on the following operation: first, it tries to scroll up. If the page is then
    changed, which means that there is content above, so the program has not reached the top. On the contrary, if the
    program cannot see anything else after scrolling up, it should has reached the top.

    By default, it will try 5 times to scroll up.

    :param scroll_window: the scrollable window position
    :type: ((left, top), (right, bottom))
    :param scan_length: the pixels to be scanned as reference
    :type: int
    :param try_time: how many times to try before drawing conclusion
    :type: int
    :return: whether the current page is at the top
    :rtype: Boolean
    """
    return _reach_the_end_core(scroll_window, scan_length, "up", try_time)


def reach_the_bottom(scroll_window, scan_length, try_time=5):
    """Return whether the current page is at the bottom. The user needs to illustrate where is the scrollable window and
    how many pixels down.

    The function provide the results based on the following operation: first, it tries to scroll down. If the page is
    then changed, which means that there is content below, so the program has not reached the bottom. On the contrary,
    if the program cannot see anything else after scrolling down, it should has reached the bottom.

    By default, it will try 5 times to scroll down.

    :param scroll_window: the scrollable window position
    :type: ((left, top), (right, bottom))
    :param scan_length: the pixels to be scanned as reference
    :type: int
    :param try_time: how many times to try before drawing conclusion
    :type: int
    :return: whether the current page is at the bottom
    :rtype: Boolean
    """
    return _reach_the_end_core(scroll_window, scan_length, "down", try_time)


def scroll_to_the_end(scroll_window, direction, mode, scroll_bar='', max_wait_time=3):
    """Scroll to either top or bottom of the current page

    It can support up to three different scroll methods: mouse_wheel, keyboard and click_and_drag. In click_and_drag
    mode, the user has to give the scroll bar as a PIL image file. If this function later unable to find the scroll bar,
    an error will be given. If it cannot reach the top/bottom of the page, it will give an error. It will wait
    max_wait_time until give error.

    click_and_drag mode is currently not supported.

    :param scroll_window: the scrollable window position
    :type: ((left, top), (right, bottom))
    :param direction: either up or down
    :type: str, 'up' or 'down'
    :param mode: choose from one of the three modes
    :type: str, 'mouse_wheel', 'keyboard' or 'click_and_drag'
    :param scroll_bar: only will be used when mode is chosen to 'click_and_drag'
    :type: PIL image file
    :param max_wait_time: the time to wait before giving error message, in seconds
    :type: int
    :return: None
    """
    step = 10
    for i in range(max_wait_time):
        while not _reach_the_end_core(scroll_window, 8, direction):
            if mode == "mouse_wheel":
                for j in range(step):
                    ac.scroll(direction)
                    time.sleep(0.4)
            elif mode == "keyboard":
                if direction == "down":
                    for j in range(step):
                        ac.press("down_arrow")
                        time.sleep(0.4)
                elif direction == "up":
                    for j in range(step):
                        ac.press("up_arrow")
                        time.sleep(0.4)
            else:
                print("Error: Given mode is not supported currently")
            time.sleep(0.1)


def move_mouse_to_match_pic_res_in_list(target_pic, mouse_start_pos, mouse_stop_pos, full_screen=False, find_mode=False,
                                        threshold=0.5):
    """Move mouse in a line and search a specific picture while moving mouse

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the picture while moving the mouse. The search_box is calculated based on the
    position of the mouse. It will suppose cursor is at right bottom of the searching box and calculate the search area.
    The shape of the search box will be the same to the shape of target picture. If the full_screen is set to True, the
    search_box will be disabled and whole screen picture will be searched.

    This method will return the similar ratio between the search box and the target picture. So be careful when using
    full_screen parameter. It might case the ratio very low.

    The find mode is made for other function. When find mode is on, the threshold will be considered. Once the FIRST
    point satisfies the threshold is found, the point will be given and the function will be stopped.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param mouse_stop_pos: the position where mouse stop to move
    :type: (x, y)
    :param full_screen: directly search the whole screen
    :type: Boolean
    :param find_mode: whether to use find mode
    :type: Boolean
    :param threshold: the threshold used to define 'find'
    :type: double
    :return: ALL similar ratios between the search box and the target picture / Find result (point and rate)
    :rtype: list / (coordinate_x, coordinate_y, similar_rate) (Depends on 'find mode' controller)
    """
    # Init
    start_x, start_y = mouse_start_pos
    stop_x, stop_y = mouse_stop_pos
    start_x = int(start_x)
    start_y = int(start_y)
    stop_x = int(stop_x)
    stop_y = int(stop_y)

    (size_y, size_x) = np.array(target_pic).shape[:2]

    results_list = {}
    top = start_y - size_y
    if top < 0:
        raise ValueError("""Search box cannot be deployed in current mouse start position! Need more room on y axis
        you need {0} pixels available in y axis. However only {1} pixels available.""".format(size_y, start_y))
    bottom = start_y

    # Start here
    while start_x < stop_x or start_y < stop_y:
        left = start_x - size_x
        right = start_x
        if left < 0:
            raise ValueError("""Search box cannot be deployed in current mouse start position! Need more room on x axis
        you need {0} pixels available in x axis. However only {1} pixels available.""".format(size_x, start_x))

        while start_y < stop_y:
            top = start_y - size_y
            bottom = start_y

            win32api.SetCursorPos((start_x, start_y))

            if full_screen:
                screen_shot = pe.ImageGrab.grab()
            else:
                try:
                    screen_shot = pe.screenshot_certain_place(((left, top), (right, bottom)))
                except ValueError:
                    start_y += 1
                    continue
            screen_shot = np.array(screen_shot)

            temp_res = pe.comparing_two_pictures(screen_shot, target_pic)
            if find_mode:
                if temp_res > threshold:
                    return start_x, start_y, temp_res
            else:
                results_list["((" + str(left) + "," + str(top) + "),(" + str(right) + "," + str(bottom) + "))"] = \
                    temp_res

            start_y += 1

        win32api.SetCursorPos((start_x, start_y))

        if full_screen:
            screen_shot = pe.ImageGrab.grab()
        else:
            try:
                screen_shot = pe.screenshot_certain_place(((left, top), (right, bottom)))
            except ValueError:
                start_x += 1
                continue
        screen_shot = np.array(screen_shot)

        temp_res = pe.comparing_two_pictures(screen_shot, target_pic)
        if find_mode:
            if temp_res > threshold:
                return start_x, start_y, temp_res
        else:
            results_list["((" + str(left) + "," + str(top) + "),(" + str(right) + "," + str(bottom) + "))"] = \
                temp_res

        start_x += 1

    return results_list


def move_mouse_to_match_pic(target_pic, mouse_start_pos, mouse_stop_pos, full_screen=False):
    """Move mouse in a line and search a specific picture while moving mouse

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the picture while moving the mouse. The search_box is calculated based on the
    position of the cursor. It will suppose cursor is at right bottom of the searching box and calculate the search area
    .The shape of the search box will be the same to the shape of target picture. If the full_screen is set to True, the
    search_box will be disabled and whole screen picture will be searched.

    This method will return the similar ratio between the search box and the target picture. So be careful when using
    full_screen parameter. It might case the ratio very low.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param mouse_stop_pos: the position where mouse stop to move
    :type: (x, y)
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the highest similar ratio between the search box and the target picture
    :rtype: double
    """
    results = move_mouse_to_match_pic_res_in_list(target_pic, mouse_start_pos, mouse_stop_pos, full_screen)

    return sorted(results.items(), key=lambda x: x[1], reverse=True)[0]


def move_mouse_to_detect_change(target_ratio, search_area, mouse_start_pos, mouse_stop_pos, full_screen=False):
    """Move mouse in a line and detect changes

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the changes while moving the mouse. The target ratio is the threshold to stop
    moving mouse. Once the changing ratio is higher than given target ratio, the method will return the final changing
    ratio. The search box is calculated based on the position of the cursor. It will suppose cursor is at right bottom
    of the searching box and calculate the search area. The shape of the search box will be the same to the shape of
    target picture. If the full_screen is set to True, the search_box will be disabled and whole screen picture will be
    searched.

    This method will return the change ratio inside the search box. So be careful when using full_screen parameter. It
    might consider something totally not related but changed stuffs.

    :param target_ratio: the threshold to stop searching
    :type: double
    :param search_area: the area to be searched, which is defined based on the position of cursor
    :type: (x, y)
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param mouse_stop_pos: the position where mouse stop to move
    :type: (x, y)
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the similarity ratio if anything inside the search box has changed and the cursor stopped position
    :rtype: (coordinate_x, coordinate_y, similar_rate)
    """
    # Init
    start_x, start_y = mouse_start_pos
    stop_x, stop_y = mouse_stop_pos
    start_x = int(start_x)
    start_y = int(start_y)
    stop_x = int(stop_x)
    stop_y = int(stop_y)

    screen_shot = pe.ImageGrab.grab()
    screen_shot = np.array(screen_shot)
    (size_x, size_y) = search_area

    top = start_y - size_y
    if top < 0:
        return FLAG_ERROR_NAN_COORDINATE, FLAG_ERROR_NAN_COORDINATE, 0
    bottom = start_y

    # Start
    while start_x < stop_x or start_y < stop_y:
        left = start_x - size_x
        right = start_x
        if left < 0:
            return FLAG_ERROR_NAN_COORDINATE, FLAG_ERROR_NAN_COORDINATE, 0

        while start_y < stop_y:
            if full_screen:
                search_window_1 = screen_shot
            else:
                search_window_1 = screen_shot[top: bottom, left: right]
            win32api.SetCursorPos((start_x, start_y))
            screen_shot = pe.ImageGrab.grab()
            screen_shot = np.array(screen_shot)
            if full_screen:
                search_window_2 = screen_shot
            else:
                search_window_2 = screen_shot[top: bottom, left: right]

            # print(1 - pe.comparing_two_pictures(search_window_1, search_window_2))
            if (1 - pe.comparing_two_pictures(search_window_1, search_window_2)) >= target_ratio:
                return start_x, start_y, pe.comparing_two_pictures(search_window_1, search_window_2)

            start_y += 1

        top = start_y - size_y
        if top < 0:
            return FLAG_ERROR_NAN_COORDINATE, FLAG_ERROR_NAN_COORDINATE, 0
        bottom = start_y

        # I think it is repeated here
        if full_screen:
            search_window_1 = screen_shot
        else:
            search_window_1 = screen_shot[top: bottom, left: right]
        win32api.SetCursorPos((start_x, start_y))
        screen_shot = pe.ImageGrab.grab()
        screen_shot = np.array(screen_shot)
        if full_screen:
            search_window_2 = screen_shot
        else:
            search_window_2 = screen_shot[top: bottom, left: right]

        # print(1 - pe.comparing_two_pictures(search_window_1, search_window_2))
        if (1 - pe.comparing_two_pictures(search_window_1, search_window_2)) >= target_ratio:
            return start_x, start_y, pe.comparing_two_pictures(search_window_1, search_window_2)

        start_x += 1

    return FLAG_ERROR_NAN_COORDINATE, FLAG_ERROR_NAN_COORDINATE, 0


def move_mouse_to_detect_change_only_two_points(search_area, direction='left', full_screen=False):
    """Move mouse to next point and detect changes

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the changes while moving the cursor. And sometimes we only need the difference
    between two points. This method will compare the picture in the search box at current cursor position. Then, it
    will move the cursor to either left/right/up/down one pixel and compare the picture after moving the cursor.

    The search box here is defined based on before moving the cursor. So the moved one pixel will not affect the search
    box position. If full_screen is set to True, the search_box parameter will be ignored and it will compare across
    the whole screen.

    :param search_area: the area to be searched, which is defined based on the position of cursor
    :type: (x, y)
    :param direction: where to move the cursor
    :type: str, choose from left/right/up/down
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the similarity ratio if anything inside the search box has changed
    :rtype: double / None
    """
    _, _, mouse_start_pos = win32gui.GetCursorInfo()
    mouse_stop_pos = list(mouse_start_pos)
    mouse_start_pos = list(mouse_start_pos)
    if direction == "left":
        mouse_stop_pos[0] -= 1
        mouse_start_pos[0] -= 2
    elif direction == "right":
        mouse_stop_pos[0] += 1
    elif direction == "up":
        mouse_stop_pos[1] -= 1
        mouse_start_pos[1] -= 2
    elif direction == "down":
        mouse_stop_pos[1] += 1
    else:
        raise ValueError("Given direction {0} is not defined".format(direction))

    # Init
    start_x, start_y = mouse_start_pos
    start_x = int(start_x)
    start_y = int(start_y)

    (size_x, size_y) = search_area

    top = start_y - size_y
    if top < 0:
        return None
    bottom = start_y
    left = start_x - size_x
    if left < 0:
        return None
    right = start_x

    if full_screen:
        screen_shot = pe.ImageGrab.grab()
        search_window_1 = np.array(screen_shot)
    else:
        screen_shot = pe.ImageGrab.grab((left, top, right, bottom))
        search_window_1 = np.array(screen_shot)
    win32api.SetCursorPos(mouse_stop_pos)
    if full_screen:
        screen_shot = pe.ImageGrab.grab()
        search_window_2 = np.array(screen_shot)
    else:
        screen_shot = pe.ImageGrab.grab((left, top, right, bottom))
        search_window_2 = np.array(screen_shot)

    return pe.comparing_two_pictures(search_window_1, search_window_2)


def click_here():
    """Click at where the cursor is

    :return: None
    """
    # TODO Add more modes to this function. Support for other clicks
    _, _, mouse_pos = win32gui.GetCursorInfo()
    ac.click(mouse_pos[0], mouse_pos[1])


def click_center_of_a_picture(area):
    # TODO Add more modes to this function. Support for other clicks
    ((left, top), (right, bottom)) = area
    ac.click(int((right - left) / 2 + left), int((bottom - top) / 2 + top))


def search_given_picture_in_area_and_move_mouse_to(target_pic, search_area, full_screen=False):
    """Search in given area to find target picture and move cursor to there if the picture is found

    This function will search in an area to find the target picture. If any part in this area is EXACTLY the same with
    the target picture, return True. Else return False. If full_screen is set to True, this function will ignore
    search area and search the target picture through whole screen. Besides, if the picture is found, move the cursor
    to the middle of the found picture.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param search_area: the area to be searched
    :type: ((left, top), (right, bottom))
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: whether the picture is in the given area
    :rtype: Boolean
    """
    res = pe.search_given_picture_in_area_and_give_pos(target_pic, search_area, full_screen)
    if res is None:
        return False
    else:
        ((left, top), (right, bottom)) = res
        win32api.SetCursorPos((int((right - left) / 2 + left), int((bottom - top) / 2 + top)))
        return True


def take_action_to_detect_change(search_area, action_function, wait_time, full_screen, *args):
    ((left, top), (right, bottom)) = search_area
    if full_screen:
        search_window_1 = pe.ImageGrab.grab()
    else:
        search_window_1 = pe.ImageGrab.grab((left, top, right, bottom))
    search_window_1 = np.array(search_window_1)

    action_function(*args)

    time.sleep(wait_time)

    if full_screen:
        search_window_2 = pe.ImageGrab.grab()
    else:
        search_window_2 = pe.ImageGrab.grab((left, top, right, bottom))
    search_window_2 = np.array(search_window_2)

    return pe.comparing_two_pictures(search_window_1, search_window_2)


# TODO precise comparision of two pictures


if __name__ == "__main__":
    # print(reach_the_bottom(((560, 151), (1896, 717)), 5))
    # scroll_to_the_end(((560, 151), (1896, 717)), "up", "keyboard")

    # target = pe.Image.open("test.png")
    # size_x = 100
    # size_y = 94
    # res = move_mouse_to_match_pic_res_in_list(target, (100, 94), (100, 294), find_mode=False, threshold=0.99)
    # res = move_mouse_to_match_pic(target, (100, 94), (200, 94))
    # print(res)
    # print(len(res))

    # print(move_mouse_to_detect_change(0.4, (20, 20), (20, 70), (300, 70), full_screen=False))

    # for i in range(200):
    #     print(move_mouse_to_detect_change_only_two_points((20, 20), "right"))

    # click_here()

    # target = pe.Image.open("test_button.png")
    # print(search_given_picture_in_area_and_move_mouse_to(target, ((0, 0), (100, 300)), full_screen=True))

    # click_center_of_a_picture(((0, 0), (1920, 1080)))

    def testfunc(para_1, para_2):
        print(para_1)
        print("===")
        print(para_2)
    print(take_action_to_detect_change(((0, 0), (1920, 1080)), testfunc, 1, True, 6, 3))
