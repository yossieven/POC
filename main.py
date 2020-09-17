# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2

import numpy as np


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    image = cv2.imread('generators/test_open_search_not_found.png')
    image2 = cv2.imread('generators/test_voice_search_no_mic.png')
    cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    error = mse(image, image2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
