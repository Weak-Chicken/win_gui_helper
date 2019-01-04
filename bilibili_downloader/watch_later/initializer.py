import base_methods as gh
import sys


#  Set your path here
cwd_name = "bilibili_downloader"  # the name of the project. set this so the work flow generator can read parameters
# recursively
pic_path = "pics"
working_folder = sys.path[0]


#  Write your customized functions here. Remember to register them later in function_list_to_implement


#  Write settings in this file. Run this file to initialize for the app
button_dict = {

}  # buttons

function_list_to_implement = [

]  # functions to run after init process

element_size_dict = {

}  # elements which need to be measured sizes

my_own = {

}

para_dict = {
    "button_dict": button_dict,
    "function_list_to_implement": function_list_to_implement,
    "element_size_dict": element_size_dict,
    "my_own": my_own,
}

if __name__ == "__main__":
    gh.working_flow.init_working_flow(para_dict, cwd_name, working_folder)
