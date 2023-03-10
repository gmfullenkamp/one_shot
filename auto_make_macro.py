import json
from pynput import mouse
import time

output_filename = "auto_btd5.json"

start_time = time.time()
actions = {"widths": [], "heights": [], "times": []}


# TODO: Later have it save screen ratios instead of specific pixel values
def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed is True:  # When left mouse click (track)
        s = time.time() - start_time
        print(f"left mouse pressed at ({x}, {y}, {s})")
        actions["widths"].append(x)
        actions["heights"].append(y)
        actions["times"].append(s)
    if button == mouse.Button.right and pressed is True:  # When right mouse click (save data)
        json_object = json.dumps(actions)
        with open(output_filename, 'w') as f:
            f.write(json_object)


listener = mouse.Listener(on_click=on_click)
listener.start()
listener.join()
