import json
import pyautogui as pag
from tqdm import tqdm

input_filename = "auto_btd5.json"

f = open(input_filename)
actions = json.load(f)
f.close()

widths, heights, times = actions["widths"], actions["heights"], actions["times"]
count = 1
while True:
    print(f"Starting loop {count}...")
    prev_s = 0
    for x, y, s in tqdm(zip(widths, heights, times)):
        pag.moveTo(x, y, duration=s - prev_s)
        pag.click()
        prev_s = s
    count += 1
