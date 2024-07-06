# Importing Modules
import pygame
from io import BytesIO
import numpy as np
import ai


frame = 0
# clear log file
with open('chess.log', 'w') as f:
    pass

def print_n_log(*args):
    print(*args)
    with open('chess.log', 'a') as f:
        print(*args, file=f)

# Initialising pygame module
pygame.init()

# Setting Width and height of the Chess_Game screen
WIDTH = 1000
HEIGHT = 1000

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess_Game')

small_font = pygame.font.Font('freesansbold.ttf', 18)
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 1

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

pieces_path = 'C:/Users/miikka/OneDrive - Aveso/Desktop/Projektit/Muut/chess/pieces/'
# url for Chess_pieces images
images = ['Chess_qdt60.png',
            'Chess_kdt60.png',
            'Chess_rdt60.png',
            'Chess_bdt60.png',
            'Chess_ndt60.png',
            'Chess_pdt60.png',
            'Chess_qlt60.png',
            'Chess_klt60.png',
            'Chess_rlt60.png',
            'Chess_blt60.png',
            'Chess_nlt60.png',
            'Chess_plt60.png']

images = [pieces_path + image for image in images]


# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load(images[0])
small_black_queen = pygame.transform.scale(black_queen, (80, 80))
black_king = pygame.image.load(images[1])
small_black_king = pygame.transform.scale(black_king, (80, 80))
black_rook = pygame.image.load(images[2])
small_black_rook = pygame.transform.scale(black_rook, (80, 80))
black_bishop = pygame.image.load(images[3])
small_black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_knight = pygame.image.load(images[4])
small_black_knight = pygame.transform.scale(black_knight, (80, 80))
black_pawn = pygame.image.load(images[5])
small_black_pawn = pygame.transform.scale(black_pawn, (80, 80))

white_queen = pygame.image.load(images[6])
small_white_queen = pygame.transform.scale(white_queen, (80, 80))
white_king = pygame.image.load(images[7])
small_white_king = pygame.transform.scale(white_king, (80, 80))
white_rook = pygame.image.load(images[8])
small_white_rook = pygame.transform.scale(white_rook, (80, 80))
white_bishop = pygame.image.load(images[9])
small_white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_knight = pygame.image.load(images[10])
small_white_knight = pygame.transform.scale(white_knight, (80, 80))
white_pawn = pygame.image.load(images[11])
small_white_pawn = pygame.transform.scale(white_pawn, (80, 80))


white_images = [white_pawn, white_queen, white_king,
                white_knight, white_rook, white_bishop]
small_white_images = [small_white_pawn, small_white_queen, small_white_king,
                        small_white_knight, small_white_rook, small_white_bishop]

black_images = [black_pawn, black_queen, black_king,
                black_knight, black_rook, black_bishop]
small_black_images = [small_black_pawn, small_black_queen, small_black_king,
                        small_black_knight, small_black_rook, small_black_bishop]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

comment = "- -"
# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [
                             600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [
                             700 - (column * 200), row * 100, 100, 100])

        # newline comment every 15 words
        tokens = comment.replace('"', '').split()
        new_comment = ""
        for i in range(len(tokens)):
            new_comment += tokens[i] + " "
            if i % 15 == 0 and i != 0:
                screen.blit(small_font.render(
                    new_comment, True, 'black'), (20, 820 + 20 * i // 15))
                new_comment = ""
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)



# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(
                white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i]
                                              [0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(
                black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i]
                                              [0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!',
                            True, 'white'), (210, 240))

def coords_to_chess_notation(coords):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return f'{letters[coords[0]]}{coords[1]+1}'

def chess_notation_to_coords(notation):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return (letters.index(notation[0]), int(notation[1])-1)

def get_board_as_notations():
    board = "White pieces:\n"
    print_n_log('White pieces:')
    for i in range(len(white_pieces)):
        print_n_log(f'{white_pieces[i]} at {coords_to_chess_notation(white_locations[i])}')
        board += f'{white_pieces[i]} at {coords_to_chess_notation(white_locations[i])}\n'
    print_n_log('Black pieces:')
    board += "Black pieces:\n"
    for i in range(len(black_pieces)):
        print_n_log(f'{black_pieces[i]} at {coords_to_chess_notation(black_locations[i])}')
        board += f'{black_pieces[i]} at {coords_to_chess_notation(black_locations[i])}\n'

    return board


# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
error = ""
last_move = "First move of the game."
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()


    # event handling
    # Remove pygame event handling and replace with input prompts
    if not game_over:
        try:
            if turn_step <= 1:
                player = 'White'
                piece, move = ai.get_a_move(get_board_as_notations(), 'white', last_move, error)
                print_n_log(piece, move)
                in_case_of_error = f"You tried {piece}->{move} but that is illegal. Try another piece!"
                valid_pieces_str = [str(i) for i in white_locations]
                valid_pieces_str = [i.replace('(', '').replace(')', '') for i in valid_pieces_str]
                #from_input = np.random.choice(valid_pieces_str)
                from_input = piece
                from_coords = chess_notation_to_coords(from_input)
                print_n_log(from_coords)

                if from_coords in white_locations:
                    selection = white_locations.index(from_coords)
                else:
                    raise ValueError("Invalid selection. Please select a white piece.", white_locations)

                valid_moves = check_valid_moves()

                if len(valid_moves) == 0:
                    raise ValueError("No valid moves for this piece. Please select another piece.", valid_moves)

                valid_moves_str = [str(i) for i in valid_moves]
                valid_moves_str = [i.replace('(', '').replace(')', '') for i in valid_moves_str]
                #to_input = np.random.choice(valid_moves_str)
                to_input = move

                to_coords = chess_notation_to_coords(to_input)

                selection = white_locations.index(from_coords)
                if to_coords in valid_moves and selection != 100:
                    white_locations[selection] = to_coords
                    if to_coords in black_locations:
                        black_piece = black_locations.index(to_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                else:
                    raise ValueError("Invalid move. Please enter a valid move.", valid_moves)

            elif turn_step > 1:
                player = 'Black'
                piece, move = ai.get_a_move(get_board_as_notations(), 'black', last_move, error)
                print_n_log(piece, move)
                in_case_of_error = f"You tried {piece}->{move} but that is illegal. Try another piece!"
                valid_pieces_str = [str(i) for i in black_locations]
                valid_pieces_str = [i.replace('(', '').replace(')', '') for i in valid_pieces_str]
                #from_input = np.random.choice(valid_pieces_str)
                from_input = piece
                from_coords = chess_notation_to_coords(from_input)

                if from_coords in black_locations:
                    selection = black_locations.index(from_coords)
                else:
                    raise ValueError("Invalid selection. Please select a black piece.", black_locations)
                
                valid_moves = check_valid_moves()
                if len(valid_moves) == 0:
                    raise ValueError("No valid moves for selected piece. Please select another piece.", black_locations)

                valid_moves_str = [str(i) for i in valid_moves]
                valid_moves_str = [i.replace('(', '').replace(')', '') for i in valid_moves_str]
                #to_input = np.random.choice(valid_moves_str)
                to_input = move
                to_coords = chess_notation_to_coords(to_input)

                if to_coords in valid_moves and selection != 100:
                    black_locations[selection] = to_coords
                    if to_coords in white_locations:
                        white_piece = white_locations.index(to_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                else:
                    raise ValueError("Invalid move. Please enter a valid move.", valid_moves)
            error = ""
            last_move = f"Your oppenent moved from {from_input} to {to_input}"
            comment = ai.get_move_comment(get_board_as_notations(), player, last_move)
            print_n_log(comment)
            # save the game window as an image
            pygame.image.save(screen, f'recordings/chess_{frame}.png')
            frame += 1
        except ValueError as e:
            print_n_log(e)
            error = in_case_of_error

    pygame.display.flip()


pygame.quit()