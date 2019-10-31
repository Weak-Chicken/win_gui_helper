from chrome_game_player.translator import *

hwndMain = win32gui.FindWindow(None, "chrome://dino/ - Google Chrome")
win32gui.SetForegroundWindow(hwndMain)
time.sleep(0.1)

night_flag = False

#
# original_image = grab_detecting_area()
# image = divide_pictures(original_image, (30, 30))

# feature_matrix = np.array([])

# while True:
#     # print(win32api.GetKeyState(VK_CODE["a"])) # 0 or 1 is up. -128 or -127 is down
#     if win32api.GetKeyState(VK_CODE["spacebar"]) == -128 or win32api.GetKeyState(VK_CODE["spacebar"]) == -127:
#         break
#     time.sleep(0.1)

# while True:
#     if win32api.GetKeyState(VK_CODE["esc"]) == -128 or win32api.GetKeyState(VK_CODE["esc"]) == -127:
#         break
#     else:
#         detect_area = grab_detecting_area()
#         processed_detect_area = divide_pictures(detect_area, (30, 30))
#         detecting = []
#         for array in processed_detect_area:
#             detecting.append(gh.support_functions.array_pooling(array, (30, 30), (0, 0), "avg_pooling"))
#         if np.mean(np.array(detecting)) <= 240:
#             jump()
timer = []

while True:
    if win32api.GetKeyState(VK_CODE["esc"]) == -128 or win32api.GetKeyState(VK_CODE["esc"]) == -127:
        break
    else:
        start_time = time.time()
        detect_area, night_area = optimise_grab_func(FullScreenPara().detect_area, FullScreenPara().BACK_GROUND)
        night = gh.support_functions.array_pooling(np.array(night_area), (5, 5), (0, 0), "max_pooling")
        detect = gh.support_functions.array_pooling(np.array(detect_area), (137, 300), (0, 0), "avg_pooling")
        if int(night) == 255:
            night = False
        else:
            night = True
        if not night:
            if int(detect) <= 240:
                jump()
        else:
            if int(detect) >= 240:
                jump()
        timer.append(time.time() - start_time)

print(len(timer), np.mean(np.array(timer)))