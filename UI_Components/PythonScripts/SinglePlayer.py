from bge import logic

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
objects = scene.objects

singleplayerkey = cont.sensors['singleplayerkey']
startOptions = objects["StartOptions"]
quit = objects["Quit"]

if singleplayerkey.positive: 
    startOptions.visible = 0
    quit.visible = 1    
    f = open("G:\My Drive\TicTacToe\GameMode.txt", "w")
    f.write("SinglePlayer")
    f.close()      
    print("Single Player")