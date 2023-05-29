import json

import pyautogui as pag
from tqdm import tqdm

input_filename = "auto_coromon.json"
speed_up = 1.5

screen_width, screen_height = pag.size()

f = open(input_filename)
actions = json.load(f)
f.close()

types, x_ratios, y_ratios, times = actions["type"], actions["x_ratios"], actions["y_ratios"], actions["times"]

count = 1
while True:
    print(f"Starting loop {count}...")
    prev_s = 0
    for i, (t, x, y, s) in tqdm(enumerate(zip(types, x_ratios, y_ratios, times))):
        if t == "mouse_clicked":
            mouse_clicked_x = screen_width * x
            mouse_clicked_y = screen_height * y
            pag.moveTo(mouse_clicked_x, mouse_clicked_y, duration=(s - prev_s) / speed_up)
            pag.mouseDown(button="left")
        elif t == "mouse_released":
            mouse_released_x = screen_width * x
            mouse_released_y = screen_height * y
            pag.moveTo(mouse_released_x, mouse_released_y, duration=(s - prev_s) / speed_up)
            pag.mouseUp(button="left")
        prev_s = s
    count += 1
