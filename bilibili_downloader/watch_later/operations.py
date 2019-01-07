from bilibili_downloader.watch_later.translator import *


set_focus_to_bilibili_app("哔哩哔哩动画")
time.sleep(0.1)
# if find_pic(watch_later_start_picture):
scroll_to_the_bottom()

win32api.Beep(3000, 100)
download_one_page()

    # give_the_number_of_downloaded_videoes()
# else:
#     watch_later_start_picture.show()
#     raise ValueError("Not in 'watch_later' page in bilibili app")


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
