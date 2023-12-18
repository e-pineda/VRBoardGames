import keras
from src.Board import Board
from src.TicTacToeClassifier import reshape_input
from src.image_processing import *
from src.utils import *
import time

BOARD_MOVES_FILE = "G:\My Drive\TicTacToe\\board.csv"
GAME_STATUS_FILE = "G:\My Drive\TicTacToe\\GameStatus.txt"
GAME_MODE_FILE = "G:\My Drive\TicTacToe\\GameMode.txt"


def purge_game_files():
    with open(GAME_STATUS_FILE, 'w') as file:
        file.truncate(0)

    with open(BOARD_MOVES_FILE, 'r+') as file:
        file.truncate(0)

    # with open(GAME_MODE_FILE, 'r+') as file:
    #     file.truncate(0)

# leverages CNN to detect if the user made a move in the given cell
def detect_user_movement(grid_cell):
    mapper = {0: 'O', 1: 'None', 2: 'X'}
    # print(grid_cell)
    grid_cell = reshape_input(grid_cell)
    idx = np.argmax(loaded_model.predict(grid_cell))
    return mapper[idx]

# writes the made move to the file
def write_move_to_file(p_symbol, move_pos):
    if move_pos == 0:
        move = f'{p_symbol},0,0\n'
    elif move_pos == 1:
        move = f'{p_symbol},0,1\n'
    elif move_pos == 2:
        move = f'{p_symbol},0,2\n'
    elif move_pos == 3:
        move = f'{p_symbol},1,0\n'
    elif move_pos == 4:
        move = f'{p_symbol},1,1\n'
    elif move_pos == 5:
        move = f'{p_symbol},1,2\n'
    elif move_pos == 6:
        move = f'{p_symbol},2,0\n'
    elif move_pos == 7:
        move = f'{p_symbol},2,1\n'
    elif move_pos == 8:
        move = f'{p_symbol},2,2\n'
    # print(f'{p_symbol}\'s move: {move}')
    with open(BOARD_MOVES_FILE, 'a') as file:
        file.write(move)

def is_game_done(board):
    if board.complete():
        if board.O_won() and PLAYER1_SYMBOL == 'O':
            print('Player 1 won!')
        elif board.X_won() and PLAYER1_SYMBOL == 'X':
            print('Player 1 won!')
        elif board.X_won() and PLAYER1_SYMBOL != 'X':
            print('Player 2 won!')
        elif board.O_won() and PLAYER1_SYMBOL != 'O':
            print('Player 2 won!')
        elif board.tied():
            print('Tied game!')
        write_game_status_to_file()
        return 'Done'
    return 'no'


def write_game_status_to_file():
    with open(GAME_STATUS_FILE, 'w') as file:
        file.write('Done')


def read_game_mode():

    total_time = 0

    while True:
        with open(GAME_MODE_FILE, 'r') as file:
            gameMode = file.readline()
            if gameMode != '':
                return gameMode
        print(f'GameMode file is empty; retrying in 1 sec {total_time}')
        total_time += 1
        time.sleep(1)


def update_current_player(curr_symbol):
    if curr_symbol == PLAYER1_SYMBOL:
        return PLAYER2_SYMBOL
    elif curr_symbol == PLAYER2_SYMBOL:
        return PLAYER1_SYMBOL


# Instantiate Board obj for the game as well dictionary to track game history
board = Board()
g_status = is_game_done(board)

history = {}
message = True

# Set player's symbols for the game
PLAYER1_SYMBOL = currentSymbol = 'X'
PLAYER2_SYMBOL = 'O'

# Purge the game files so we are not overwriting
purge_game_files()
# print('Reset game files\n')


# ingest the game mode
game_mode = read_game_mode()
# game_mode = 'SinglePlayer'


''' 
The AI_move_detection_mode variable determines if the game uses a CNN to detect the position of the player's moves.

If on (e.g. AI move detection is True), the player will have to make their move and hit the space bar to let the program 
know their move has been made. From there, the game will leverage the trained CNN to detect which slot the player made
their move in. 

If off (e.g. AI move detection is False), the player will have to type their move into the program and then hit the space
bar to let the program know their move has been made. 

For reference, the CNN to detect the position of player's moves will have to be loaded. 
'''
AI_move_detection_mode = False
if AI_move_detection_mode:
    model_path = 'model/TicTacToeClassifier.h5'
    loaded_model = keras.models.load_model(model_path)


''' 
The is_easy_opponent variable determines the difficulty of the computer opponent that the player will face. 

If on (e.g. is_easy_opponent = True), the computer opponent will be using the minimax algorithm. 
If off (e.g. is_easy_opponent = False), the computer opponent will be using the alphabeta algorithm. 
'''
print(f'Game mode: {game_mode}')
if game_mode == 'SinglePlayer':
    computer_opponent = True
    is_easy_opponent = False
    if is_easy_opponent:
        print(f'Computer Difficulty: Easy (minimax algorithm)')
    else:
        print(f'Computer Difficulty: Hard (alphabeta algorithm)')
else:
    computer_opponent = False

# prevents the users from making illegal moves
satisfactory_move = True

# Turn on web camera, begin ingesting live video feed from camera as well as entered key strokes from user
cap = cv2.VideoCapture(0)
while cap.isOpened():

    ret, frame = cap.read()
    key = cv2.waitKey(1) & 0xFF

    # 0. Show live video feed -- shows the program is working
    cv2.imshow('Step 0. Live Original Video Feed', frame)

    # 1. convert live video feed to gray scale -- video feed will be easier to work with than colored feed
    gray_frame = to_gray_scale(frame)
    cv2.imshow('Step 1. Manipulated Video Feed', gray_frame)

    # 2. Find the playable board & present a top-down view of it
    board_frame = find_board(frame, gray_frame)
    cv2.imshow('Step 2. Top-down view of board', board_frame)

    # 3. Find & record the positions of the playable slots on the board
    board_frame, img_thresh, move_slot_coords = find_grid(board_frame)

    # 4. Draw & populate grid with made moves
    for i, (x, y, w, h) in enumerate(move_slot_coords):
        cv2.rectangle(board_frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
        if history.get(i) is not None:
            shape = history[i]['shape']
            board_frame = draw_shape(board_frame, shape, (x, y, w, h))
    cv2.imshow('Step 4. Board w/ detected grid', board_frame)

    # 5. Prompt user to make move and if needed, record made move
    available_moves = board.available_moves()
    unavailable_moves = board.unavailable_moves()

    unavailable_keys = [x+48 for x in unavailable_moves]
    if message and g_status != 'Done':
        print(f'{currentSymbol}\'s Available moves: {board.available_moves()}')
        print(f'{currentSymbol}\'s Unavailable moves: {board.unavailable_moves()}')
        if AI_move_detection_mode:
            print(f'\nPlayer {currentSymbol}\'s turn!\nMake move (on window), then press spacebar\n')
        else:
            print(f'\nPlayer {currentSymbol}\'s turn!\nEnter move (on window), then press spacebar\n')
        message = False

    if key != 255 and g_status != 'Done':
        # print(key, type(key))
        if 48 <= key < 57:
            if key in unavailable_keys:
                # if key == 32 and movePos is None:
                #     print(f'No, movePos = {movePos}')
                # print('Unavailable move; try again')
                satisfactory_move = False
            elif key not in unavailable_keys:
                movePos = key - 48
                satisfactory_move = True
                # print(f'Set satisfactory move to true as movePos={movePos}')
        # print('----------------------')
    if not key == 32:
        continue

    if satisfactory_move and g_status != 'Done':
        # 6. Determine player's position if AI_move_detection_mode is true, make, record & write player's move
        for i, (x, y, w, h) in enumerate(move_slot_coords):
            if i not in available_moves:
                continue
            if AI_move_detection_mode:
                slot_img = img_thresh[int(y): int(y + h), int(x): int(x + w)]
                print(slot_img.shape)
                detected_move_shape = detect_user_movement(slot_img)
                print(i, detected_move_shape)
            else:
                if i == movePos:
                    # detected_move_shape = PLAYER1_SYMBOL
                    detected_move_shape = currentSymbol
                else:
                    detected_move_shape = None

            if detected_move_shape is not None and detected_move_shape == currentSymbol:
                board.make_move(i, currentSymbol)
                board_frame = draw_shape(board_frame, detected_move_shape, (x, y, w, h))
                history[i] = {'shape': detected_move_shape, 'ccords': (x, y, w, h)}

                # write players move
                write_move_to_file(currentSymbol.lower(), i)
                continue

        g_status = is_game_done(board)
        if g_status == 'Done':
            print('Game is over; Hit ESC to exit session')
            satisfactory_move = False

        # 7. Computer opponent to make move; make, record and write computer's move
        if computer_opponent and g_status != 'Done':
            # input('enter key')
            time.sleep(25)
            currentSymbol = update_current_player(currentSymbol)
            computer_move = determine(board, PLAYER2_SYMBOL, easy_mode=is_easy_opponent)
            board.make_move(computer_move, PLAYER2_SYMBOL)
            history[computer_move] = {'shape': 'O', 'ccords': move_slot_coords[computer_move]}
            board_frame = draw_shape(board_frame, 'O', move_slot_coords[computer_move])
            write_move_to_file(PLAYER2_SYMBOL.lower(), computer_move)

        currentSymbol = update_current_player(currentSymbol)
        message = True

        # 8. Check whether game has finished
        # if the game ended, then print a message
        # if the game didnt end, then keep playing
        g_status = is_game_done(board)
        if g_status == 'Done':
            print('Game is over; Hit ESC to exit session')
            satisfactory_move = False

        # hit ESC to exit live video feed
        if key == 27:
            cv2.destroyAllWindows()
            cap.release()
        # print(key)

    # hit ESC to exit live video feed
    # if key == 27:
    #     print(key, 'teeheetee')
    #     break
    #     exit


input('Hit Enter Key to end the session')
cv2.destroyAllWindows()
cap.release()
