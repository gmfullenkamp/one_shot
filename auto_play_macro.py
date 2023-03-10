import json
import pyautogui as pag
from tqdm import tqdm

input_filename = "auto_btd6.json"

screen_width, screen_height = pag.size()

f = open(input_filename)
actions = json.load(f)
f.close()

width_ratios, height_ratios, times = actions["width_ratios"], actions["height_ratios"], actions["times"]
count = 1
while True:
    print(f"Starting loop {count}...")
    prev_s = 0
    for x_ratio, y_ratio, s in tqdm(zip(width_ratios, height_ratios, times)):
        pag.moveTo(screen_width * x_ratio, screen_height * y_ratio, duration=s - prev_s)
        pag.click()
        prev_s = s
    count += 1
