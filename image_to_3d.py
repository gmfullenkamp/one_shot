"""
Vertical blur kernel for a 2d convolution on images.
The output is then turned into red and blue lines (positive and negative values).
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np
import scipy

IMG_NAME = "smile.png"

blur = [[0.25, 0., -0.25],
        [0.5, 0., -0.5],
        [0.25, 0., -0.25]]
blur = np.array(blur)


def pn_2_rb(in_img: np.array) -> np.array:
    """Positive and negatives turn into red and blue pixels respectively."""
    shp = list(in_img.shape)
    rb_img = np.zeros(shp + [3])
    for r in range(shp[0]):
        for c in range(shp[1]):
            if in_img[r][c] > 1:
                rb_img[r][c] = [0., 230., 255.]  # Turns positives into red
            elif in_img[r][c] < -1:
                rb_img[r][c] = [255., 0., 255.]  # Turns negatives into blue
    return rb_img


input_img = cv2.imread(IMG_NAME)
gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
conv_img = scipy.signal.convolve2d(gray_img, blur)
holo_img = pn_2_rb(conv_img)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex="all", sharey="all")
ax1.set_title("Input")
ax1.imshow(input_img, cmap="brg")
ax2.set_title("Gray")
ax2.imshow(gray_img, cmap="gray")
ax3.set_title("Conv")
ax3.imshow(conv_img, cmap="gray")
ax4.set_title("Holo")
ax4.imshow(holo_img, cmap="brg")
plt.show()

cv2.imwrite("holo_" + IMG_NAME, holo_img)
