import base_methods as gh
import sys


#  Set your path here
cwd_name = "bilibili_downloader"  # the name of the project. set this so the work flow generator can read parameters
# recursively
working_folder = sys.path[0]


#  Write your customized functions here. Remember to register them later in function_list_to_implement
def testfunc(state):
    print("Now from test func")
    print("button_dict", state["NECESSARY_PARAMETERS"]["button_dict"])
    print("function_list_to_implement", state["NECESSARY_PARAMETERS"]["function_list_to_implement"])
    print("element_size_dict", state["NECESSARY_PARAMETERS"]["element_size_dict"])
    print("button_positions", state["PRODUCED_PARAMETERS"]["button_positions"])
    print("element_sizes", state["PRODUCED_PARAMETERS"]["element_sizes"])

    state["NECESSARY_PARAMETERS"]["button_dict"] = None
    print("test func now end")
    return state


def testfunc2(state):
    print("Now from test func2")
    print("button_dict", state["NECESSARY_PARAMETERS"]["button_dict"])
    print("function_list_to_implement", state["NECESSARY_PARAMETERS"]["function_list_to_implement"])
    print("element_size_dict", state["NECESSARY_PARAMETERS"]["element_size_dict"])
    print("button_positions", state["PRODUCED_PARAMETERS"]["button_positions"])
    print("element_sizes", state["PRODUCED_PARAMETERS"]["element_sizes"])
    print("test func2 now end")
    return state

#  Write settings in this file. Run this file to initialize for the app
button_dict = {

}  # buttons

function_list_to_implement = [
    testfunc,
    testfunc2,
]  # functions to run after init process

element_size_dict = {

}  # elements which need to be measured sizes

para_dict = {
    "button_dict": button_dict,
    "function_list_to_implement": function_list_to_implement,
    "element_size_dict": element_size_dict,
}

if __name__ == "__main__":
    gh.para_initializer.init_parameters(para_dict, cwd_name, working_folder, force_refresh=True)
