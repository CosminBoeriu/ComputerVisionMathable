import cv2 as cv
import numpy as np
import os

NUMBERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 24, 25, 27, 28, 30, 32, 35, 36, 40, 42, 45, 48, 49, 50, 54, 56, 60, 63, 64,
           70, 72, 80, 81, 90)

INITIAL_BOARD = (
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1,  1,  2, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1,  3,  4, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
                    (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)
                )

MULTIPLIER_BOARD = (
                    (3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3),
                    (1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
                    (1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1),
                    (1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1),
                    (1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1),
                    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3),
                    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3),
                    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                    (1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1),
                    (1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1),
                    (1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1),
                    (1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
                    (3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3)
                   )

SIGN_BOARD = (
                ('', '', '', '', '', '', '', '', '', '', '', '', '', ''),
                ('', '', '', '', '/', '', '', '', '', '/', '', '', '', ''),
                ('', '', '', '', '', '-', '', '', '-', '', '', '', '', ''),
                ('', '', '', '', '', '', '+', '*', '', '', '', '', '', ''),
                ('', '/', '', '', '', '', '*', '+', '', '', '', '', '/', ''),
                ('', '', '-', '', '', '', '', '', '', '', '', '-', '', ''),
                ('', '', '', '*', '+', '', '', '', '', '*', '+', '', '', ''),
                ('', '', '', '+', '*', '', '', '', '', '+', '*', '', '', ''),
                ('', '', '-', '', '', '', '', '', '', '', '', '-', '', ''),
                ('', '/', '', '', '', '', '+', '*', '', '', '', '', '/', ''),
                ('', '', '', '', '', '', '*', '+', '', '', '', '', '', ''),
                ('', '', '', '', '', '-', '', '', '-', '', '', '', '', ''),
                ('', '', '', '', '/', '', '', '', '', '/', '', '', '', ''),
                ('', '', '', '', '', '', '', '', '', '', '', '', '', ''),
             )

def load_digits():
    Digits = {x: '' for x in NUMBERS}
    PATH = './Data/modele_cifre/'
    image_names = sorted([img for img in os.listdir(PATH) if '.jpg' in img])
    for name in image_names:
        padding = 0
        # Pad the image with white pixels
        white_color = [255, 255, 255]  # White in BGR
        digit = cv.imread(PATH+name)
        # _, digit = cv.threshold(digit, 60, 255, cv.THRESH_BINARY)
        padded_image = cv.copyMakeBorder(digit, top=padding, bottom=padding, left=padding,
                                        right=padding, borderType=cv.BORDER_CONSTANT,
                                        value=white_color)
        padded_image = cv.cvtColor(padded_image, cv.COLOR_BGR2GRAY)
        Digits[int(name[:-4])] = padded_image
    return Digits
DIGITS = load_digits()


def show_image(image, title='', resize=True):
    if resize:
        image = cv.resize(image, (1000, 1000))
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def draw_horizontal_line(image, h):
    start_point = (0, int(h))
    end_point = (2000, int(h))
    cv.line(image, start_point, end_point, color=(0, 0, 255), thickness=3)
    return image

def draw_vertical_line(image, v):
    start_point = (int(v), 0)
    end_point = (int(v), 2000)
    cv.line(image, start_point, end_point, color=(0, 0, 255), thickness=3)
    return image

def erode_image(image, kernel_size=9):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    image = cv.erode(image, kernel)
    return image

def dilate_image(image, kernel_size=9):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    image = cv.dilate(image, kernel)
    return image