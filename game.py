import os
from turtle import left
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,250)#This section allows setting the window position on the monitor

from guizero import App, Text, TextBox, Box, PushButton, Picture
#skeleton for game states
from enum import Enum
import pgzrun
import tkinter
import random
from pgzero import clock
class State(Enum):
    START = 1
    RUN = 2
    CRASH = 3
    GAME_END = 4
 
class SpaceObject:
    player = Actor("rocket", center=(440,320))#Our player
    asteroid = Actor("asteroid",center=(100,-64))#Supposed to dodge this object
    playerName = ''
    passed = 0
    explosions = 0
    POSITION = random.randint(100,570)
    BLOCK_FLAG = False
    MOVING = []
    COLLISION = []
    state = State.RUN
    animations = []
    clocks = []
    leaders=[]
WIDTH=720
HEIGHT=600

def asteroid_move():
    global BLOCK_FLAG, animations
    if not SpaceObject.BLOCK_FLAG:
        SpaceObject.BLOCK_FLAG = True
        SpaceObject.POSITION = random.randint(100,570)#Randomly throwing asteroids in any position on the screen
        lane = SpaceObject.POSITION
        asteroid = Actor("asteroid",(lane,-64))#Making asteroid actors
        SpaceObject.MOVING.append((asteroid,lane))#Making the asteroids move
        SpaceObject.animations.append(animate(asteroid,pos=(lane, HEIGHT//3),duration=.8,
                on_finished=finish_move))#Adding it to the list of asteroids
 
def finish_move():
    global BLOCK_FLAG, animations
    asteroid = SpaceObject.MOVING[-1]
    SpaceObject.BLOCK_FLAG = False
    SpaceObject.animations.append(animate(asteroid[0],pos=(asteroid[1],HEIGHT+64),duration=.8,
            on_finished=clear_moving))
 
def clear_moving():
    global passed
    SpaceObject.passed +=1 #Incrementing by 1 for the asteroids passed
    while len(SpaceObject.MOVING) > 4:
        SpaceObject.MOVING.pop(1)
 
def handle_collision():
    setup_state(State.CRASH)#Setting up the crash feature
    sounds.rocketflying.stop()#Background noise
    sounds.crash.play()#This is the crash noise
    clock.schedule_unique(changetoend, 3)#Showing the right time for the crash
    for cb in SpaceObject.clocks:
        clock.unschedule(cb)
    explode_asteroid()
 
def explode_asteroid():
    SpaceObject.explosions +=1#Adding 1 to the number of explosions
    if SpaceObject.explosions <= 8 :
        SpaceObject.player.image="explosion_"+str(SpaceObject.explosions)#Showing the explosion
        clock.schedule(explode_asteroid, 0.125)#Putting the sound in the correct time
 
def setup_start():
    fontSize = 14 #Making the font size to 14
 
    def clicked():
        setup_state(State.RUN)#Uploading the game into setup_state()
        x.destroy()#Destroying the main window
 
    x = App(layout="grid", width=350) # Making a new window grid for the game
    x.when_closed = clicked
    x.bg = "white"
    logo = Picture(x, image="images/spaceEscapeLogo.png", grid=[0,0], align = "right")
    label = Text(x, text="Enter your Name: ",grid=[0,1],size=fontSize, align="left")#Putting some text into the game
    name = TextBox(x, grid=[0,1], width=12, align="right")#Making a textbox for you to type your name in
    name.text_size = fontSize
    howToPageText = Text(x, text="\n\nHow to play this game:\n\nUse arrow keys to move the rocket,\ndodge the asteroids, and score points.\n\n",grid=[0,8],size=fontSize)#Making the how to play page
    startButton = PushButton(x,text="Start the Game!",grid=[0,16], command=clicked)#Making a button to start the game
    startButton.text_size=fontSize
    name.focus()
    x.display()#Displaying the window
    SpaceObject.playerName = name.value
 
def setup_run():
    # run the setup needed for the RUN state
    SpaceObject.player = Actor("rocket", center=(440,320))#Making your player
    SpaceObject.asteroid = Actor("asteroid",center=(100,-64))#Making an asteroid(The object you have to dodge)
    SpaceObject.passed = 0#Showing the number of asteroids passed
    SpaceObject.explosions = 0#Showing the number of explosions you had
    SpaceObject.BLOCK_FLAG = False
    SpaceObject.MOVING = []#A list of asteroids
    SpaceObject.COLLISION = []#List of asteroids that you had a collision with
    SpaceObject.state = State.RUN#Running the game
    clock.schedule_interval(asteroid_move, 0.6)#Showing how fast the asteroid is going to move at
    sounds.rocketflying.play(-1)#Playing the background noise
 
def update_run():
    global passed, COLLISION#Making these variables global
   
    if keyboard.right:#Defining the right key
        animate(SpaceObject.player,duration = 0.5,angle = -20)
        SpaceObject.player.x = min(477,SpaceObject.player.x+2)
    elif keyboard.left:#Defining the left key
         animate(SpaceObject.player,duration = 0.5,angle = 20)
         SpaceObject.player.x = max(SpaceObject.player.x-2,291)
    elif keyboard.up:#Defining the up key
        SpaceObject.player.y -=2
    elif keyboard.down:#Defining the down key
        SpaceObject.player.y += 2
    else:
         animate(SpaceObject.player,duration=.1, angle = 0.0)
           
# Collision and passed asteroids routine
    for asteroid in SpaceObject.MOVING:
        if SpaceObject.player.colliderect(asteroid[0]):
            if len(SpaceObject.COLLISION) == 0:
                SpaceObject.COLLISION.append((SpaceObject.player,asteroid[0]))
                clock.schedule(handle_collision,.5)
                break
 
def draw_run():
    global passed 
    screen.fill((0,0,0))#Making the screen black
    screen.blit("background.png",(0,0))#Displaying the background image
    SpaceObject.player.draw()#Drawing the rocket
    for asteroid in SpaceObject.MOVING:#Drawing the asteroids
        asteroid[0].draw()
    screen.draw.text(" Asteroids Passed: "+str(SpaceObject.passed),(22,32))#Showing the amount of asteroids passed
 
def setup_crash():#Running the crash state
    """
    run the setup needed for the CRASH state
    """
 
def changetoend():
    setup_state(State.GAME_END)#Programming the game end code
   
def setup_game_end():
    fontSize = 14
    player = SpaceObject.playerName#Assigning the player name to the variable
 
    def restart():
        setup_state(State.RUN)#Running the program
        x.destroy()#Restarting the game after you died
 
    def closeGame():
        x.destroy()#Closing the game completely
 
    x = App(layout="grid")#Making the game window
    x.when_closed = closeGame
 
    leaderScores = [("Jenine",91), ("Rian",76), ("Joe", 43)]#Setting up a leaderboard
    leaderScores.append((player, SpaceObject.passed - 3))#Appending your name and score
    leaderScores.sort(key=lambda i: i[1], reverse=True)#Sorting the list by your score
 
    board = Box(x, grid = [1,1],border=2)#Making the board
    heading = Text(board,"Leaderboard", size=fontSize)#Making the heading for the leaderboard
    for leaderScore in leaderScores:
         t = Text(board, text=f'{leaderScore[0]}\t{leaderScore[1]}', size=fontSize)#Displaying the names and scores on the leaderboard

    restartButton = PushButton(x,text="Reset Game",grid=[8,5],command=restart)#Making a button to restart the game
    endButton = PushButton(x, text="End Game", grid=[4,5], command=exit)#Making a button to exit the game
    x.display()#Running the game
 
def setup_state(state):
    if state == State.START:#Starting the game
        setup_start()
    elif state == State.RUN:#Running the game
        setup_run()
    elif state == State.CRASH:#Setting up the crash
        setup_crash()
    else:
        setup_game_end()#Setting up the ending of the game
    return

setup_state(State.START)# start the game in the START STATE  
 
def update():#Updating the values of run, crash, and the ending of the game
    global state
    if SpaceObject.state == State.RUN:
        update_run()
    if SpaceObject.state == State.CRASH:
        update_crash()
    if SpaceObject.state == State.GAME_END:
        update_game_end()
   
def draw():#Drawing the program
    global state
    if SpaceObject.state == State.RUN:
        draw_run()
    if SpaceObject.state == State.CRASH:
        draw_crash()
    if SpaceObject.state == State.GAME_END:
        draw_game_end()
pgzrun.go()#Runs all of the code