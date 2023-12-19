from bge import logic



cont = logic.getCurrentController()
scene = logic.getCurrentScene()
objects = scene.objects

restartkey = cont.sensors['restartkey']
gameOver = objects["GameOver"]

if restartkey.positive and gameOver.visible == 1: 
    gameOver.visible = 0
    f = open("G:\My Drive\TicTacToe\\board.csv", "w")
    f.close()
    f = open("G:\My Drive\TicTacToe\GameStatus.txt", "w")
    f.close()      
    
    objects["Cross.1"].position.x = -43.0244 
    objects["Cross.1"].position.y = 68.4877 
    objects["Cross.1"].position.z = 7.5

    objects["Cross.2"].position.x = -50.9777 
    objects["Cross.2"].position.y = 68.4877 
    objects["Cross.2"].position.z = 7.5 

    objects["Cross.3"].position.x = -43.0244 
    objects["Cross.3"].position.y = 74.7025 
    objects["Cross.3"].position.z = 7.5 

    objects["Cross.4"].position.x = -50.9777 
    objects["Cross.4"].position.y = 74.7125 
    objects["Cross.4"].position.z = 7.5 

    objects["Cross.5"].position.x = -43.0244 
    objects["Cross.5"].position.y = 80.9373 
    objects["Cross.5"].position.z = 7.5 



    objects["Circle.1"].position.x = -50.9777 
    objects["Circle.1"].position.y = 80.9373 
    objects["Circle.1"].position.z = 7.5 

    objects["Circle.2"].position.x = -43.0244 
    objects["Circle.2"].position.y = 87.162 
    objects["Circle.2"].position.z = 7.5 

    objects["Circle.3"].position.x = -50.9777 
    objects["Circle.3"].position.y = 87.162 
    objects["Circle.3"].position.z = 7.5 

    objects["Circle.4"].position.x = -43.0244 
    objects["Circle.4"].position.y = 93.3868 
    objects["Circle.4"].position.z = 7.5 

    objects["Circle.5"].position.x = -50.9777 
    objects["Circle.5"].position.y = 93.3868 
    objects["Circle.5"].position.z = 7.5 
    
    print("Game Restarted")    
    