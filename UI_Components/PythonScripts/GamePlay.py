
from bge import logic
import os
import csv
import time
import sys

directory = "G:\My Drive"
filename = "board.csv"

board = os.path.join(directory, filename)

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
objects = scene.objects

startScreen = objects["StartScreen"]
startOptions = objects["StartOptions"]
hand = objects["Hand"]

if startScreen.visible == 0 and startOptions.visible == 0:

    cross_cnt = 1
    circle_cnt = 1
    with open(board, "r") as openfile:
        mycsv = csv.reader(openfile, delimiter=',')
        for record in mycsv:
            type,row,column = record
            if type == "x":
                piece = objects["Cross." + str(cross_cnt)] 
                cross_cnt = cross_cnt + 1  
            if type == "o":
                piece = objects["Circle." + str(circle_cnt)] 
                circle_cnt = circle_cnt + 1 
                             
            #print("Board." + str(row) + "." + str(column))      
            board_position = objects["Board." + row + "." + column]
            
            diff = board_position.position.x - piece.position.x
            if abs(diff) > 2:
                if diff > 0:                
                    piece.position.x = piece.position.x + 2            
                else:
                    piece.position.x = piece.position.x - 2 

            else:
                piece.position.x= board_position.position.x

            diff = board_position.position.y - piece.position.y
            if abs(diff) > 2:
                if diff > 0:
                    piece.position.y = piece.position.y + 2
                else:
                    piece.position.y = piece.position.y - 2
            else:
                piece.position.y= board_position.position.y

 
            diff = board_position.position.z - piece.position.z
            if abs(diff) > 2:
                if diff > 0:
                    piece.position.z = piece.position.z + 2
                else:
                    piece.position.z = piece.position.z - 2 
            else:
                piece.position.z = board_position.position.z


            if piece.position.x == board_position.position.x and piece.position.y == board_position.position.y and piece.position.z == board_position.position.z:
                hand.visible = 0
            else:
                hand.visible = 1
                hand.position.x = piece.position.x            
                hand.position.y = piece.position.y            
                hand.position.z = piece.position.z + 1           
                
    openfile.close() 
    
    f = open("G:\My Drive\GameStatus.txt", "r")

    if f.read() == "Done":
        gameOver = objects["GameOver"]
        gameOver.visible = 1
            
    f.close()
        