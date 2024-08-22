# Name: Pranav Marthi
# Date: January 25, 2023
# Course: ICS3U-01
# Description: play a fun, engaging game in which you have to click the piano tiles while gathering hints to solve the
# subsequent puzzles. There are two levels.

# Imports (pygame, math)
import pygame.draw
from pygame import *
from math import *
import os
import random
from pygame.time import get_ticks

# Pygame initialization
init()

# Setting screen size and environment settings
SIZE = (width, height) = (1000, 650)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 20)
screen = display.set_mode(SIZE)

# Environment and colour definitions used throughout the program
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GRAY = (214, 214, 214)
SELECTOR_BLUE = (0, 43, 112)

# Defining the starting position of the first tile
y_start = 500

# All available states in the gameplay experience
MAIN_MENU_STATE = 0
GAMEPLAY_STATE = 1
LEADERBOARD_STATE = 2
LOGIN_STATE = 3
INSTRUCTIONS_STATE = 4
EXIT_PROGRAM_STATE = 5
PAUSE = 6
GAME_OVER_STATE = 7
SUCCESSFUL_STATE = 8
FAILED_STATE = 9

# Text width and height initialization
text_width = 0
text_height = 0

# Loading all the images prior to gameplay
background_image = image.load("gradient.png")
cover_up = image.load('Screen Shot 2022-12-27 at 10.46.24 AM.png')
cover_up2 = image.load('Screen Shot 2022-12-27 at 10.53.25 AM.png')
cover_button1 = image.load('coverbutton1.png')
cover_button2 = image.load('coverbutton2.png')
leadership_bg = image.load('leadership_board_background.jpeg')
lock_icon = image.load('lock-icon-vector-13820047-removebg-preview.png')
e_waste5 = image.load("wasteimg5.png")
e_waste_character = image.load('ewastecharacter.png')
piano_background_image = image.load("pianobackground.jpeg").convert()
bg_img = image.load('bggame.png')
play_background_image = transform.scale(image.load("download (1).jpeg").convert(), (1000, 650))
home_button = image.load('home_icon.png')
replay_button = image.load('replay_icon.png')
diagram_img = image.load('diagram.png')
l2puzzle_background = image.load('transparent_version.png')

# Initialization of level states (whether they are unlocked or locked)
levels_unlocked = [True, False, False, False]
puzzles_unlocked = [False, False, False, False]
level_selected = -1  # Determines the rows and levels the user is currently in
row_selected = -1

# Questions and hints used throughout the program structured in two-dimensional arrays for simple and eloquent access
user_hint_categories = ["E-Waste", "Health"]
user_hint_questions = [[
    "The average cell phone user replaces their unit every 18 months.",
    "85% of our e-waste sent to landfills and incinerators is burned, and releases harmful toxins into the air",
    "300 million computers and over 1 billion cell phones are produced each year."
], [
    "Doctors recommend that for every 20 minutes you spend on a screen, look away for 20 seconds and focus your eyes "
    "on an object 20 feet away.",
    "A 2017 study of 8th to 12th graders found that high levels of depressive symptoms increased by 33% between "
    "2010 and 2015.",
    "The more time spent on social media can lead to cyberbullying, social anxiety, depression, and exposure to "
    "content that is not age appropriate."
]
]
answers_array = [
    ["18 months", "24 months", "36 months", "6 months"],
    ["85%", "90%", "20%", "43%"],
    ["1.3B", "500M", "60,000", "12B"],
    ["20-20-20", "1-2-√3", "1-1-√2", "Neither"],
    ["12%", "17%", "56%", "33%"],
    ["Diabetes", "Cyberbullying", "Stroke", "Cancer"]
]

questions_array = ['q1.png', 'q2.png', 'q3.png', "q4.png", "q5.png", "q6.png"]  # An array with all the images used
# as prompts in the hint section

final_answers = [3, 3, 3, 3, 1, 2]  # Answers for the first puzzle

# Puzzle two questions, labels and answers.
multiple_choice_labels = [
    ["Settlement", "Receiving", "Pick up", "Processing"],
    ["Sorting", "Reporting", "Processing", "Pick Up"],
    ["Hazard Removal", "Receiving", "Reporting", "Sorting"],
    ["Processing", "Sortation", "Receiving", "Waste Removal"],
]
multiple_choice_questions = [
    "What comes first in the e-waste",
    "What comes last in the e-waste",
    "What comes second in the e-waste",
    "What comes third in the e-waste"
]
multiple_choice_answers = [2, 1, 1, 1]

# Multiple choice label coordinates
answer_rect_coordinates = [  # Made for puzzle 1
    [130, 330, 330, 120],
    [130, 480, 330, 120],
    [540, 330, 330, 120],
    [540, 480, 330, 120]
]

# Variable initialization (scrolling background functionality)
scrolling_x_position = 0
scrolling_y_position = 0

# Variable initialization (playing state -- level 1)
row_determination = 1
tiles = []  # --> used in tiles generation process
row_determinant = random.randint(0, 3)
GAME_START = False
eliminate_first_tile = 0
game_score = 0
puzzle_selected = -1
hint_counter = 0
rect_selected = -1  # Used in the multiple choice quiz
answer_box = [0, 0, 0, 0]
levels = 0
question_counter = 0
character_positions = [[130, 330], [540, 330], [540, 480], [130, 480]]

# Variable initialization (leaderboard state)
username_list = []
scores_list = []

# Variable initialization (instructions state)
page_counter = 0

# Variable initialization (second level)
curr_tile = Rect(0, 0, 0, 0)
SECOND_LEVEL_START = False
hit_counter = 0  # Current number of tiles hit
loss_counter = 100  # Limit to number of tiles hit
total_loss_tolerance = 100
l2game_score = 0
puzzle2_question_counter = 0
puzzle_two_correct = 0
selector_coordinates = [[200, 350], [350, 500], [500, 650], [650, 800]]

# Variable initialization (login state)
username = ''
current_session_user_name = ''
submitted = False

# Falling image variables (e-waste in level 1)
img_x = 0
img_y = 0
spacer = 0  # Ensures that trash doesn't fall too frequently
random_img = random.randint(0, 3)
bonus_clicked = False

# High score trackers
current_session_high_score = 0

# Timer termination limits
termination_time = 10
current_time = 0
button_press_time = 0
waste_imgs = e_waste5

# Elements used in the hint screen (character position) + list of random questions and corresponding answers
character_x, character_y = 140, 340
final_list = []
random_questions_array = []

# Generates the list with the random hints
while len(random_questions_array) < 5:
    random_hint = random.randint(0, 4)

    # Always ensures that the hints that are given are not already issued
    if random_hint not in random_questions_array:
        random_questions_array.append(random_hint)
        final_list.append(final_answers[random_hint])


# Displays the scrolling piano tiles background in the main menu
def scrolling_menu_background():
    # Global variables defined and used within function scope
    global current_state, scrolling_x_position, scrolling_y_position, mx, my, button

    # Transformations to rotate the piano images to the appropriate orientation
    img_vert_flip = transform.flip(piano_background_image, False, True)

    # Left piano rotations
    img_left_rotation = transform.flip(piano_background_image, False, True)
    full_img_left_rot = transform.rotate(img_left_rotation, -270)

    # Right piano image rotations
    img_right_rotation = transform.flip(piano_background_image, False, True)
    full_img_right_rot = transform.rotate(img_right_rotation, -90)

    # Getting the relative width and height of the piano image to create endless scroll
    rel_x = scrolling_x_position % piano_background_image.get_rect().width
    rel_y = scrolling_y_position % piano_background_image.get_rect().height

    # Displaying the oriented images to the screen. Hiding part of the image to give effect that only part of the
    # image is visible.
    screen.blit(piano_background_image, (rel_x - piano_background_image.get_rect().width, 600))
    screen.blit(img_vert_flip, (rel_x - piano_background_image.get_rect().width, -500))
    screen.blit(full_img_left_rot, (-500, rel_y - piano_background_image.get_rect().height))
    screen.blit(full_img_right_rot, (950, rel_y - piano_background_image.get_rect().height))

    # If the image scrolls off the screen, a new image will be generated on the y-axis
    if rel_y > 800:
        # Creating the new images in case the original image slides off the screen
        screen.blit(full_img_left_rot, (-500, rel_y))
        screen.blit(full_img_right_rot, (600, rel_y))

    # If the image scrolls off the screen, a new image will be generated on the x-axis
    if rel_x < 1000:
        # Creating the new images in case the original image slides off the screen
        screen.blit(piano_background_image, (rel_x, 600))
        screen.blit(img_vert_flip, (rel_x, -500))

    # Scrolls the piano images continuously to the left and down. Gives treadmill effect.
    scrolling_x_position -= 5
    scrolling_y_position += 5

    # Function returns to current state
    return current_state


# Displays the text to the screen, given an input, font size, font type, colour and (x, y) coordinates of the blit
def display_text(input_str, text_font, size, colour, pos_x, pos_y):
    # Global variables used within function scope
    global current_state, mx, my, button

    # Loads fonts, renders and blits to the screen
    text_font = font.Font(text_font, size)
    text = text_font.render(input_str, False, colour)
    screen.blit(text, (pos_x, pos_y))


# Centers text given an input, font type, size, and the region bounding the text (in which region should the text be
# centered)
def center_region(input_length, font_type, font_size, x_start, x_end, y_start, y_end):
    # Global variables used within function scope
    global text_width, text_height

    # The user's input is the length of the input itself
    input_length = len(input_length)

    # Depending on the font, the width and height scales differently (used linear scaling to determine the appropriate
    # scale effect.
    if font_type == '3-DSalter Regular.ttf':

        # Font scales linearly
        text_width = ((font_size * 0.35) + 11) * input_length
        text_height = ((font_size * 0.5) + 40)

    # If the font is different...
    elif font_type == 'LoveGlitchPersonalUseRegular-vmEyA.ttf':

        # Font scales linearly
        text_width = ((font_size * 0.5) - 8) * input_length - (0.95 * font_size - 14)
        text_height = ((font_size * 0.675) - 11)

    # Centers the font in the given region (x-axis)
    total_length = x_end - x_start - text_width
    start_margin = total_length / 2
    final_x_pos = x_start + start_margin

    # Centers the font in the given region (y-axis)
    total_height_length = y_end - y_start - text_height
    y_start_margin = total_height_length / 2
    final_y_pos = y_start + y_start_margin

    # Returns the (x,y) of where the text should be placed to be centered in the region.
    return final_x_pos, final_y_pos


# Function to display the back button to the user
def back_button(mx, my, current_state, color):
    # Distance from the back button
    dist_from_backb = sqrt((50 - mx) ** 2 + (50 - my) ** 2)

    # Draws the back button given a color
    draw.circle(screen, color, (50, 50), 20)

    # Detects if the back button is being hovered
    if dist_from_backb < 20:

        # Detects back button click
        if button == 1:
            current_state = MAIN_MENU_STATE

    # Creates contrast between back button and circle
    if color == WHITE:

        # Black button
        display_text("<", None, 50, BLACK, 40, 30)

    # Case that background is black
    else:

        # White button
        display_text("<", None, 50, WHITE, 40, 30)

    # Function returns updated state
    return current_state


# Draws the menu of the game given mouse position and auxiliary information on state and mouse
def drawMenu(mx, my, button, current_state):

    # Global variables used within the function scope
    global y_start, GAME_START, tiles, level_selected, page_counter, question_counter, puzzle_selected, \
        hit_counter, loss_counter, puzzle2_question_counter, puzzle_two_correct, eliminate_first_tile

    # Resetting the variables changed throughout the levels' selection (user can play the game multiple times)
    level_selected = -1
    y_start = 500
    page_counter = 0
    GAME_START = False
    tiles = []
    question_counter = 0
    puzzle_selected = -1
    puzzle2_question_counter = 0
    puzzle_two_correct = 0
    eliminate_first_tile = 0
    hit_counter = 0
    loss_counter = 100

    # Title (used the centering function described previously)
    x_title, y_title = center_region("E-WASTE TILES", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 100, 0, 1000, 0, 250)
    display_text("E-WASTE TILES", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 100, BLACK, x_title, y_title)

    # Used the centering function to ensure labels are within the label box
    sub_heading1x, sub_heading1y = center_region("INSTRUCTIONS", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, 600, 900,
                                                 220, 350)
    sub_heading2x, sub_heading2y = center_region("QUIT", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, 600, 900,
                                                 390, 510)
    sub_heading3x, sub_heading3y = center_region("LEADERBOARD", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, 0, 400,
                                                 220, 350)
    sub_heading4x, sub_heading4y = center_region("LOGIN", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, 0, 400,
                                                 390, 510)

    # All the labels, and their corresponding coordinates
    labels = ["INSTRUCTIONS", "QUIT", "LEADERBOARD", "LOGIN"]
    subheadingX = [sub_heading1x, sub_heading2x, sub_heading3x, sub_heading4x]
    subheadingY = [sub_heading1y, sub_heading2y, sub_heading3y, sub_heading4y]

    # Draws play button outline
    draw.circle(screen, BLACK, (500, 380), 170, 3)

    # Draws rectangles for each of the menu options (objects + actual drawing)
    instructions_rect = Rect(600, 250, 300, 100)
    quit_rect = Rect(600, 410, 300, 100)
    leader_rect = Rect(100, 250, 300, 100)
    login_rect = Rect(100, 410, 300, 100)
    draw.rect(screen, BLACK, instructions_rect, 3, border_radius=10)
    draw.rect(screen, BLACK, quit_rect, 3, border_radius=10)
    draw.rect(screen, BLACK, leader_rect, 3, border_radius=10)
    draw.rect(screen, BLACK, login_rect, 3, border_radius=10)

    # Used a multitude of cover-ups to hide the outline of the circle border. This gives a uniform, organized menu page.
    screen.blit(transform.scale(cover_up, (220, 350)), (390, 210))
    screen.blit(transform.scale(cover_up2, (800, 60)), (100, 350))
    screen.blit(transform.scale(cover_button1, (13, 15)), (650, 340))
    screen.blit(transform.scale(cover_button2, (13, 15)), (337, 340))
    screen.blit(transform.scale(cover_button1, (13, 15)), (650, 400))
    screen.blit(transform.scale(cover_button2, (13, 15)), (337, 400))

    # Draws circles for the play button + the play icon triangle
    draw.circle(screen, WHITE, (500, 380), 155)
    draw.circle(screen, BLACK, (500, 380), 155, 2)
    draw.circle(screen, BLACK, (500, 380), 130, 2)
    draw.polygon(screen, BLACK, [(465, 300), (465, 450), (565, 375)])

    # Calls the scrolling piano tiles function
    scrolling_menu_background()

    # If the mouse is clicked
    if button == 1:

        # Calculates distance from the center of the play button to determine whether it is clicked
        dist = sqrt((500 - mx) ** 2 + (300 - my) ** 2)

        # If the previously determined distance is less than the radius...
        if dist < 155:

            # Create tiles for the gameplay and switch states
            tiles = create_tile(mx, my, button, current_state)
            current_state = GAMEPLAY_STATE

        # If the instructions are selected...
        elif instructions_rect.collidepoint(mx, my):

            # Determine states
            current_state = INSTRUCTIONS_STATE

        # If the instructions are selected...
        elif quit_rect.collidepoint(mx, my):

            # Determine states
            current_state = QUIT

        # If the leaderboard screen is selected...
        elif leader_rect.collidepoint(mx, my):

            # Determine states
            current_state = LEADERBOARD_STATE

        # If the login screen is selected...
        elif login_rect.collidepoint(mx, my):

            # Determine states
            current_state = LOGIN_STATE

    # Displays the labels using the linked lists, as described previously
    for i in range(4):
        display_text(labels[i], 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, BLACK, subheadingX[i], subheadingY[i])

    # Function returns
    return current_state


# Function to sort the two-dimensional array in the leaderboard (bubble sort)
def sort_leaderboard_scores(sub_li):

    # Gets length
    l = len(sub_li)

    # For each array in the list
    for i in range(0, l):

        # Iterate through each element (reduce time complexity by subtract i along with it)
        for j in range(0, l - i - 1):

            # Sort the list and see if one element is greater than the one beside it
            if sub_li[j][1] > sub_li[j + 1][1]:

                # Swap the elements
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo

    # Return the list sorted by the second element in each array of the two-dimensional list
    return sub_li


# Draw the leaderboard page using the mouse input and the current state of the game
def drawLeader(mx, my, button, current_state):
    # Global variable definitions used in the function scope
    global GAME_START, username_list, score_list, data_list, final

    # Initializing the username list and scores list
    username_list = []
    scores_list = []
    final = []
    total_record = 0

    # Sets the transparency of the leaderboard page background
    leadership_bg.convert_alpha().set_alpha(1000)
    screen.blit(transform.scale(leadership_bg, (1000, 650)), (0, 0))

    # All the leaderboard organizational structures and labels
    display_text("Place", None, 60, BLACK, 230, 100)
    display_text("Username", None, 60, BLACK, 380, 100)
    display_text("Score", None, 60, BLACK, 620, 100)
    draw.line(screen, BLACK, (600, 80), (600, 550), width=5)
    draw.line(screen, BLACK, (360, 80), (360, 550), width=5)
    draw.line(screen, BLACK, (230, 150), (740, 150), width=5)

    # Draws the back button
    back_button(mx, my, current_state, WHITE)

    # Opens the scores file in read mode
    scores_file = open("lv1highscores.txt", "r")

    # Reads through the file
    while True:

        # Gets the text from the file in lines
        text = scores_file.readline()
        text = text.rstrip("\n")

        # Breaks the program if the file is empty
        if text == "":
            break

        # Arrifies data
        values = text.split(",")

        # Appends data to appropriate lists and increments number of values in file
        username_list.append(values[0])
        final.append([values[0], int(values[1])])
        total_record += 1

    final = sort_leaderboard_scores(final)[::-1]

    # Closes file
    scores_file.close()

    # Sort the scores list inverse (highest to lowest)
    scores_list.sort(reverse=True)

    # For each record
    for i in range(1, total_record + 1):

        if i <= 8:
            # Display the information
            display_text(str(i), None, 50, BLACK, 270, 140 + 50 * i)
            display_text("@" + final[i - 1][0], None, 50, BLACK, 380, 140 + 50 * i)
            display_text(str(final[i - 1][1]), None, 50, BLACK, 630, 140 + 50 * i)

    # Sets the current state to the state of the back button
    current_state = back_button(mx, my, current_state, BLACK)

    # Function returns current state to the main loop
    return current_state


# Draws the start button
def startButton(position):
    # Given the position, it will draw the start button
    draw.rect(screen, BLACK, position)


# Creates tiles for use within the levels in the game
def create_tile(mx, my, button, current_statem):
    # Global variable definitions
    global row_determinant

    # If it's the first tile
    if len(tiles) < 1:
        # Default to appending a 150x150 tile to a random column
        tiles.append([row_determination * 150 + 202, 500, 150, 150])

    # Always maintain a list of 5 tiles (once they are popped off, this function will regenerate tiles)
    while len(tiles) < 5:

        # Determines the column in which the tiles would fall + the height of the individual tiles
        row_determinant = random.randint(0, 3)
        random_tile_height = random.randint(200, 350)

        # Append this new data to the tiles array
        tiles.append([200 + 150 * row_determinant + 2, 0, 150, random_tile_height])

        # Ensures that no more than two successive tiles fall in the same column
        for tile in range(len(tiles) - 1):

            # Ensure the next tile is at the y-coordinate of the previous tile
            tiles[tile + 1][1] = tiles[tile][1] - tiles[tile + 1][3]

            # If the tiles are in the same column
            while tiles[tile + 1][0] == tiles[tile][0]:
                # Keep changing the row to avoid repetition
                row_determinant = random.randint(0, 3)

                # Reset the value of the tile's x position
                tiles[tile][0] = 200 + 150 * row_determinant + 2

    # Returns the tiles list of the coordinates the tiles to the playing state
    return tiles


# Draws the level screen given mouse and current state information
def levels_screen(mx, my, button, current_state):
    # Global variable definitions used throughout function scope
    global level_selected, game_score, tiles, puzzle_selected, l2game_score, SECOND_LEVEL_START, puzzle2_question_counter

    # Reset colour of screen
    screen.fill(BLACK)

    # Calculations to ensure that the tiles are evenly spread across the screen
    positioning_x = 1000 // 10
    current_state = back_button(mx, my, current_state, WHITE)

    # Initialization for the levels and generic initialization
    l2game_score = 0
    font = pygame.font.Font(None, 40)
    SECOND_LEVEL_START = False

    # Centering the title text and disclaimer text...
    levels_title_x, levels_title_y = center_region("LEVELS", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 80, 0, 900, 0,
                                                   125)
    display_text("LEVELS", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 100, WHITE, levels_title_x, levels_title_y)
    l3_disclaimer = font.render("Level 3 is exclusive!", False, WHITE)
    w, h = l3_disclaimer.get_size()
    screen.blit(l3_disclaimer, ((1000 - w) / 2, 550))

    # Draws the levels boxes
    for i in range(3):

        # Draws rectangles for the level/puzzle click detection
        current_rect = Rect(positioning_x + positioning_x * (3 * i), 170, positioning_x * 2, 200)
        puzzle_rect = Rect(positioning_x + positioning_x * (3 * i), 400, positioning_x * 2, 100)

        # Draws rectangles at appropriate positions
        draw.rect(screen, WHITE, current_rect, border_radius=10)
        draw.rect(screen, WHITE, puzzle_rect, border_radius=10)
        draw.rect(screen, (179, 208, 255),
                  (positioning_x + positioning_x * (3 * i) + 15, 310, positioning_x * 2 - 30, 40), border_radius=10)

        # Level and puzzle labels...
        display_text(("LEVEL %i" % (i + 1)), None, 40, BLACK, positioning_x + positioning_x * (3 * i) + 45, 210)
        display_text(("PUZZLE %i" % (i + 1)), None, 25, BLACK, positioning_x + positioning_x * (3 * i) + 58, 420)
        display_text("PLAY!", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, BLACK,
                     positioning_x + positioning_x * (3 * i) + 68, 310)

        # If the level is not unlocked...
        if not levels_unlocked[i]:
            # Display lock icon
            screen.blit(transform.scale(lock_icon, (48, 52)), (positioning_x + positioning_x * (3 * i) + 68, 240))

        # If the puzzle is not unlocked...
        if not puzzles_unlocked[i]:
            # Display lock icon
            screen.blit(transform.scale(lock_icon, (48, 52)), (positioning_x + positioning_x * (3 * i) + 68, 440))

        # If a click is detected
        if button == 1:

            # If the user clicks on the puzzle rectangle
            if puzzle_rect.collidepoint(mx, my):

                # If the rectangle clicked is the first one
                if i == 0:

                    # If the level is unlocked
                    if puzzles_unlocked[0]:
                        # Set the selected puzzle to 0 (used throughout main loop)
                        puzzle_selected = 0

                # If the second puzzle is clicked
                if i == 1:

                    # If that puzzle is unlocked
                    if puzzles_unlocked[1]:
                        # Set the selection of the puzzle
                        puzzle_selected = 1

            # If the levels selection is clicked
            if current_rect.collidepoint(mx, my):

                if i == 0:
                    level_selected = 0
                    tiles = []
                    game_score = 0
                elif i == 1:
                    level_selected = 1

    return current_state, level_selected


# Function for drawing the images (hints) on the gameplay screen
def draw_falling_images(current_state, mx, my, button):
    # Global variables used within the function scope
    global row_determinant, img_y, spacer, random_img, img_rect, bonus_clicked, random_section, random_question, hint_counter, button_press_time, current_time

    # Draws the falling hint tiles
    img_rect = Rect(random_img * 150 + 225, img_y, 100, 147)

    # Initially, the bonus clicked is false
    bonus_clicked = False

    # Here, we are checking for collision with any other tiles -- intuitively, this program will regenerate the location
    # of a new hint tile if it hits a piano tiles
    if img_y < 650 and not img_y == 0 and spacer % 2 == 1:

        # A for loop cycling through the tiles
        for tile in tiles:

            # If the tile hits the image rectangle
            if Rect(tile).colliderect(img_rect):
                # Regenerates a random location of the image
                random_img = random.randint(0, 3)

        # Displays the image to the screen
        screen.blit(transform.scale(waste_imgs, (100, 147)), (random_img * 150 + 225, img_y))

    # IN THE CASE that the tile hasn't collided
    else:

        # Regenerates a new location for the falling image and creates spacing between the next tile falling
        img_y = 0
        random_img = random.randint(0, 3)
        spacer += 1

    # If the user clicks on the hint tile
    if img_rect.collidepoint(mx, my):

        # If a click is detected...
        if button == 1:
            # Change the state to paused and start a timer that counts for 5 seconds (also generate a hint)
            current_state = PAUSE
            bonus_clicked = True
            hint_counter += 1
            button_press_time = pygame.time.get_ticks()
            random_section = random.randint(0, 1)
            random_question = random.randint(0, 2)
            current_time = 0

    # Continuously move the hint tiles down at a rate of 10px/frame
    img_y += 10

    # Return the location of the image rectangle, whether the bonus is clicked, and the state of the game to the main
    # loop
    return img_rect, bonus_clicked, current_state


# Draws the first puzzle to the screen
def draw_puzzle_1(mx, my, button, current_state):
    # Global variables to define positions within the function scope
    global character_x, answer_box, character_y, rect_selected, question_counter, bg_img, answer_rect_coordinates, \
        username_list, character_positions

    # Clear the screen and create background image
    screen.fill(BLACK)
    screen.blit(bg_img, (103, 0))

    # Current state is returned from the button
    current_state = back_button(mx, my, current_state, WHITE)

    # Draws the question image onto the screen
    question_image = image.load(questions_array[random_questions_array[question_counter]])
    image_width, image_height = question_image.get_size()
    screen.blit(transform.scale(question_image, (800, round(800 * image_height / image_width))), (100, 50))

    # Draws the multiple choice boxes
    for answer_box in answer_rect_coordinates:
        # Creates a rect for detection later on...
        answer_box = Rect(answer_box)
        draw.rect(screen, WHITE, answer_box, border_radius=10)

    # Defines the text font
    textfont = font.Font(None, 60)

    # Iterates through the answers array
    for j in range(len(answers_array[random_questions_array[question_counter]])):

        # Draws the text onto the specific coordinates defined in the answer_rect_coordinates list
        # (also centers the text using the coordinates 2D array, as well)
        text = textfont.render(str(answers_array[random_questions_array[question_counter]][j]), False, BLACK)
        text_w, text_h = text.get_size()
        x_coord = (answer_rect_coordinates[j][2] - text_w) / 2 + answer_rect_coordinates[j][0]
        y_coord = (answer_rect_coordinates[j][3] - text_h) / 2 + answer_rect_coordinates[j][1]
        screen.blit(text, (x_coord, y_coord))

    # Loop to show the user's selection
    for i in range(4):

        # Efficiency improvement
        if rect_selected % 4 == i:

            # Creates the highlight feature
            character_x = character_positions[i][0]
            character_y = character_positions[i][1]
            draw.rect(screen, RED, (character_x, character_y, 330, 120), 5, border_radius=10)

    # Draws the character depending on the character position
    screen.blit(transform.scale(e_waste_character, (85, 85)), (character_x, character_y))
    draw.rect(screen, BLACK, (0, 0, 1000, 650), 50)

    # If the user gets all the questions correct
    if question_counter >= 4 and correct_answers == 4:

        # The state is successful
        current_state = SUCCESSFUL_STATE
        levels_unlocked[1] = True

        # Move onto the stats file in which the user's score in the piano tiles level is now recorded into the file
        stats_file = open("lv1highscores.txt", 'a')

        # If the user is available
        if current_session_user_name != "":
            # Appends the data to the file
            stats_file.write(current_session_user_name + "," + str(int(current_session_high_score)) + "\n")
            stats_file.close()

    # if the use did not achieve all questions correct
    elif correct_answers != 4 and question_counter >= 4:
        # Head to failed state
        current_state = FAILED_STATE

    # Returns current state to the main loop
    return current_state


# Draws the play screen
def drawPlay(mx, my, button, current_state):

    # Global variables used within the function scope
    global y_start, start_rect, GAME_START, tiles, random_tile_height, current_rect, \
        row_determinant, row_determination, current_tile, eliminate_first_tile, game_score, level_selected, waste_imgs, \
        img_y, bonus_clicked, game_speed, puzzles_unlocked, current_session_high_score

    # Initially, the level selected is 0 (no level selected)
    level_selected = 0

    # Creates the tiles to avoid overlap and regeneration + update speed + starting point of the start tile
    tiles = create_tile(mx, my, button, current_state)
    game_speed = 0.175 * game_score + 5
    y_start = 500
    starting_x = 200

    # Background image of the play display
    screen.blit(play_background_image, (0, 0))
    draw.rect(screen, (171, 235, 255), (200, -5, 600, 660))
    draw.rect(screen, BLACK, (200, -5, 600, 660), 4)

    # Ensures that the first tile is eliminated in all circumstances. The first tile is an exception to all the other
    # tiles because it is initially paused
    while eliminate_first_tile < 1:
        # Deletes first tile
        tiles.pop(0)

        # Never enters the program in later stages
        eliminate_first_tile += 1

    # Displays the score of the game
    display_text("SCORE", None, 40, RED, 850, 50)
    display_text(str(round(game_score)), None, 40, RED, 850, 100)

    # The rect of the first tile
    start_rect = Rect(200 + row_determination * 150, y_start, 150, 150)

    # If the start rectangle is collided
    if start_rect.collidepoint(mx, my):

        # If the button is clicked
        if button == 1:
            # Starts the game!
            GAME_START = True

    # If the game hasn't started...
    if not GAME_START:

        # Draw the start button
        startButton(start_rect)

        # Draw all the tiles in a static state
        for i in range(len(tiles)):
            # Draws tiles
            draw.rect(screen, BLACK, tiles[i])

        # Start text
        display_text("START", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 40, WHITE, 240 + row_determination * 150,
                     y_start + 40)

    # In the case the game has started
    else:

        # The speed of the game + increments game score by 0.1/frame
        y_start += game_score * 0.1 + 5
        game_score += 0.1

        # Draws the falling images from the aforementioned function
        img_rectangle, bonus_clicked, current_state = draw_falling_images(current_state, mx, my, button)

        # Draws all the tiles in the array
        for i in range(len(tiles) - 1):

            # Draws all the tiles on the screen
            current_tile = Rect(tiles[i])
            draw.rect(screen, BLACK, current_tile)

            # If the hint tile is not clicked
            if not bonus_clicked:
                # Continue to move the tiles
                tiles[i][1] += game_speed

            # If the tile is being clicked
            if current_tile.collidepoint(mx, my) == 1:

                # Mouse detection
                if button == 1:
                    # Pop this tile from the list
                    tiles.pop(i)

            # If the user clicks on a tile that isn't a piano tile (game over!!!)
            elif i == 0 and current_tile.collidepoint(mx, my) == 0 and start_rect.collidepoint(mx,
                                                                                               my) != 1 and img_rectangle.collidepoint(
                mx, my) == 0 and current_state != PAUSE:

                # If the user clicked the button
                if button == 1 and game_score < 50:
                    # Returns to main menu
                    GAME_START = False
                    current_state = FAILED_STATE

                # If the button is clicked after a score of 50
                elif button == 1:
                    current_state = SUCCESSFUL_STATE

        # If the tile falls off the screen
        if tiles[0][1] > 650:
            # Remove the first element from the list and regenerate the tiles
            tiles.pop(0)
            tiles = create_tile(mx, my, button, current_state)

            if game_score < 50:
                current_state = FAILED_STATE
            else:
                current_state = SUCCESSFUL_STATE

    # Used for the lines on the gameplay screen
    for i in range(1, 4):
        # Draws the lines
        draw.line(screen, BLACK, (starting_x + 150 * i, 0), (starting_x + 150 * i, 650))

    # If the game score is passed 50, the puzzle is unlocked
    if 50 < game_score < 70:
        # NEW PUZZLE UNLOCKED!
        puzzles_unlocked = [True, False, False, False]

    # Sets the current session high score to the new high score if greater
    if game_score > current_session_high_score:
        current_session_high_score = game_score

    # Draws the back button
    current_state = back_button(mx, my, current_state, WHITE)

    # Returns the current state and the current level selected
    return current_state, level_selected


# Draws the instructions screen, given the mouse position and general program information
def drawInstructions(mx, my, button, current_state):
    # Global variables used within the function scope
    global x, y, page_counter

    # Resets screen colour
    screen.fill(BLACK)

    # The next page rectangle
    next_page_rect = Rect(800, 50, 70, 70)
    screen.blit(transform.scale(background_image, (1000, 650)), (0, 0))
    draw.rect(screen, BLACK, next_page_rect, 10, border_radius=15)
    display_text(">", None, 90, BLACK, 820, 50)

    # Instructions title
    instructions_title_x, instructions_title_y = center_region("INSTRUCTIONS", 'LoveGlitchPersonalUseRegular-vmEyA.ttf',
                                                               80, -50, 900, 0, 125)
    display_text("INSTRUCTIONS", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 100, BLACK, instructions_title_x,
                 instructions_title_y - 10)

    # Draws the instructions (page 1) to the screen
    display_text("1) Welcome to E-Tiles Master! To get started, please begin by", None, 40, BLACK, 70, 150)
    display_text("configuring your login for your score to be recorded in the", None, 40, BLACK, 70, 190)
    display_text("leaderboard or the general arrow keys", None, 40, BLACK, 70, 230)

    display_text("2) Then, return to the main menu and click play. You must start", None, 40, BLACK, 70, 300)
    display_text("with lv. 1. Play level 1 by clicking on the start tile and click ", None, 40, BLACK, 70, 340)
    display_text("on the BLACK TILES ONLY. Failure to do so will result in termination ", None, 40, BLACK, 70, 380)

    display_text("3) While playing this section of the game, your objective is to try", None, 40, BLACK, 70, 450)
    display_text("to click on as many hints tiles as possible (remember these prompts)", None, 40, BLACK, 70, 490)

    display_text("4) Game's speed will accelerate linearly and a minimum score of 50", None, 40, BLACK, 70, 560)
    display_text("must be achieved to pass level 1. After this, puzzle 1 will unlock.", None, 40, BLACK, 70, 600)

    # Current state with the back button
    current_state = back_button(mx, my, current_state, BLACK)

    # If the next page rectangle is clicked
    if next_page_rect.collidepoint(mx, my):

        # Click detected
        if button == 1:
            # Increase the page counter
            page_counter += 1

    # Return the current state of the game
    return current_state


# Draws the second page of the instructions screen
def draw_instructions_pg_2(mx, my, button, current_state):
    # Gets the page counter variable
    global page_counter

    # Resets contents of the screen
    screen.fill(BLACK)

    # Creates the background image
    screen.blit(transform.scale(background_image, (1000, 650)), (0, 0))

    previous_page_rect = Rect(70, 50, 70, 70)

    draw.rect(screen, BLACK, previous_page_rect, 10, border_radius=15)
    display_text("<", None, 90, BLACK, 90, 50)

    display_text("5) Finish puzzle 1 by navigating using the arrow keys and pressing", None, 40, BLACK, 70, 150)
    display_text("enter once you have made your final selection. You must get all", None, 40, BLACK, 70, 190)
    display_text("correct to pass.", None, 40, BLACK, 70, 230)

    display_text("6) Return to the levels screen and start level 2. To pass level 2,", None, 40, BLACK, 70, 300)
    display_text("you must press enter to start. Use the arrow keys to maximize time", None, 40, BLACK, 70, 340)
    display_text("on the black tiles. Time not spent on the black tiles will kill.", None, 40, BLACK, 70, 380)

    display_text("7) Finish the corresponding puzzle once a score of 50 is achieved.", None, 40, BLACK, 70, 450)
    display_text("(memorize the e-waste Cycle)", None, 40, BLACK, 70, 490)

    display_text("8) You have finished the game! Congratulations!", None, 40, BLACK, 70, 560)

    # If the previous page is clicked
    if previous_page_rect.collidepoint(mx, my):

        # Clicked
        if button == 1:
            # Reduces the page counter
            page_counter -= 1

    # Returns the current state to the main loop
    return current_state


# Draws the login page
def drawlogin(mx, my, button, current_state):
    # Global variables defined the function scope
    global username, current_session_user_name, submitted, username_list

    # Clears the screen
    screen.fill(BLACK)

    # The submit button is created through the instantiation of the Rect object
    submit_rect = Rect(370, 450, 200, 50)
    draw.rect(screen, WHITE, submit_rect, border_radius=15)

    # Username textbox caption
    display_text("Enter a Username", None, 50, WHITE, 330, 200)
    draw.rect(screen, WHITE, (280, 280, 400, 80), 5, border_radius=15)
    display_text("@", None, 50, WHITE, 300, 300)
    display_text(username, None, 50, WHITE, 340, 300)
    display_text("Start Typing...", None, 50, WHITE, 360, 390)
    display_text("Done!", None, 50, BLACK, 420, 460)

    # If the submit button is clicked and the submit button has yet to be clicked
    if submit_rect.collidepoint(mx, my) and not submitted and username not in username_list:

        # If the button is clicked
        if button == 1:
            # The session username is set to the user entered by the user
            current_session_user_name = username
            submitted = True

    # If the button is clicked
    if submitted:
        # Change the button text to green
        display_text("Done!", None, 50, (0, 255, 0), 420, 460)

    # Draws back button
    current_state = back_button(mx, my, current_state, WHITE)

    # Returns current state to game loop
    return current_state


# If the game is successfully played, the screen created by the following function will be displayed
def successfully_played(mx, my, button, current_state):
    # Global variables used within the function scope
    global y_start, GAME_START, tiles, level_selected, page_counter, question_counter, puzzle_selected, \
        hit_counter, loss_counter, puzzle2_question_counter, puzzle_two_correct, eliminate_first_tile, correct_answers, levels

    # Resetting the variables changed throughout the levels' selection (user can play the game multiple times)
    level_selected = -1
    y_start = 500
    page_counter = 0
    GAME_START = False
    tiles = []
    question_counter = 0
    correct_answers = 0
    puzzle_selected = -1
    puzzle2_question_counter = 0
    puzzle_two_correct = 0
    eliminate_first_tile = 0
    hit_counter = 0
    loss_counter = 100

    # Reset the contents of the screen
    screen.fill(BLACK)

    # Drawing the successful prompt
    draw.rect(screen, WHITE, (200, 100, 600, 400), border_radius=15)
    display_text("Congratulations! You have successfully", None, 40, BLACK, 220, 150)
    display_text("played the level", None, 40, BLACK, 415, 190)
    screen.blit(transform.scale(home_button, (150, 150)), (300, 270))
    screen.blit(transform.scale(replay_button, (150, 150)), (550, 270))
    home_button_rect = Rect(300, 270, 150, 150)
    replay_button_rect = Rect(550, 270, 150, 150)

    # Draws the button and sets the current state
    current_state = back_button(mx, my, current_state, WHITE)

    if button == 1:
        # Home button clicked
        if home_button_rect.collidepoint(mx, my):

            # Current state set to the main menu
            current_state = MAIN_MENU_STATE

        # The replay button is clicked
        if replay_button_rect.collidepoint(mx, my):

            # Returns to the menu state
            current_state = GAMEPLAY_STATE
            question_counter = 0
            puzzle_selected = -1
            GAME_START = False

    # Return the current state to the game loop
    return current_state


# Draws the hint page
def drawHintPage(mx, my, button, current_state):
    # All the global variables defined within this function scope
    global hint_counter, random_section, random_question, user_hint_categories, user_hint_questions, bonus_clicked, button_press_time

    # Draws the hint screen with all corresponding hints
    pygame.draw.rect(screen, (207, 207, 207), (100, 180, 800, 250), border_radius=10)
    hint_title_x, hint_title_y = center_region("Hint #" + str(hint_counter), 'LoveGlitchPersonalUseRegular-vmEyA.ttf',
                                               80, 0, 1000, 200, 280)
    display_text("Hint #", 'LoveGlitchPersonalUseRegular-vmEyA.ttf', 80, BLACK, hint_title_x, hint_title_y)
    display_text(str(hint_counter), None, 80, BLACK, hint_title_x + 130, hint_title_y + 10)

    display_text(user_hint_categories[random_section] + " Hint: ", None, 35, BLACK, 125, 300)

    # If the certain hint is this one
    if user_hint_questions[random_section][random_question] == "The average cell phone user replaces their unit every " \
                                                               "18 months.":

        # display text
        display_text("The average cell phone user replaces their unit", None, 35, BLACK, 300, 330)
        display_text("every 18 months.", None, 35, BLACK, 390, 360)
        user_hint_questions.pop([0][0])

    # If the certain hint is this one
    elif user_hint_questions[random_section][random_question] == "85% of our e-waste sent to landfills and " \
                                                                 "incinerators is burned, and releases harmful toxins " \
                                                                 "into the air":

        # Display text
        display_text("85% of our e-waste sent to landfills and incinerators", None, 35, BLACK, 285, 300)
        display_text("is burned, and releases harmful toxins into the air", None, 35, BLACK, 230, 330)

    # Certain hint is selected
    elif user_hint_questions[random_section][random_question] == "300 million computers and over 1 billion cell phones " \
                                                                 "are produced each year.":

        # Display text
        display_text("300 million computers and over 1 billion cell phones ", None, 35, BLACK, 280, 300)
        display_text("are produced each year.", None, 35, BLACK, 360, 330)

    # Certain hint is selected
    elif user_hint_questions[random_section][random_question] == "Doctors recommend that for every 20 minutes you " \
                                                                 "spend on a screen, look away for 20 seconds and focus " \
                                                                 "your eyes on an object 20 feet away.":

        # Display corresponding text
        display_text("Doctors recommend that for every 20 minutes you ", None, 35, BLACK, 290, 300)
        display_text("spend on a screen, look away for 20 seconds and focus your eyes", None, 35, BLACK, 125, 330)
        display_text(" on an object 20 feet away.", None, 35, BLACK, 320, 360)

    # Certain hint is selected
    elif user_hint_questions[random_section][random_question] == "A 2017 study of 8th to 12th graders found that high " \
                                                                 "levels of depressive symptoms increased by 33% " \
                                                                 "between 2010 and 2015.":

        # Corresponding hint text
        display_text("A 2017 study of 8th to 12th graders found that high", None, 35, BLACK, 300, 300)
        display_text("levels of depressive symptoms increased by 33% between 2010", None, 35, BLACK, 140, 330)
        display_text("and 2015.", None, 35, BLACK, 420, 360)

    # Another hint check
    elif user_hint_questions[random_section][random_question] == "The more time spent on social media can lead to " \
                                                                 "cyberbullying, social anxiety, depression, " \
                                                                 "and exposure to content that is not age " \
                                                                 "appropriate.":

        # Display corresponding text
        display_text("The more time spent on social media can lead to ", None, 35, BLACK, 280, 300)
        display_text("cyberbullying, social anxiety, depression, and exposure to ", None, 35, BLACK, 125, 330)
        display_text("content that is not age appropriate.", None, 35, BLACK, 360, 360)

    # Draws the countdown timer
    draw.circle(screen, BLACK, (110, 190), 25)
    display_text(str(round(5 - -1 * (button_press_time - current_time) / 1000)), None, 40, WHITE, 100, 180)

    # Timer if statement
    if button_press_time - current_time < -5000:

        # Returns to gameplay
        current_state = GAMEPLAY_STATE
        bonus_clicked = False

    # Returns current state of game to main loop
    return current_state


# Draws the screen users are faced with when they fail a level
def failed_played(mx, my, button, current_state):
    # Global functions used within the function scope
    global question_counter, puzzle_selected, GAME_START, level_selected, y_start, page_counter, tiles, \
        puzzle2_question_counter, puzzle_two_correct, eliminate_first_tile, hit_counter, loss_counter, correct_answers

    level_selected = -1
    y_start = 500
    page_counter = 0
    GAME_START = False
    tiles = []
    question_counter = 0
    puzzle_selected = -1
    correct_answers = 0
    puzzle2_question_counter = 0
    puzzle_two_correct = 0
    eliminate_first_tile = 0
    hit_counter = 0
    loss_counter = 100

    # Reset the contents of the screen
    screen.fill(BLACK)

    # Drawing the successful prompt
    draw.rect(screen, WHITE, (200, 100, 600, 400), border_radius=15)
    display_text("Oh No! You have failed the level!", None, 40, BLACK, 280, 150)
    display_text("Return to the main menu to try again.", None, 40, BLACK, 260, 190)
    screen.blit(transform.scale(home_button, (150, 150)), (300, 270))
    screen.blit(transform.scale(replay_button, (150, 150)), (550, 270))
    home_button_rect = Rect(300, 270, 150, 150)
    replay_button_rect = Rect(550, 270, 150, 150)

    # Draws the button and sets the current state
    current_state = back_button(mx, my, current_state, WHITE)

    if button == 1:
        # Home button clicked
        if home_button_rect.collidepoint(mx, my):

            # Current state set to the main menu
            current_state = MAIN_MENU_STATE

        # The replay button is clicked
        if replay_button_rect.collidepoint(mx, my):

            current_state = GAMEPLAY_STATE
            question_counter = 0
            puzzle_selected = -1
            GAME_START = False

    # Returns current state to game loop
    return current_state


# Draws the second level screen, given auxiliary inputs from the game loop
def level2screen(mx, my, button, current_state):
    # Global variables used within the function scope
    global l2game_score, curr_tile, game_speed, SECOND_LEVEL_START, current_column, hit_counter, loss_counter, termination_time, level_selected

    # Determines the speed of the game (dependent on the game score)
    game_speed = 0.1 * l2game_score + 5

    # Resets the screen to blank
    screen.fill(BLACK)

    # Draws the back button
    current_state = back_button(mx, my, current_state, WHITE)

    # Draws all the elements of the gameplay screen (lines separating the tiles)
    draw.rect(screen, (171, 235, 255), (200, -5, 600, 660))
    draw.line(screen, BLACK, (200, 0), (200, 650))
    draw.line(screen, BLACK, (350, 0), (350, 650))
    draw.line(screen, BLACK, (500, 0), (500, 650))
    draw.line(screen, BLACK, (650, 0), (650, 650))
    draw.line(screen, BLACK, (800, 0), (800, 650))

    # Creates a new set of tiles for the gameplay experience
    tiles = create_tile(mx, my, button, current_state)

    # If the second level hasn't started
    if not SECOND_LEVEL_START:

        # Draw all the tiles at their predetermined locations
        for tile in range(len(tiles) - 1):
            # Drawing the tiles
            draw.rect(screen, BLACK, tiles[tile])

    # If the second level started
    else:

        # For each panel tile
        for tile_panel in range(len(tiles) - 1):

            # Set the current rectangle to the most recent and display it onto the screen
            curr_tile = Rect(tiles[0])
            draw.rect(screen, BLACK, tiles[tile_panel])

            # If the game score
            if l2game_score < 50:
                # Continue to increase the gamespeed
                tiles[tile_panel][1] += game_speed

        # The target is a rectangle tracking the position of the circle target used to giving aiming capabilities to
        # the player
        target = Rect(current_column * 150 + 200, 437, 25, 25)

        # Possible column values
        for j in range(4):

            # Detects the current column
            if current_column == j:

                # Adjusts the visual selector
                draw.line(screen, SELECTOR_BLUE, (selector_coordinates[j][0], 0), (selector_coordinates[j][0], 650), width=10)
                draw.line(screen, SELECTOR_BLUE, (selector_coordinates[j][1], 0), (selector_coordinates[j][1], 650), width=10)
                draw.circle(screen, SELECTOR_BLUE, (selector_coordinates[j][0]+75, 450), 25)

        # If the target hits the piano tiles
        if target.colliderect(curr_tile):

            # Made to not exceed 100% health
            if loss_counter / total_loss_tolerance < 1:
                # Increments the hit counter and restores the losses
                hit_counter += 1
                loss_counter += 1

        # Target is not hit
        else:
            # The loss counter is incremented
            loss_counter -= 0.45

        # If the tile falls of the screen...
        if tiles[0][1] >= 650:
            # The tiles array will pop the first element (one that has fallen off the screen)
            tiles.pop(0)

        # Screen life bar
        display_text("LIFE", None, 40, RED, 25, 50)
        draw.rect(screen, RED, (25, 100, 150, 25), 5, border_radius=10)

        # if the second level score is greater than 50... (show the diagram)
        if l2game_score > 50:

            # Draws the diagram screen
            draw.rect(screen, WHITE, (150, 100, 700, 500), border_radius=50)
            screen.blit(transform.scale(diagram_img, (420, 438)), (285, 130))

            # Timer code
            termination_time -= 1 / 60
            display_text(str(round(termination_time)), None, 60, BLACK, 180, 130)

            # If the termination time is up...
            if termination_time < 0:
                # Return to the menu state
                current_state = GAMEPLAY_STATE
                level_selected = -1
                puzzles_unlocked[1] = True

        # If the score is under 50
        else:

            # Continue to falling trash images
            draw_falling_images(mx, my, current_state, button)
            draw.rect(screen, RED, (25, 100, int(150 * (loss_counter / total_loss_tolerance)), 25), border_radius=10)
            l2game_score += 0.1

            # Loss tolerance (if health == 0)
            if loss_counter / total_loss_tolerance < 0:
                # Returns to main menu
                current_state = FAILED_STATE

    # Displays the l2 score
    display_text("SCORE", None, 40, RED, 850, 50)
    display_text(str(round(l2game_score)), None, 40, RED, 850, 100)

    # Returns the current state and the selected level back to the main loop
    return current_state, level_selected


# Draws the second level puzzle
def level_two_puzzle(mx, my, button, current_state):
    # Global variables used within the function scope
    global answer_rect_coordinates, puzzle2_question_counter, puzzle_two_correct

    # Resets the colour of the screen
    screen.fill(BLACK)

    # Draws the puzzle background and question using the predefined multiple choice questions two-dimensional array
    screen.blit(transform.scale(l2puzzle_background, (1000, 650)), (0, 0))
    display_text(multiple_choice_questions[puzzle2_question_counter], None, 80, BLACK, 70, 105)
    display_text("cycle?", None, 80, BLACK, 400, 175)

    # For each tile in answer rect coordinates, draw the answer labels
    for answer_tile in range(len(answer_rect_coordinates)):

        # Draws and creates rectangle objects for drawing the labels and the multiple choice question boxes themselves
        draw.rect(screen, BLACK, answer_rect_coordinates[answer_tile], 5, border_radius=15)
        currRect = Rect(answer_rect_coordinates[answer_tile])

        x_coord = answer_rect_coordinates[answer_tile][0] + 30
        y_coord = answer_rect_coordinates[answer_tile][1] + 15
        display_text(str(answer_tile + 1) + ". " + str(multiple_choice_labels[puzzle2_question_counter][answer_tile]), None, 50, BLACK, x_coord, y_coord)

        # if the user gets more than two questions correct in the puzzle
        if puzzle_two_correct >= 2:

            # Return to successful page
            current_state = SUCCESSFUL_STATE

        # If the puzzle is continuing (yet to complete the puzzle)
        elif puzzle_two_correct <= 2 and puzzle2_question_counter > 2:
            current_state = FAILED_STATE
        else:

            # Finish the current rectangle (see if contact is made)
            if currRect.collidepoint(mx, my):

                # Click is detected
                if button == 1:

                    # Question counter incremented by 1
                    puzzle2_question_counter += 1

                    # Checking if it's the correct answer
                    if answer_tile == multiple_choice_answers[puzzle2_question_counter]:
                        # If so, increment the correct variable by 1
                        puzzle_two_correct += 1

    # Draws the back button
    current_state = back_button(mx, my, current_state, BLACK)

    # Returns the current state to the main loop
    return current_state


# MAIN PROGRAM
# Initialization variables (used within the main loop)
program_running = True
myClock = pygame.time.Clock()
current_state = MAIN_MENU_STATE
mx = my = button = 0
pressed_right = False
pressed_left = False
pressed_up = False
pressed_down = False
correct_answers = 0
current_column = 0

# White the program is running
while program_running:

    # Initially, the button is set to 0
    button = 0

    # Check all the events that happen
    for evnt in event.get():
        # if the user tries to close the window, then raise the "flag"
        if evnt.type == QUIT:
            program_running = False

        # If the mouse button is down
        if evnt.type == MOUSEBUTTONDOWN:
            # capture mx and my to return to functions
            mx, my = evnt.pos
            button = evnt.button

        # If the mouse is being moved
        if evnt.type == MOUSEMOTION:
            # Capture the mx and my position to the functions
            mx, my = evnt.pos

        # If the key is down
        if evnt.type == KEYDOWN:

            # The right key is clicked
            if evnt.key == K_RIGHT:
                pressed_right = True

                # Case in the second level
                if SECOND_LEVEL_START:

                    # Increment the column counter
                    current_column += 1

                    # Adjust if it's on the outermost column
                    if current_column > 3:
                        current_column -= 1

            # The left key is clicked
            elif evnt.key == K_LEFT:
                pressed_left = True
                if SECOND_LEVEL_START:
                    current_column -= 1
                    if current_column < 0:
                        current_column += 1

            # The enter key is clicked
            elif evnt.key == K_RETURN:

                # If the second level is selected
                if level_selected == 1:
                    # Start the second level and pop the first tile to avoid repetition
                    SECOND_LEVEL_START = True
                    tiles.pop(0)

                # While the puzzle 1 question counter is less than 5
                if question_counter < 5:

                    # First puzzle selected...
                    if puzzle_selected == 0:

                        # Increment the number of questions entered by the user
                        question_counter += 1

                        # Checking for the correct answer
                        if (rect_selected + 3) % 4 == final_list[question_counter - 1]:
                            # Increment to the correct answers
                            correct_answers += 1

            # Only in the login state
            if current_state == LOGIN_STATE:

                # Special case for backspace
                if evnt.key == K_BACKSPACE:

                    # Eliminates one of the characters
                    username = username[:-1]

                # All other keys
                else:

                    # Restricts input to 8 characters
                    if len(username) < 8:
                        # Adds unicode of the keyboard
                        username += evnt.unicode

        if evnt.type == KEYUP:
            if evnt.key == K_RIGHT:
                pressed_right = False
            elif evnt.key == K_LEFT:
                pressed_left = False
            elif evnt.key == K_UP:
                pressed_up = False
            elif evnt.key == K_DOWN:
                pressed_down = False

        # If the first puzzle is selected...
        if puzzle_selected == 0:

            # Right detection
            if pressed_right:

                # Changes the rect selection
                rect_selected += 1

            # Left detection
            elif pressed_left:

                # Changes the rect selection
                rect_selected -= 1

    # When the user is in the state of the main menu
    if current_state == MAIN_MENU_STATE:
        screen.blit(transform.scale(background_image, (1000, 700)), (0, 0))
        current_state = drawMenu(mx, my, button, current_state)
        row_determination = random.randint(0, 3)

    # In the case the gameplay state is triggered
    elif current_state == GAMEPLAY_STATE:

        # If the first level is selected
        if level_selected == 0:
            current_state, level_selected = drawPlay(mx, my, button, current_state)

        # Second level selected
        elif level_selected == 1 and levels_unlocked[1]:
            current_state, level_selected = level2screen(mx, my, button, current_state)

        # Menu screen (levels screen)
        else:
            current_state, level_selected = levels_screen(mx, my, button, current_state)

        # If the first puzzle is selected
        if puzzle_selected == 0:

            # Draw the first puzzle
            current_state = draw_puzzle_1(mx, my, button, current_state)

        elif puzzle_selected == 1:
            current_state = level_two_puzzle(mx, my, button, current_state)

    # When the user successfully finishes the puzzle
    elif current_state == SUCCESSFUL_STATE:
        current_state = successfully_played(mx, my, button, current_state)
        puzzle_selected = -1

    # When the user fails...
    elif current_state == FAILED_STATE:

        # Sets the state to failed and all puzzles and levels deselected
        current_state = failed_played(mx, my, button, current_state)
        puzzle_selected = -1
        levels_selected = -1

    # In the case the instructions state is triggered
    elif current_state == INSTRUCTIONS_STATE:

        # If the instructions page selected is 1
        if page_counter == 0:

            # Draws the first page
            current_state = drawInstructions(mx, my, button, current_state)

        # If the instructions page selected is 2
        elif page_counter == 1:

            # Draws the second page
            current_state = draw_instructions_pg_2(mx, my, button, current_state)

    # User opts to quit the game
    elif current_state == QUIT:
        program_running = False

    # Current state in the login
    elif current_state == LOGIN_STATE:
        current_state = drawlogin(mx, my, button, current_state)

    # Current state in the leaderboard
    elif current_state == LEADERBOARD_STATE:
        current_state = drawLeader(mx, my, button, current_state)

    # The state of being paused
    elif current_state == PAUSE:

        # Draws the hint screen (only case where the PAUSE state is used)
        current_state = drawHintPage(mx, my, button, current_state)

    # Gets the current time to pass information to other parts of the program
    current_time = pygame.time.get_ticks()

    # waits long enough to have 60 fps
    display.flip()
    myClock.tick(60)

# Quits the program
quit()
