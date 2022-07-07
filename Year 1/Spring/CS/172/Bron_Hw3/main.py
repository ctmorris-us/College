import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

import pygame
import abc
import random

from drawable import Block, Ball, Text, Line

if __name__ == '__main__':
    pygame.init()
    score = 0
    dt = .1
    g = -6.67
    R = .7
    eta = .5

    ball_list = []
    block_list = []

    height = 600
    width  = 600

    background = [Line(0, int(400), width, int(400)), Text()]

    play = True
    made_main_ball = False #remove anything with made_ball to get rid of the line

    num_blocks = 5
    size = 30
    for x_position in range(num_blocks):
        for y_position in range(num_blocks):
            block_list.append(Block(400 + size*x_position, 400 - size*y_position, size))



    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((height, width))


    while True:
        surface.fill((255,255,255))

        if play:
            mousex, mousey = pygame.mouse.get_pos()

            if len(ball_list) != 0:
                ball_list[-1].setX(mousex)
                ball_list[-1].setY(mousey)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and not made_main_ball:
                    made_main_ball = True
                    mousex, mousey = pygame.mouse.get_pos()
                    ball_list.append(Ball(mousex, mousey, (255,0,0)))
                    ball_list.append(Line(mousex, mousey, mousex, mousey))


                elif event.type == pygame.MOUSEBUTTONUP:
                    main_ball = ball_list[0]
                    drawing_line = ball_list[1]
                    main_ball.setVX(abs(main_ball.position()[0] - drawing_line.position()[0]))
                    main_ball.setVY(-1* abs(main_ball.position()[1] - drawing_line.position()[1]))
                    del ball_list[-1]
                    play = False
        else:
            pygame.event.get()

        if not play:
            main_ball = ball_list[0]
            if (abs(main_ball.getVY()) > .0001): # and (main_ball.position()[0] <= width): #If make go again uncomment

                new_y = main_ball.position()[1] + main_ball.getVY() * dt
                new_x = main_ball.position()[0] + main_ball.getVX() * dt

                main_ball.setY(new_y)
                main_ball.setX(new_x)

                if main_ball.getY() >= 400:
                    new_vx = main_ball.getVX() * eta
                    new_vy = main_ball.getVY() *  -R

                    main_ball.setVX(new_vx)
                    main_ball.setVY(new_vy)
                else:
                    new_vy = main_ball.getVY() - g*dt
                    main_ball.setVY(new_vy)


                bad_index = 0
                bad_ones = []
                for block in block_list:
                    if main_ball.intersect(block):
                        score += 1
                        bad_ones.append(bad_index)
                    bad_index += 1

                if len(bad_ones) != 0:
                    bad_ones.reverse()
                    for bad_index in bad_ones:
                        del block_list[bad_index]


        for ball in ball_list:
            ball.draw(surface)
        for block in block_list:
            block.draw(surface)
        for item in background:
            if isinstance(item, Text):
                item.draw(surface, score)
            else:
                item.draw(surface)

        pygame.display.update()
        clock.tick(40)
