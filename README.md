# VRBoardGames

**CV & Game Component**
#### Installation
To run the computer vision script, you MUST be using Python 3.9. Next, run the following command to install the necessary libraries:
    pip install -r requirements.txt


While the packages are being installed, please take the time to prepare your hardware. A web camera, piece of paper with a Tic-Tac-Toe grid drawn on it and a writing instrument are all needed. 
Make sure the piece of paper with a Tic-Tac-Toe grid drawn on it is entirely within the vision of the webcamera. The only visible object to the webcamera should be the playable board.
Also ensure there is ample lighting in the room with no shadows being cast on the Tic-Tac-Toe grid. For a reference, please note the hardware setup at 4:19 in the following video: https://drive.google.com/file/d/1DWJwIGtPGcsbmzFBtDZMj8eLrwhxADJZ/view?usp=sharing

#### Running the script
When everything is set up, run TicTacToePlayer.py to begin the computer vision script. Please note that our game isn't resilient to failure yet. So, when you are playing, take care to ensure that piece of paper with a Tic-Tac-Toe grid drawn on it is the only object visible to the webcamera. You are able to draw your respective symbol on the board, but for the sake of your game, make sure to remove your hand and writing instrument from the camera's vision after you're done making your move.


To change the computer opponent's difficulty, go to the TicTacToePlayer.py file and set is_easy_opponent to True.


To turn the AI move detector off, go to the TicTacToePlayer.py file and set AI_move_detection_mode to False.

#### Experimenting with the AI move Detector
If you are interested in retraining or experimenting with the CNN, please run TicTacToeClassifier.py file. NOTE: you must unzip the data folder as it contains the training and test data.

#### Issues
If there any issues, please check that the whole board is within the vision of the webcamera, there is ample lighting on the board (no shadows or darkness should be on the board). 
Plase note that currently, the only way to fix a wrong prediction made by the AI move detector is to restart the game. If you are experiencing issues with the AI detector, feel free to turn it off.


**UI Component**
