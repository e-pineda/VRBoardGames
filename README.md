# VRBoardGames

NOTE: Please install Google Drive for desktop. Once done, this will create a directory called "G:\My Drive\" on your machine. In that directory, create a folder called "TicTacToe" and populate said folder with three empty files: board.csv, GameStatus.txt and GameMode.txt. These files are how the VR and Computer Vision components communicate to one another. 
Here's a link offering guidance on this task: https://support.google.com/drive/answer/10838124?hl=en


Also, here's a report explaining our project: https://docs.google.com/document/d/1byRqBKa7IiX0Wc4QQ1mNew1SFi11p3Zw/edit?usp=sharing&ouid=112616462046538216374&rtpof=true&sd=true


A demo video for our project: https://drive.google.com/file/d/1DWJwIGtPGcsbmzFBtDZMj8eLrwhxADJZ/view?usp=sharing


A presentation for our project: https://drive.google.com/file/d/1patP26iwCHg_QD6k1pjEs021mdojdRSM/view?usp=drive_link



## CV & Game Component
### Installation
To run the computer vision script, you MUST be using Python 3.9. Next, run the following command to install the necessary libraries:
    pip install -r requirements.txt


While the packages are being installed, please take the time to prepare your hardware. A web camera, piece of paper with a Tic-Tac-Toe grid drawn on it and a writing instrument are all needed. 
Make sure the piece of paper with a Tic-Tac-Toe grid drawn on it is entirely within the vision of the webcamera. The only visible object to the webcamera should be the playable board.
Also ensure there is ample lighting in the room with no shadows being cast on the Tic-Tac-Toe grid. For a reference, please note the hardware setup at 4:19 in the following video: https://drive.google.com/file/d/1DWJwIGtPGcsbmzFBtDZMj8eLrwhxADJZ/view?usp=sharing

### Running the script
When everything is set up, run TicTacToePlayer.py to begin the computer vision script. Please note that our game isn't resilient to failure yet. So, when you are playing, take care to ensure that piece of paper with a Tic-Tac-Toe grid drawn on it is the only object visible to the webcamera. You are able to draw your respective symbol on the board, but for the sake of your game, make sure to remove your hand and writing instrument from the camera's vision after you're done making your move.


To change the computer opponent's difficulty, go to the TicTacToePlayer.py file and set is_easy_opponent to True.


To turn the AI move detector off, go to the TicTacToePlayer.py file and set AI_move_detection_mode to False.

### Experimenting with the AI move Detector
If you are interested in retraining or experimenting with the CNN, please run TicTacToeClassifier.py file. NOTE: you must unzip the data folder as it contains the training and test data.

### Issues
If there any issues, please check that the whole board is within the vision of the webcamera, there is ample lighting on the board (no shadows or darkness should be on the board). 
Plase note that currently, the only way to fix a wrong prediction made by the AI move detector is to restart the game. If you are experiencing issues with the AI detector, feel free to turn it off.


## UI Component

### Installation

Download and install Blender 3.6 and UPBGE 0.36.1

Blender 3.6: https://www.blender.org/download/lts/3-6/

UPBGE 0.36.1: https://upbge.org/#/download

### Download Source Code

Blender code: https://github.com/e-pineda/VRBoardGames/blob/main/UI_Components/BlenderCode.txt

Python code: https://github.com/e-pineda/VRBoardGames/tree/main/UI_Components/PythonScripts

### Download 

We use the blender add-on poliigon.

Download: https://www.poliigon.com/blender

Download Image Files for the 3D Model of the Hand: 

https://drive.google.com/file/d/1-v0LF4qYrMbK_QcpWg-JgSLHwuEmRvhV/view?usp=sharing

https://drive.google.com/file/d/1-ya2Ymsz3Hysx3BrfYmJ_L5sXk7-mC2Q/view?usp=sharing


### Running Blender Code

1. Open TicTacToeVR.blend in UPBGE
2. Install the add-on for poliigon
3. You may be missing some of the files needed by the add-ons. To fix this, go to File --> External Data --> Find Missing Files and navigate to the directory where the poliigon add-on has been installed and select "Find Missing Files" button. Navigate to the directory where you saved the 3D Model of the Hand and select "Find Missing Files" button as well.
   
![Import Missing File](images/ImportMissingFile.jpg "Import Missing File")

4. Run UPBGE game engine by selecting Standalone Start as shown below.
![Start Gaming Engine](images/StartUPBGE.jpg "Start Gaming Engine")

### Troubleshooting

1. If the game engine runs and generates the UI but does not respond to the user commands, there is an issue with the Logic Bricks setup. Check if the script name referenced in the Logic Bricks section matches that in the Text editor as shown below.
![Troubleshoot](images/Troubleshoot.jpg)
