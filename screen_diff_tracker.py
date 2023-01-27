import cv2
from matplotlib import pyplot as plt
import numpy as np
import pyautogui as pag


TIME_BETWEEN = 5


# Gets the number of images that will be watched
num_images = int(input("Input the number of screenshots you will be watching: "))
initial_images = []


# Prompts the user to get the screenshots of the initial correct images
for i in range(num_images):
    input("Press enter to take a screen shot for image {}.".format(i + 1))
    initial_images.append(pag.screenshot())

# Plots the initial images to show the user
fig, axs = plt.subplots(num_images)
for ax, im in zip(axs, initial_images):
    ax.imshow(im)
    ax.set_xticks(ticks=[], color='w')
    ax.set_yticks(ticks=[], color='w')
plt.show()


def compare_images(img1: np.array, img2: np.array) -> np.array:
    """Compares two images and returns an image with white pixels for the differences."""
    # https://stackoverflow.com/questions/56183201/detect-and-visualize-differences-between-two-images-with-opencv-python
    # Convert images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray
    return diff_img
