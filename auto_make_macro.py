import json
import pyautogui as pag
from pynput import mouse
import time

output_filename = "auto_btd6.json"

start_time = time.time()
actions = {"width_ratios": [], "height_ratios": [], "times": []}
screen_width, screen_height = pag.size()


def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed is True:  # When left mouse click (track)
        s = time.time() - start_time
        print(f"left mouse pressed at ({x / screen_width}, {y / screen_height}, {s})")
        actions["width_ratios"].append(x / screen_width)
        actions["height_ratios"].append(y / screen_height)
        actions["times"].append(s)
    # TODO: Add another dict field for button pressed (left or right) and change this to be a specific hotkey or smthn
    if button == mouse.Button.right and pressed is True:  # When right mouse click (save data)
        json_object = json.dumps(actions)
        print("Saving locations so far...")
        with open(output_filename, 'w') as f:
            f.write(json_object)


listener = mouse.Listener(on_click=on_click)
listener.start()
listener.join()
