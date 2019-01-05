import importlib

import base_methods.actions_based_on_pywin32 as ac
import base_methods.perceptions_based_on_pywin32 as pe
import base_methods.core as core

import os
import pickle
from tqdm import tqdm
import json
from PIL import Image

NECESSARY_PARAMETERS = {
    "button_dict": None, # form in {"button_name": (button_picture_in_PIL_IMAGE_form, pictures_used_to_search_in_PIL_IMAGE_form)}
    "function_list_to_implement": None,  # the functions need to be run after initialization
    "element_size_dict": None,  # form in {"element_name": element_picture_in_PIL_IMAGE_form}
}

PRODUCED_PARAMETERS = {
    "button_positions": {},
    "element_sizes": {},
}

CUSTOM_PARAMETERS = {

}


# Register for extra functions input/output parameters
FUNCTION_INPUT_PARAMETER = {
    "NECESSARY_PARAMETERS": NECESSARY_PARAMETERS,
    "PRODUCED_PARAMETERS": PRODUCED_PARAMETERS,
    "CUSTOM_PARAMETERS": CUSTOM_PARAMETERS,
}

FUNCTION_OUTPUT_PARAMETER = {
    "NECESSARY_PARAMETERS": NECESSARY_PARAMETERS,
    "PRODUCED_PARAMETERS": PRODUCED_PARAMETERS,
    "CUSTOM_PARAMETERS": CUSTOM_PARAMETERS,
}

FILE_SAVE_FORMAT = None


# TODO Screen resolution checker


def init_parameters(para_dict, cwd_name, working_folder, force_refresh=False, file_save_format="json",
                    pic_path="pics", button_path="buttons", element_path="elements", compared_pic_path="be_compared"):
    # Init
    cwd = working_folder
    initializers_to_be_executed = []

    while os.path.basename(cwd) != cwd_name:
        initializers_to_be_executed.append(cwd)
        cwd = os.path.dirname(cwd)
    initializers_to_be_executed.append(cwd)
    initializers_to_be_executed.reverse()
    initializers_to_be_executed.pop()
    cwd = working_folder

    for initializer in initializers_to_be_executed:
        initializer = os.path.join(initializer, "initializer.py")
        print("executing file: ", initializer)
        os.system("python " + initializer)

    global FILE_SAVE_FORMAT
    FILE_SAVE_FORMAT = file_save_format

    # Start
    if not _file_check(cwd, force_refresh):  # First check whether the parameters have been generated or not
        _init_parameters(para_dict)  # Read parameters from specific app

        _search_button_pics(working_folder, pic_path, button_path, compared_pic_path)  # Add button pictures from set folder
        _search_element_pics(working_folder, pic_path, element_path)  # Add element pictures from set folder

        _search_buttons()  # Search buttons
        _measure_element_size()  # Measure element sizes for later use
    else:
        print("*******Reading Mode*******")

    _run_extra_functions()  # Run any extra function if available
    _save_parameters(cwd)  # Save results
    _print_brief_report()  # Print a brief report to let user know what operations have been down

    # For readability
    print()
    print()


def read_parameters():
    pass


def _file_check(cwd, force_refresh):
    if force_refresh:
        return False
    global PRODUCED_PARAMETERS
    global CUSTOM_PARAMETERS

    if os.path.isfile(os.path.join(cwd, ".para_temp")):
        if FILE_SAVE_FORMAT == "pickle":
            (PRODUCED_PARAMETERS, CUSTOM_PARAMETERS) = pickle.load(open(os.path.join(cwd, ".para_temp"), 'rb'))
        elif FILE_SAVE_FORMAT == "json":
            with open(os.path.join(cwd, ".para_temp"), 'r') as file:
                (PRODUCED_PARAMETERS, CUSTOM_PARAMETERS) = json.loads(file.read())
        else:
            raise KeyError("File saving format is not defined")
        return True
    else:
        return False


def _init_parameters(para_dict):
    global PRODUCED_PARAMETERS
    global NECESSARY_PARAMETERS
    global CUSTOM_PARAMETERS

    for parameter in NECESSARY_PARAMETERS.keys():
        if parameter not in para_dict.keys():
            raise KeyError("You need to define key '{0}' to start initialization".format(parameter))

    for parameter in para_dict.keys():
        if parameter in NECESSARY_PARAMETERS.keys():
            NECESSARY_PARAMETERS[parameter] = para_dict[parameter]
        else:
            CUSTOM_PARAMETERS[parameter] = para_dict[parameter]


def _search_button_pics(working_folder, pic_path, button_path, compared_pic_path):
    button_pics_path = os.path.join(working_folder, pic_path, button_path)
    compared_pics_path = os.path.join(working_folder, pic_path, compared_pic_path)

    if not os.path.exists(button_pics_path):
        raise FileNotFoundError("The button picture folder is not found.")
    if not os.path.exists(compared_pics_path):
        raise FileNotFoundError("The reference picture folder is not found.")

    buttons = []
    compared_pics = []

    for button in os.listdir(button_pics_path):
        if os.path.isfile(os.path.join(button_pics_path, button)):
            buttons.append(button)
    for compared_pic in os.listdir(compared_pics_path):
        if os.path.isfile(os.path.join(compared_pics_path, compared_pic)):
            compared_pics.append(compared_pic)

    if buttons != compared_pics:
        raise RuntimeError("Button pictures and reference pictures are not match")

    global NECESSARY_PARAMETERS
    for i in range(len(buttons)):
        button = buttons[i]
        ref = compared_pics[i]
        NECESSARY_PARAMETERS["button_dict"][button[:button.find(".")]] = \
            (Image.open(os.path.join(button_pics_path, button)),
             Image.open(os.path.join(compared_pics_path, ref)))


def _search_element_pics(working_folder, pic_path, element_path):
    element_pics_path = os.path.join(working_folder, pic_path, element_path)

    if not os.path.exists(element_pics_path):
        raise FileNotFoundError("The element picture folder is not found.")

    elements = []

    for element in os.listdir(element_pics_path):
        if os.path.isfile(os.path.join(element_pics_path, element)):
            elements.append(element)

    global NECESSARY_PARAMETERS
    for element in elements:
        NECESSARY_PARAMETERS["element_size_dict"][element[:element.find(".")]] = \
            Image.open(os.path.join(element_pics_path, element))


def _search_buttons():
    global PRODUCED_PARAMETERS
    global NECESSARY_PARAMETERS

    button_dict = NECESSARY_PARAMETERS["button_dict"]
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
    global NECESSARY_PARAMETERS

    element_dict = NECESSARY_PARAMETERS["element_size_dict"]
    for element_name in element_dict.keys():
        PRODUCED_PARAMETERS["element_sizes"][element_name] = element_dict[element_name].size


def _run_extra_functions():
    global NECESSARY_PARAMETERS
    global FUNCTION_OUTPUT_PARAMETER
    global FUNCTION_INPUT_PARAMETER

    if NECESSARY_PARAMETERS["function_list_to_implement"] is not None:
        for function in NECESSARY_PARAMETERS["function_list_to_implement"]:
            FUNCTION_OUTPUT_PARAMETER = function(FUNCTION_INPUT_PARAMETER)


def _save_parameters(cwd):
    global PRODUCED_PARAMETERS
    global FILE_SAVE_FORMAT
    global CUSTOM_PARAMETERS

    if FILE_SAVE_FORMAT == "pickle":
        pickle.dump((PRODUCED_PARAMETERS, CUSTOM_PARAMETERS), open(os.path.join(cwd, ".para_temp"), 'wb'))
    elif FILE_SAVE_FORMAT == "json":
        with open(os.path.join(cwd, ".para_temp"), 'w') as file:
            file.write(json.dumps((PRODUCED_PARAMETERS, CUSTOM_PARAMETERS)))
    else:
        raise KeyError("File saving format is not defined")


def _print_brief_report():
    global PRODUCED_PARAMETERS
    global NECESSARY_PARAMETERS
    global CUSTOM_PARAMETERS

    print("===================Produced parameters involved in the init are:===================")
    for key, value in PRODUCED_PARAMETERS.items():
        print('{key}:{value}'.format(key=key, value=value))

    print("===================Customized parameters involved in the init are:===================")
    for key, value in CUSTOM_PARAMETERS.items():
        print('{key}:{value}'.format(key=key, value=value))

    print("===================Input parameters involved in the init are:===================")
    for key, value in NECESSARY_PARAMETERS.items():
        print('{key}:{value}'.format(key=key, value=value))
