import base_methods.actions_based_on_pywin32 as ac
import base_methods.perceptions_based_on_pywin32 as pe
import time


def reach_the_end_core(scroll_window, scan_length, direction, try_time=5):
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
    if direction != "up" and direction != "down":
        print("Error: direction not defined")
        return False

    ((left, top), (right, bottom)) = scroll_window
    if direction == "up":
        first_im = pe.screenshot_certain_place(((left, top), (right, top + scan_length)))
    elif direction == "down":
        first_im = pe.screenshot_certain_place(((left, bottom - scan_length), (right, bottom)))
    print(left, top, right, bottom)

    ac.click((right - left) / 2 + left, (bottom - top) / 2 + top)
    time.sleep(0.01)
    if direction == "up":
        ac.scroll("up")
    elif direction == "down":
        ac.scroll("down")
    time.sleep(0.01)

    if direction == "up":
        second_im = pe.screenshot_certain_place(((left, top), (right, top + scan_length)))
    elif direction == "down":
        second_im = pe.screenshot_certain_place(((left, bottom - scan_length), (right, bottom)))

    if first_im == second_im:
        for i in range(try_time):
            ac.click((right - left) / 2 + left, (bottom - top) / 2 + top)
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
    return reach_the_end_core(scroll_window, scan_length, "up", try_time)


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
    return reach_the_end_core(scroll_window, scan_length, "down", try_time)


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
    # TODO
    while reach_the_end_core()


def move_mouse_to_match_pic(target_pic, search_box, mouse_start_pos, mouse_stop_pos, full_screen=False):
    """Move mouse in a line and search a specific picture while moving mouse

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the picture while moving the mouse. The search_box should contain the offset and
    size of the search box. It is calculated based on the position of the mouse. If the full_screen is set to True, the
    search_box will be disabled and whole screen picture will be searched.

    This method will return the similar ratio between the search box and the target picture. So be careful when using
    full_screen parameter. It might case the ratio very low.

    :param target_pic: the picture to be found in the area
    :type: PIL image file
    :param search_box: the area to be searched. Based on the position of the mouse
    :type:((offset_x, offset_y), (size_x, size_y))
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param mouse_stop_pos: the position where mouse stop to move
    :type: (x, y)
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the similar ratio between the search box and the target picture
    :rtype: double
    """
    # TODO


def move_mouse_to_detect_change(target_ratio, search_box, mouse_start_pos, mouse_stop_pos, full_screen=False):
    """Move mouse in a line and detect changes

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the changes while moving the mouse. The target ratio is the threshold to stop
    moving mouse. Once the changing ratio is higher than given target ratio, the method will return the final changing
    ratio. The search_box should contain the offset and size of the search box. It is calculated based on the position
    of the mouse. If the full_screen is set to True, the search_box will be disabled and whole screen picture will be
    searched.

    This method will return the change ratio inside the search box. So be careful when using full_screen parameter. It
    might consider something totally not related but changed stuffs.

    :param target_ratio: the threshold to stop searching
    :type: double
    :param search_box: the area to be searched. Based on the position of the mouse
    :type:((offset_x, offset_y), (size_x, size_y))
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param mouse_stop_pos: the position where mouse stop to move
    :type: (x, y)
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the change ratio if anything inside the search box has changed
    :rtype: double
    """
    # TODO


def move_mouse_to_detect_change_only_two_points(search_box, mouse_start_pos, next_point='left', full_screen=False):
    """Move mouse to next point and detect changes

    In many cases, some buttons or amines will only show when the mouse is passing by specific area. To click on these
    buttons/amines, we need to detect the changes while moving the mouse. And sometimes we only need the difference
    between two points. This method will compare the picture in the search box at current cursor position. Then, it
    will move the cursor to either left/right/up/down one pixel and compare the picture after moving the cursor.

    The search box here is defined based on before moving the cursor. So the moved one pixel will not affect the search
    box position. If full_screen is set to True, the search_box parameter will be ignored and it will compare across
    the whole screen.

    :param search_box: the area to be searched. Based on the position of the mouse
    :type:((offset_x, offset_y), (size_x, size_y))
    :param mouse_start_pos: the position where mouse start to move
    :type: (x, y)
    :param next_point: where to move the cursor
    :type: str, choose from left/right/up/down
    :param full_screen: directly search the whole screen
    :type: Boolean
    :return: the change ratio if anything inside the search box has changed
    :rtype: double
    """
    # TODO


def click_here():
    """Click at where the cursor is

    :return: None
    """
    # TODO


def search_given_picture_in_area_and_move_mouse(target_pic, search_area, full_screen=False):
    """Search in given area to find target picture and move cursor to there if the picture is found

    This function will search in an area to find the target picture. If any part in this aera is EXACTLY the same with
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
    # TODO


if __name__ == "__main__":
    print(reach_the_top(((560, 151), (1896, 717)), 5))
