from matplotlib import pyplot as plt
import pyautogui as pag


TIME_BETWEEN = 5


initial_images = [[0, 0, 0], [0, 0, 0]]


# Prompts the user to get the screenshots of the initial correct images
for r in range(2):
    for c in range(3):
        input("Is the screen ready for screenshot (y or n)?\n")
        initial_images[r][c] = pag.screenshot()

# Plots the initial images to show the user
fig, axs = plt.subplots(2, 3)
for ax1, im1 in zip(axs, initial_images):
    for ax2, im2 in zip(ax1, im1):
        ax2.imshow(im2)
        ax2.set_xticks(ticks=[0], color='w')
        ax2.set_yticks(ticks=[0], color='w')
plt.show()
