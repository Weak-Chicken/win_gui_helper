from bilibili_downloader.watch_later.translator import *


if start_picture == watch_later_start_picture:
    scroll_to_the_bottom()

    while not reach_the_top():
        download_one_line()
        go_to_upper_line()

    # give_the_number_of_downloaded_videoes()


# ==========================The followings are directly wrote pseudo-code of the problem==========================

# if start_picture == watch_later_start_picture:
#     scroll_to_the_bottom()
#
#     while not reach_the_top():
#         from right to left:
#             click_into_one_element()
#             click_download_button()
#             if multiple_episode:
#                 click_all_select_button()
#             # Then Download page will be shown
#             click_download_button()
#             go_back_to_upper_page()
#         go_to_upper_line()
#
#     give_the_number_of_downloaded_videoes()
