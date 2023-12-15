import keras
from src.Board import Board
from src.TicTacToeClassifier import reshape_input
from src.image_processing import *
from src.utils import *

# leverages CNN to detect if the user made a move in the given cell
def detect_user_movement(grid_cell):
    mapper = {0: 'O', 1: 'None', 2: 'X'}
    print(grid_cell)
    grid_cell = reshape_input(grid_cell)
    idx = np.argmax(loaded_model.predict(grid_cell))
    return mapper[idx]

# writes the made move to the file
def write_move_to_file(player_symbol, move_pos):
    FILEPATH = "G:\My Drive\TicTacToe\\board.csv"
    TEST_FILEPATH = 'board.csv'
    if move_pos == 0:
        move = f'{player_symbol}, 0, 0\n'
    elif move_pos == 1:
        move = f'{player_symbol}, 0, 1\n'
    elif move_pos == 2:
        move = f'{player_symbol}, 0, 2\n'
    elif move_pos == 3:
        move = f'{player_symbol}, 1, 0\n'
    elif move_pos == 4:
        move = f'{player_symbol}, 1, 1\n'
    elif move_pos == 5:
        move = f'{player_symbol}, 1, 2\n'
    elif move_pos == 6:
        move = f'{player_symbol}, 2, 0\n'
    elif move_pos == 7:
        move = f'{player_symbol}, 2, 1\n'
    elif move_pos == 8:
        move = f'{player_symbol}, 2, 2\n'

    with open(FILEPATH, 'a') as file:
        file.write(move)

# Instantiate Board obj for the game as well dictionary to track game history
board = Board()
history = {}
message = True

# Set player's symbols for the game
player_symbol = 'X'
computer_symbol = 'O'

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
is_easy_opponent = False


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
    if message:
        print(f'Available moves: {board.available_moves()}')
        if AI_move_detection_mode:
            print('Make move, then press spacebar\n')
        else:
            print('Enter move, then press spacebar\n')
        message = False
    if key != 255:
        if key != 32 and key >= 48 and key < 57:
            movePos = key - 48
    if not key == 32:
        continue

    # 6. Determine player's position if AI_move_detection_mode is true, make, record & write player's move
    available_moves = board.available_moves()
    for i, (x, y, w, h) in enumerate(move_slot_coords):
        if i not in available_moves:
            continue
        if AI_move_detection_mode:
            if x < 0:
                slot_img = img_thresh[int(y): int(y + h), int(x+w): int(x)]
            else:
                slot_img = img_thresh[int(y): int(y + h), int(x): int(x + w)]
            detected_move_shape = detect_user_movement(slot_img)
        else:
            if i == movePos:
                detected_move_shape = player_symbol
            else:
                detected_move_shape = None

        if detected_move_shape is not None and detected_move_shape == player_symbol:
            board.make_move(i, player_symbol)
            board_frame = draw_shape(board_frame, detected_move_shape, (x, y, w, h))
            history[i] = {'shape': detected_move_shape, 'ccords': (x, y, w, h)}
            detected_user_move = True

            # write players move
            write_move_to_file(player_symbol, i)

    # 7. Computer opponent to make move; make, record and write computer's move
    computer_move = determine(board, computer_symbol, easy_mode=is_easy_opponent)
    board.make_move(computer_move, computer_symbol)
    history[computer_move] = {'shape': 'O', 'ccords': move_slot_coords[computer_move]}
    live_grid = draw_shape(board_frame, 'O', move_slot_coords[computer_move])
    write_move_to_file(computer_symbol, computer_move)

    message = True

    # 8. Check whether game has finished
    # if the game ended, then print a message
    # if the game didnt end, then keep playing
    if board.complete():
        if board.O_won() and player_symbol == 'O':
            print('Congrats you won!')
        elif board.X_won() and player_symbol == 'X':
            print('Congrats you won!')
        elif board.X_won() and player_symbol != 'X':
            print('Haha you lose!')
        elif board.O_won() and player_symbol != 'O':
            print('Haha you lose!')
        elif board.tied():
            print('You tied!')
        break
    cv2.imshow('Populated board', board_frame)

    # hit ESC to exit live video feed
    if cv2.waitKey(5) & 0xFF == 27:
        cv2.destroyAllWindows()
        cap.release()

