import base_methods as gh
import os
import sys

from PIL import Image

#  Set your path here
cwd_name = "bilibili_downloader"  # the name of the project. set this so the work flow generator can read parameters
# recursively
pic_path = "pics"
working_folder = sys.path[0]


#  Write your customized functions here. Remember to register them later in function_list_to_implement


#  Write settings in this file. Run this file to initialize for the app
button_dict = {
    "download_button": (Image.open(os.path.join(working_folder, pic_path, "download_button.png")),
                        Image.open(os.path.join(working_folder, pic_path, "episode_pic_to_search.png"))),
    "select_all_button": (Image.open(os.path.join(working_folder, pic_path, "select_all_button.png")),
                          Image.open(os.path.join(working_folder, pic_path, "episode_page_download_button_pic_to_search.png"))),
    "confirm_button": (Image.open(os.path.join(working_folder, pic_path, "confirm_button.png")),
                       Image.open(os.path.join(working_folder, pic_path, "episode_page_download_button_pic_to_search.png"))),
    "start_download_button": (Image.open(os.path.join(working_folder, pic_path, "start_download_button.png")),
                              Image.open(os.path.join(working_folder, pic_path, "episode_page_downloading_page_pic_to_search.png"))),
    "back_button": (Image.open(os.path.join(working_folder, pic_path, "back_button.png")),
                    Image.open(os.path.join(working_folder, pic_path, "episode_pic_to_search.png"))),
}  # buttons

function_list_to_implement = [

]  # functions to run after init process

element_size_dict = {
    "single_episode": Image.open(os.path.join(sys.path[0], pic_path, "mouse_hover.png"))
}  # elements which need to be measured sizes

#  Register your parameters here
para_dict = {
    "button_dict": button_dict,
    "function_list_to_implement": function_list_to_implement,
    "element_size_dict": element_size_dict,
}

if __name__ == "__main__":
    gh.working_flow.init_working_flow(para_dict, cwd_name, working_folder)
