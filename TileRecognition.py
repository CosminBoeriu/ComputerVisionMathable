import cv2
import numpy as np

from basics import *
from GameLogic import *

def recolor_playingboard(image):
    image = cv.cvtColor(image, cv.COLOR_HSV2RGB)
    h, s, v = cv.split(image)
    _, working_img = cv.threshold(h, 170, 255, cv.THRESH_BINARY)
    return working_img


def determine_cell_position(horizontal_lines, vertical_lines, diff_image):
    pixels = []
    for i in range(len(diff_image)):
        for j in range(len(diff_image[i])):
            if diff_image[i][j] != 0:
                pixels.append((i, j))
    horizontal_votes = [0] * len(horizontal_lines)
    vertical_votes = [0] * len(vertical_lines)
    for pixel in pixels:
        for index in range(len(horizontal_lines)-1):
            if horizontal_lines[index] <= pixel[0] < horizontal_lines[index+1]:
                horizontal_votes[index] += 1
        for index in range(len(vertical_lines)-1):
            if vertical_lines[index] <= pixel[1] < vertical_lines[index+1]:
                vertical_votes[index] += 1
    return horizontal_votes.index(max(horizontal_votes)), vertical_votes.index(max(vertical_votes))


def determine_number(h, v, horizontal_lines, vertical_lines, image, game_board, index):
    buff = 5
    coordinates1 = int(vertical_lines[v]), int(horizontal_lines[h])
    coordinates2 = int(vertical_lines[v+1]) + buff, int(horizontal_lines[h+1])
    piece = image[coordinates1[1]:coordinates2[1], coordinates1[0]:coordinates2[0], :]
    piece = cv.cvtColor(piece, cv2.COLOR_HLS2RGB)
    piece = cv.cvtColor(piece, cv.COLOR_RGB2GRAY)
    #show_image(piece)
    max_value = -1
    max_digit = -1
    width, height = piece.shape
    factor = 110 / width
    piece = cv.resize(piece, (int(height * factor), int(width * factor)))
    for possible_digit in get_possible_models(game_board, (h, v)):
        template = DIGITS[possible_digit]
        res = cv.matchTemplate(piece, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        res = max_val
        if res > max_value:
            max_value = res
            max_digit = possible_digit
    return max_digit
