"""
planet_data.py

Space wars game where you can fire at enemy ships using missiles.
Enemies have 3 lives each and crashing.
Defeat enemies by either shooting them or colliding into them (directly in the center).
Speed up using up arrow; Slow down and or stop/reverse using down arrow.
Turn spaceship left/right with left/right arrow keys.
Fire missiles using space bar. Good luck!

Author: Gierado Pham
Date: 2024-08-20
"""

import os
import random

# Import turtle module
import turtle
# For MacOSX, needed to show animation window
turtle.fd(0)
# Set animation speed, 0 = maximun
turtle.speed(0)
# Set background color
turtle.bgcolor("black")
# Hide default turtle, that automatically gets created
turtle.ht()
# Save memory
turtle.setundobuffer(1)
# Speeds up drawing
turtle.tracer(2)

# Draw spaceship using coordinates
spaceship_shape = (
    (0, 25),   
    (-2, 23),   
    (-2, 5),   
    (-8, 5),  
    (-15, 0),  
    (-30, -5),  
    (-30, -10), 
    (-30, 20), 
    (-32, 20), 
    (-32, -10),  
    (-10, -10),  
    (-10,-20),
    (-3,-20),
    (-3,-10),
    (0,-10),
    (3, -10),   
    (3, -20),  
    (10, -20),  
    (10, -10),  
    (32, -10),   
    (32, 20),   
    (30, 20),    
    (30, -10),   
    (30, -5),   
    (15, 0),  
    (8, 5),   
    (2, 5),    
    (2, 23),   
    (0, 25)    
)

# Register the custom shape with turtle
turtle.register_shape("spaceship", spaceship_shape)

#
class Sprite(turtle.Turtle):
    def __init__(self,spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self,shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx,starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    # Detectin collision
    def collision(self,other):
        if (self.xcor() >= (other.xcor() - 20)) and \
            (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)) and \
            (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False
    

class Player(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.speed = 4
        self.lives = 3
    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.lt(-45)
    
    def accelerate(self):
        self.speed+= 1

    def deccelerate(self):
        self.speed+= -1

class Enemy(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

class Missile(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3,stretch_len=0.4,outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "firing"
    
    def move(self):
        if self.status == "firing":
            self.fd(self.speed)
        if self.status == "ready":
            self.goto(-1000,1000)

        # Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000,1000)
            self.status = "ready"


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
    
    def draw_border(self):
        # Draw Border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
# Create game object
game = Game()

#Draw game border
game.draw_border()

# Create sprites
player = Player("spaceship","white",0,0)
enemy1 = Enemy("circle","red",-100,0)
enemy2 = Enemy("circle","blue",-200,0)
enemy3 = Enemy("circle","green",-300,0)
missile = Missile("triangle","yellow",0,0)

# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.deccelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# Main game loop
while True:
    player.move()
    enemy1.move()
    enemy2.move()
    enemy3.move()
    missile.move()

    # Collision detection system
    x = random.randint(-250,250)
    y = random.randint(-250,250)
    collision_1 = 0
    collision_2 = 0
    collision_3 = 0
    if player.collision(enemy1):
        enemy1.goto(x,y)
        collision_1 += 1
        if collision_1 == 3:
            enemy1.reset()
    if player.collision(enemy2):
        enemy2.goto(x,y)
        collision_2 += 1
        if collision_2 == 3:
            enemy2.reset()
    if player.collision(enemy3):
        enemy3.goto(x,y)
        collision_3 += 1
        if collision_3 == 3:
            enemy3.reset()

    if missile.collision(enemy1):
        enemy1.goto(x,y)
    if missile.collision(enemy2):
        enemy2.goto(x,y)
    if missile.collision(enemy3):
        enemy3.goto(x,y)

delay = input("Press enter to finish. >")