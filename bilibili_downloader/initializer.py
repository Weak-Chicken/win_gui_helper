import base_methods as gh
import os
import sys

from PIL import Image

#  Set your path here
cwd_name = "bilibili_downloader"  # the name of the project. set this so the work flow generator can read parameters
# recursively
working_folder = sys.path[0]


#  Write your customized functions here. Remember to register them later in function_list_to_implement


#  Write settings in this file. Run this file to initialize for the app
button_dict = {

}  # buttons

function_list_to_implement = [

]  # functions to run after init process

element_size_dict = {

}  # elements which need to be measured sizes

#  Register your parameters here
para_dict = {
    "button_dict": button_dict,
    "function_list_to_implement": function_list_to_implement,
    "element_size_dict": element_size_dict,
}

if __name__ == "__main__":
    gh.para_initializer.init_parameters(para_dict, cwd_name, working_folder)
