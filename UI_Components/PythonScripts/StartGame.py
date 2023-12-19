import os
import csv
import time
import sys

from bge import logic

cont = logic.getCurrentController()
scene = logic.getCurrentScene()

objects = scene.objects

startgamekey = cont.sensors['startgamekey']
startScreen = objects["StartScreen"]
startOptions = objects["StartOptions"]


if startgamekey.positive: 
    startScreen.visible = 0   
    startOptions.visible = 1
 
