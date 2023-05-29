import json
import pyautogui as pag
from pynput import mouse
import time

output_filename = "auto_coromon.json"

start_time = time.time()
actions = {"type": [], "x_ratios": [], "y_ratios": [], "times": []}
screen_width, screen_height = pag.size()


def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed is True:
        s = time.time() - start_time
        print(f"left mouse clicked at ({x / screen_width}, {y / screen_height}, {s})")
        actions["type"].append("mouse_clicked")
        actions["x_ratios"].append(x / screen_width)
        actions["y_ratios"].append(y / screen_height)
        actions["times"].append(s)
    elif button == mouse.Button.left and pressed is False:
        s = time.time() - start_time
        print(f"left mouse released at ({x / screen_width}, {y / screen_height}, {s})")
        actions["type"].append("mouse_released")
        actions["x_ratios"].append(x / screen_width)
        actions["y_ratios"].append(y / screen_height)
        actions["times"].append(s)
    elif button == mouse.Button.right and pressed is True:
        json_object = json.dumps(actions)
        print("Saving actions so far...")
        with open(output_filename, 'w') as f:
            f.write(json_object)


with mouse.Listener(on_click=on_click) as mouse_listener:
    mouse_listener.join()
