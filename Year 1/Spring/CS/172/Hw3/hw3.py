import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
# My path variable with python is messed up, this is included so I can access pygames, but is edited out so it doesn't influence your python

'''
Name: Christopher Morris
Id: 14289223
'''

import pygame
import abc
import random

from user import BackgroundLine, UserObjects
from text import Text
from ball import Ball
from block import Block


'''
The program has the addition that it has a more realistic physics engine that better models collisions and bouncing
'''


if __name__ == '__main__':
    screen_height = 600
    screen_width  = 600
    ball_radius = 15
    block_size = 30
    num_blocks = 5
    dt = .1
    g = 6.67
    R = .7
    eta = .5

    pygame.init()
    User = UserObjects(screen_height, screen_width, ball_radius, block_size, num_blocks) #initiates the blocks and line
    surface = pygame.display.set_mode((screen_height, screen_width))

    clock = pygame.time.Clock()

    user_interact = True #Done to make sure the user can use the mouse
    made_ball = False #Once the ball is launched it is turned to false to keep user from messing with program

    while True:
        surface.fill((255,255,255))

        if user_interact: #Tests is user's actions should effect game
            mousex, mousey = pygame.mouse.get_pos()

            if len(User.getBalls()) != 0: #For the small green ball, moves the ball with the mouse
                User.getBalls()[-1].setX(mousex)
                User.getBalls()[-1].setY(mousey)

            if made_ball: #Makes sure the little green ball doesn't go beyond the line, meant to set limit of vy
                if mousey > User.getLine().getY():
                    pygame.mouse.set_pos(mousex, User.getLine().getY())
            else: #once the blue ball has been set the message no longer displays
                font = pygame.font.Font("freesansbold.ttf", 25)
                message = font.render("Click to and drag to launch ball.", True,(0, 0, 0))
                surface.blit(message, (screen_width/4, screen_height/4))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and not made_ball: #One user clicks the blue ball is placed at mouse location
                    mousex, mousey = pygame.mouse.get_pos()
                    User.setBalls(Ball(mousex, mousey, ball_radius))
                    User.setBalls(Ball(mousex, mousey, ball_radius - 10))
                    User.getBalls()[-1].setColor((0,255,0)) #makes smaller green ball that follows mouse as indicator
                    made_ball = True

                elif event.type == pygame.MOUSEBUTTONUP: #Once user lets go the distance between the two balls sets the vx and vy
                    User.getBalls()[0].setVX(abs(User.getBalls()[0].getX() - User.getBalls()[-1].getX()))
                    User.getBalls()[0].setVY(-1* abs(User.getBalls()[0].getY() - User.getBalls()[-1].getY()))
                    del User.getBalls()[-1]
                    user_interact = False
        else:
            pygame.event.get() #done just to get the events if the user doesn't do anything

        if not user_interact:
            if (abs(User.getBalls()[0].getVY()) > .0001) and (User.getBalls()[0].getX() <= User.getScreenWidth()): #if ball stops bouncing or leaves screen
                User.getBalls()[0].setVY(User.getBalls()[0].getVY() + g*dt) #Done to make a more realistic physics simulation
                User.getBalls()[0].setX(User.getBalls()[0].getX() + User.getBalls()[0].getVX() * dt)
                User.getBalls()[0].setY(User.getBalls()[0].getY() + User.getBalls()[0].getVY() * dt)

                if ((User.getBalls()[0].getY() + User.getBalls()[0].getRadius()) >= User.getLine().getY()) and (User.getBalls()[0].getVY() > 0):
                    User.getBalls()[0].setY(User.getLine().getY() - User.getBalls()[0].getRadius()) #checks to see if ball intersects with line
                    User.getBalls()[0].setVX(User.getBalls()[0].getVX() * eta)

                    if User.getBalls()[0].getVY() >= g*dt: #Included because the new physics messes with the velocity
                        User.getBalls()[0].setVY(User.getBalls()[0].getVY() *  -R) #If greater than the acceleraion that ball bounces
                    else:
                        User.getBalls()[0].setVY(0) #if the resulting velocity would not be greater than the acceleration then the balls stops

                for i, block in enumerate(User.getBlocks()): #tests for collisions and deletes block
                    if User.getBalls()[0].get_intersection(block):
                        User.incrementScore()
                        del User.getBlocks()[i]
            else: #once the ball stops moving repeats so the user can continue
                user_interact = True
                made_ball = False
                del User.getBalls()[0]

        for o in User.getObjects(): #draws objects
            o.draw(surface)


        pygame.display.update()
        clock.tick(40)
