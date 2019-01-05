import base_methods as gh
import sys

from bilibili_downloader.__bilibili_parameters__ import *


#  Set your path here
cwd_name = PROJECT_NAME  # the name of the project. set this so the work flow generator can read parameters
# recursively
working_folder = sys.path[0]


#  Write your customized functions here. Remember to register them later in function_list_to_implement
def calculate_each_episode_poistion(state):
    pos_left_top = state["PRODUCED_PARAMETERS"]["pos_left_top"]
    pos_right_bottom = state["PRODUCED_PARAMETERS"]["pos_right_bottom"]
    episode_size = state["PRODUCED_PARAMETERS"]["single_episode"]
    pointer_right_bottom = pos_right_bottom

    while pointer_right_bottom[1][0] >= pos_left_top[1][0]:  # pointer_right_bottom below the left top
        while pointer_right_bottom[1][1] >= pos_left_top[1][1]:  # pointer_right_bottom is on the right side of the left column


    state["CUSTOM_PARAMETERS"]

#  Write settings in this file. Run this file to initialize for the app
button_dict = {

}  # buttons

function_list_to_implement = [
    calculate_each_episode_poistion
]  # functions to run after init process

element_size_dict = {

}  # elements which need to be measured sizes

para_dict = {
    "button_dict": button_dict,
    "function_list_to_implement": function_list_to_implement,
    "element_size_dict": element_size_dict,
}

if __name__ == "__main__":
    gh.para_initializer.init_parameters(para_dict, cwd_name, working_folder)
