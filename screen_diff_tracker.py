import cv2
from matplotlib import pyplot as plt
import numpy as np
import pyautogui as pag
from skimage.metrics import structural_similarity


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
    img1 = np.array(img1)
    img2 = np.array(img2)

    # Convert images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = structural_similarity(img1_gray, img2_gray, full=True)
    print("Image similarity: {}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0, 1]
    # os we must convert the array to 8-bit unsigned integers in the range
    # [0, 255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img2.shape, dtype="uint8")
    filled_after = img2.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    cv2.imshow("after", img2)
    cv2.waitKey()
    return img2


diff_img = compare_images(initial_images[0], initial_images[1])
