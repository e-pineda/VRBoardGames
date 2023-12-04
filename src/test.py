import cv2
import keras
import numpy as np
from src.Board import Board
from src.TicTacToeClassifier import reshape_input
from src.image_processing import *
from src.utils import *
import math
import pickle


def detect_user_movement(grid_cell):
    mapper = {0: 'O', 1: 'None', 2: 'X'}
    print(grid_cell)
    grid_cell = reshape_input(grid_cell)
    idx = np.argmax(loaded_model.predict(grid_cell))
    return mapper[idx]


board = Board()
history = {}
player_symbol = 'X'
computer_symbol = '0'
message = True
AI_mode = False
outputFile = ''

if AI_mode:
    model_path = 'model/TicTacToeClassifier.h5'
    loaded_model = keras.models.load_model(model_path)

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
# server_ip = "127.0.0.1"
# server_port = 6666

cap = cv2.VideoCapture(0)
while cap.isOpened():

    ret, frame = cap.read()
    key = cv2.waitKey(1) & 0xFF

    cv2.imshow('Live Original Video Feed', frame)

    gray_frame = to_gray_scale(frame)
    cv2.imshow('Manipulated Video Feed', gray_frame)

    # # draw circles at board's corners
    board_frame = find_and_mark_board_boundary(frame, gray_frame)
    # cv2.imshow('Boundary with Circles', board_frame)

    # find playable grid & moveslots on board
    board_frame, img_thresh, move_slot_coords = find_board(board_frame)
    cv2.imshow('Boundary with Circles', board_frame)

    # Draw grid and wait until user makes a move
    for i, (x, y, w, h) in enumerate(move_slot_coords):
        cv2.rectangle(board_frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
        if history.get(i) is not None:
            shape = history[i]['shape']
            board_frame = draw_shape(board_frame, shape, (x, y, w, h))
    cv2.imshow('Populated board', board_frame)

    if message:
        print('Make move, then press spacebar')
        message = False
    if key != 255:
        if key != 32 and key >= 48 and key < 57:
            movePos = key - 48
            print(movePos)
    if not key == 32:
        # cv2.imshow('original', frame)
        # cv2.imshow('bird view', paper)
        continue

    available_moves = np.delete(np.arange(9), list(history.keys()))
    for i, (x, y, w, h) in enumerate(move_slot_coords):
        if i not in available_moves:
            continue
        if AI_mode:
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

        # print(f'{detected_move_shape} move detected at {i}')
        if detected_move_shape is not None and detected_move_shape == player_symbol:
            board.make_move(i, player_symbol)
            board_frame = draw_shape(board_frame, detected_move_shape, (x, y, w, h))
            history[i] = {'shape': detected_move_shape, 'ccords': (x, y, w, h)}
            detected_user_move = True

    # Computer's time to play
    computer_move = determine(board, computer_symbol)
    board.make_move(computer_move, computer_symbol)
    history[computer_move] = {'shape': 'O', 'ccords': move_slot_coords[computer_move]}
    live_grid = draw_shape(board_frame, 'O', move_slot_coords[computer_move])

    message = True
    board_state = board.get_board_state()
    s = ', '.join(move if move is not None else 'None' for move in board_state) + '\n'
    outputFile += s

    # Check whether game has finished
    if board.complete():
        break

    # # FOR CLIENT - SERVER COMMUNICATION # # #
    # ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY),30])
    # x_as_bytes = pickle.dumps(buffer)
    # s.sendto((x_as_bytes),(server_ip,server_port))

    # hit ESC to exit live video feed
    if cv2.waitKey(5) & 0xFF == 27:
        break

with open("outputFile.txt", 'w') as file:
    file.write(outputFile)

cv2.destroyAllWindows()
cap.release()