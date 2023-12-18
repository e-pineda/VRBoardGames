# VRBoardGames

**CV & Game Component**

To run our program, you must run the computer vision (CV) script and the blender script simultaneously.

To run the computer vision script, you MUST be using Python 3.9. Next, run the following command to install the necessary libraries:


pip install -r requirements.txt



While the packages are being installed, please take the time to prepare your hardware. A web camera, piece of paper with a Tic-Tac-Toe grid drawn on it and a writing instrument are all needed. 
Make sure the piece of paper with a Tic-Tac-Toe grid drawn on it is entirely within the vision of the webcamera. The only visible object to the webcamera should be the playable board.
Also ensure there is ample lighting in the room with no shadows being cast on the Tic-Tac-Toe grid. For a reference, please reference the hardware setup at 4:19 in the demo: https://drive.google.com/file/d/1DWJwIGtPGcsbmzFBtDZMj8eLrwhxADJZ/view?usp=sharing


When everything is set up, run TicTacToePlayer.py to begin the computer vision script. 


To change the computer opponent's difficulty, go to the TicTacToePlayer.py file and set is_easy_opponent to True.


To turn the AI move detector off, go to the TicTacToePlayer.py file and set AI_move_detection_mode to False.


If you are interested in retraining or experimenting with the CNN, please run TicTacToeClassifier.py file. 


If there any issues, please check that the whole board is within the vision of the webcamera, there is ample lighting on the board (no shadows or darkness should be on the board). 
Plase note that currently, the only way to fix a wrong prediction made by the AI move detector is to restart the game.  

**UI Component**
