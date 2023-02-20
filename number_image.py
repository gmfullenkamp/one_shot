import cv2
from itertools import cycle
from matplotlib import pyplot as plt
import numpy as np
import os
import scipy
from termcolor import colored
from time import sleep

# Order of number from lightest to darkest:
# 0853269147
IMG_NAME = "smile.png"
IMG_SIZE = [50, 50]

horizontal_blur = [[0.25, 0.5, 0.25],
                   [0., 0., 0.],
                   [-0.25, -0.5, -0.25]]
horizontal_blur = np.array(horizontal_blur)
vertical_blur = [[-0.25, 0., 0.25],
                 [-0.5, 0., 0.5],
                 [-0.25, -0., 0.25]]
vertical_blur = np.array(vertical_blur)

input_img = cv2.imread(IMG_NAME)
gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
small_img = cv2.resize(gray_img, IMG_SIZE)
horizontal_img = abs(scipy.signal.convolve2d(small_img, horizontal_blur))
vertical_img = abs(scipy.signal.convolve2d(small_img, vertical_blur))
both_img = (horizontal_img + vertical_img) / 255.0  # 0 - 2.0 scale

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex="all", sharey="all")
ax1.set_title("Horizontal")
ax1.imshow(horizontal_img, cmap="gray")
ax2.set_title("Vertical")
ax2.imshow(vertical_img, cmap="gray")
ax3.set_title("Both")
ax3.imshow(both_img, cmap="gray")
# plt.show()


def print_binary_image(img: np.array) -> None:
    """Expects an image array with 2 dimensions on a scale from 0. to 2."""
    for row in img:
        for col in row:
            if col > 0.5:
                print("000", end="")
            else:
                print("111", end="")
        print(end="\n")


for _ in range(5):  # TODO: Make his work for a video, or single input image
    print_binary_image(both_img)
    sleep(1)
os.system("cls")  # Command specific for windows
