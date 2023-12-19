from bge import logic

cont = logic.getCurrentController()
scene = logic.getCurrentScene()
objects = scene.objects

twoplayerkey = cont.sensors['twoplayerkey']
startOptions = objects["StartOptions"]
quit = objects["Quit"]

if twoplayerkey.positive: 
    startOptions.visible = 0
    quit.visible = 1
    f = open("G:\My Drive\TicTacToe\GameMode.txt", "w")
    f.write("TwoPlayer")
    f.close()      
    print("Two Player")