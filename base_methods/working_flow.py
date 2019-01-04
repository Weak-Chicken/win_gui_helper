import base_methods.actions_based_on_pywin32 as ac
import base_methods.perceptions_based_on_pywin32 as pe
import base_methods.core as core

import os
import pickle
from tqdm import tqdm
import json


INPUT_PARAMETERS = {
    "button_dict": None,  # form in {"button_name": (button_picture_in_PIL_IMAGE_form, pictures_used_to_search_in_PIL_IMAGE_form)}
    "function_list_to_implement": None,  # the functions need to be run after initialization
    "element_size_dict": None,  # form in {"element_name": element_picture_in_PIL_IMAGE_form}
}

PRODUCED_PARAMETERS = {
    "button_positions": {},
    "element_sizes": {},
}

FILE_SAVE_FORMAT = None

# TODO Screen resolution checker


def init_working_flow(para_dict, cwd, force_refresh=False, file_save_format="json"):
    global FILE_SAVE_FORMAT
    FILE_SAVE_FORMAT = file_save_format

    if not _file_check(cwd, force_refresh):  # First check whether the parameters have been generated or not
        _init_parameters(para_dict)  # Read parameters from specific app

        _search_buttons()  # Search buttons
        _measure_element_size()  # Measure element sizes for later use

    _run_extra_functions()  # Run any extra function if available
    _save_parameters(cwd)  # Save results
    _print_brief_report()  # Print a brief report to let user know what operations have been down


def _file_check(cwd, force_refresh):
    if force_refresh:
        return False
    global PRODUCED_PARAMETERS

    if os.path.isfile(os.path.join(cwd, ".para_temp")):
        if FILE_SAVE_FORMAT == "pickle":
            PRODUCED_PARAMETERS = pickle.load(open(os.path.join(cwd, ".para_temp"), 'rb'))
        elif FILE_SAVE_FORMAT == "json":
            with open(os.path.join(cwd, ".para_temp"), 'r') as file:
                PRODUCED_PARAMETERS = json.loads(file.read())
        else:
            raise KeyError("File saving format is not defined")
        return True
    else:
        return False


def _init_parameters(para_dict):
    global PRODUCED_PARAMETERS

    for parameter in INPUT_PARAMETERS.keys():
        if parameter not in para_dict.keys():
            raise KeyError("You need to define key '{0}' to start initialization")
        else:
            INPUT_PARAMETERS[parameter] = para_dict[parameter]


def _search_buttons():
    global PRODUCED_PARAMETERS
    global INPUT_PARAMETERS

    button_dict = INPUT_PARAMETERS["button_dict"]
    for button_name in tqdm(button_dict.keys(), ascii=True, desc="buttons"):
        PRODUCED_PARAMETERS["button_positions"][button_name] = \
            pe.search_given_picture_in_area_and_give_pos(button_dict[button_name][0],
                                                         ((0, 0), (1920, 1080)),
                                                         full_screen=True,
                                                         debug_mode=True,
                                                         debug_pic=button_dict[button_name][1])
        if PRODUCED_PARAMETERS["button_positions"][button_name] is None:
            print(""""button {0} cannot be found in the screenshot. Now please open your image editor to give the value
             manually.""".format(button_name))
            ((left, top), (right, bottom)) = \
                input("The position of button {0} is (Please in the format like ((left, top), (right, bottom)) ): ".
                      format(button_name))
            PRODUCED_PARAMETERS["button_positions"][button_name] = ((left, top), (right, bottom))


def _measure_element_size():
    global PRODUCED_PARAMETERS
    global INPUT_PARAMETERS

    element_dict = INPUT_PARAMETERS["element_size_dict"]
    for element_name in element_dict.keys():
        PRODUCED_PARAMETERS["element_sizes"][element_name] = element_dict[element_name].size


def _run_extra_functions():
    global INPUT_PARAMETERS
    if INPUT_PARAMETERS["function_list_to_implement"] is not None:
        for function in INPUT_PARAMETERS["function_list_to_implement"]:
            function()


def _save_parameters(cwd):
    global PRODUCED_PARAMETERS
    global FILE_SAVE_FORMAT

    if FILE_SAVE_FORMAT == "pickle":
        pickle.dump(PRODUCED_PARAMETERS, open(os.path.join(cwd, ".para_temp"), 'wb'))
    elif FILE_SAVE_FORMAT == "json":
        with open(os.path.join(cwd, ".para_temp"), 'w') as file:
            file.write(json.dumps(PRODUCED_PARAMETERS))
    else:
        raise KeyError("File saving format is not defined")


def _print_brief_report():
    global PRODUCED_PARAMETERS
    global INPUT_PARAMETERS

    print("===================Produced parameters involved in the init are:===================")
    for key, value in PRODUCED_PARAMETERS.items():
        print('{key}:{value}'.format(key=key, value=value))

    print("===================Input parameters involved in the init are:===================")
    for key, value in INPUT_PARAMETERS.items():
        print('{key}:{value}'.format(key=key, value=value))
