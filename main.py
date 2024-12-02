import os
import sys
import cv2 as cv
from BoardRecognition import *
from TileRecognition import recolor_playingboard
from TileRecognition import *
from basics import show_image

os.environ["QT_QPA_PLATFORM"] = "xcb"

# Calea unde sa fie create fisierele rezultat
OUTPUT_PATH = "./352_Boeriu_George_Cosmin/"

# Calea de unde sa fie luate testele
PATH = "./Data/antrenare/"

# Cate imagini are un joc
GAME_LENGTH = 50

# Ce jocuri sa fie rulate, pot fi si pe sarite
GAMES = (1, 2, 3, 4)

# Se considera ca imaginile au formatul 1_01.jpg, 2_34.jpg etc.
IMAGE_FORMAT = ".jpg"

def ensure_directory_exists(directory_path=OUTPUT_PATH):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def load_player_turns(filename="1_"):
    f = open(PATH + filename + "turns.txt", "r")
    turns = []
    first_player = None
    for line in f:
        player, turn = line.split(" ")
        turns.append(int(turn))
        if first_player is None:
            first_player = int(player[-1])
            first_player = first_player % 2 + 1
    return turns, first_player

def load_images(filename='1_'):
    image_names = sorted([img for img in os.listdir(PATH) if IMAGE_FORMAT in img and filename in img])
    for name in image_names:
        yield cv.imread(PATH+name)


if __name__ == '__main__':
    ensure_directory_exists()

    for game in GAMES:

        background_image = cv.imread("./Data/base_table.jpg")
        horizontal_lines, vertical_lines = recognize_board_and_red_edges(background_image)

        gameboard = [list(x) for x in INITIAL_BOARD]

        previous_frame = recolor_playingboard(recognize_board(background_image))
        colums = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']

        lines = ""
        score_lines_prints = ""
        progress_index = 1

        player_turns, current_player = load_player_turns(str(game) + '_')
        last_print_index = 1
        current_score = None

        for image in load_images(str(game) + '_'):
            current_board = recognize_board(image)
            current_frame = recolor_playingboard(current_board)
            #show_image(current_frame)

            difference = current_frame - previous_frame
            img = erode_image(difference, kernel_size=3)
            img = dilate_image(img, kernel_size=2)

            #Determine position and number
            h, v = determine_cell_position(horizontal_lines, vertical_lines, img)
            number = determine_number(h, v, horizontal_lines, vertical_lines, current_board, gameboard, progress_index)

            #Prints
            f = open(f"{OUTPUT_PATH}/{game}_{progress_index:02}.txt", 'w')
            f.write(str(h+1) + colums[v] + ' ' + str(number))
            f.close()

            # Calculate score:
            if progress_index in player_turns:
                if current_score is not None:
                    score_lines_prints += 'Player' + str(current_player) + ' ' + str(last_print_index) + ' ' + str(current_score) + '\n'
                    last_print_index = progress_index
                current_player = current_player % 2 + 1
                current_score = 0
            current_score += score_calculator(gameboard, number, (h, v))

            #Update current frame
            previous_frame = current_frame
            gameboard[h][v] = number

            print(f'Game: {game}, Image: {progress_index}')
            progress_index += 1


        score_lines_prints += 'Player' + str(current_player) + ' ' + str(last_print_index) + ' ' + str(
            current_score)

        f = open(f"{OUTPUT_PATH}/{game}_scores.txt", 'w')
        f.write(score_lines_prints)
        f.close()

