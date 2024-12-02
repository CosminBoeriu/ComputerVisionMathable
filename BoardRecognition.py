import math
from basics import *
import TileRecognition

width = 1000
height = 1000

def get_playing_board(image, original_image):
    """
    Determine the playing area of the board.

    Args:
        image (numpyArray): Grayscale transformed original image.
        original_image (numpyArray): The original image, same size as image.
    Returns:
        numpyArray: The original playing board, with the background removed.
    Raises:
        None
    """
    # Making sure the image is GrayScaled
    if len(image.shape) == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a threshold to make a binary image - everything below 60 is black
    #show_image(image)
    _, threshold_img = cv.threshold(image, 60, 255, cv.THRESH_BINARY)
    #show_image(threshold_img)
    top_left, top_right, bottom_left, bottom_right = define_contours(threshold_img)

    puzzle = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
    destination_of_puzzle = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv.getPerspectiveTransform(puzzle, destination_of_puzzle)

    result = cv.warpPerspective(original_image, M, (width, height))
    #show_image(result)
    return result

def define_contours(image):
    """
    Calculates the corners of the playing area of the board.
    Called inside get_playing_board.

    Args:
        image (numpyArray): Binary image of the edges of the board, transformed with Canny.
    Returns:
        coordinates (tuple of 4 points): top_left, top_right, bottom_left, bottom_right
    Raises:
        None
    """
    _, black_and_white = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(black_and_white,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for i in range(len(contours)):
        if len(contours[i]) > 3:
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + \
                        possible_bottom_right[1]:
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis=1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left], [possible_top_right], [possible_bottom_right],
                                        [possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array(
                    [[possible_top_left], [possible_top_right], [possible_bottom_right], [possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    image_copy = cv.cvtColor(image.copy(), cv.COLOR_GRAY2BGR)
    cv.circle(image_copy, tuple(top_left), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(top_right), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(bottom_left), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(bottom_right), 20, (0, 0, 255), -1)
    image_copy = cv.resize(image_copy, (width, height))

    return top_left, top_right, bottom_left, bottom_right

def merge_lines(lines, rho_threshold=10, theta_threshold=np.pi / 90):
    merged_lines = []
    for line in lines:
        rho, theta = line[0]  # Extract rho and theta
        found_similar = False
        for i, (mrho, mtheta) in enumerate(merged_lines):
            # Check if current line is close to any merged line
            if abs(rho - mrho) < rho_threshold and abs(theta - mtheta) < theta_threshold:
                # Average the values to merge
                merged_lines[i] = ((rho + mrho) / 2, (theta + mtheta) / 2)
                found_similar = True
                break
        if not found_similar:
            merged_lines.append((rho, theta))  # Add as a new line
    return merged_lines

def extract_lines(lines):
    horizontal_lines = []
    vertical_lines = []
    for line in lines:
        rho, theta = line
        if theta - 0.0001 < 0:
            vertical_lines.append(rho)
        else:
            horizontal_lines.append(rho)
    vertical_lines.sort()
    horizontal_lines.sort()
    return horizontal_lines, vertical_lines

def plot_lines(image, lines):
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0]
            theta = lines[i][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 2000 * (-b)), int(y0 + 2000 * (a)))
            pt2 = (int(x0 - 2000 * (-b)), int(y0 - 2000 * (a)))
            cv.line(image, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
    #show_image(image)

def recognize_tile_edges(image, original_image):
    lines = cv.HoughLines(image, 1, np.pi / 2, 120, None, 0, 0)
    lines = merge_lines(lines)
    plot_lines(original_image, lines)
    horizontal_lines, vertical_lines = extract_lines(lines)
    return horizontal_lines, vertical_lines

def recognize_tile(image, original_image):
    #image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = image[:, :, 2]
    #image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #show_image(image)
    _, threshold_img = cv.threshold(image, 150, 255, cv.THRESH_BINARY)
    image = erode_image(threshold_img, kernel_size=9)
    image = dilate_image(image, kernel_size=9)
    edges = cv.Canny(image, 200, 400)
    return recognize_tile_edges(edges, original_image)


def recognize_board(image):
    image = cv.resize(image, (2000, 2000))
    original_image = image.copy()
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(image)
    playing_board = get_playing_board(h, original_image)
    return playing_board

def recognize_board_and_red_edges(image):
    playing_board = recognize_board(image)
    original_image = playing_board.copy()
    return recognize_tile(playing_board, original_image)