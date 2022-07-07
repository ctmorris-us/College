import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

'''
Game Ideas

Roles:

Working with mouse and keyboard events
    Ties in with scenes; Mouse moves causing scene to moves
    Lighting

Building the Level
    Placing objects, projectiles, and whatnot

Building the Character

Creating environment for different objects
    How character interacts with each object


'''
from vpython import *
import numpy as np
import math as math

L = 3
cylinder_radius = .5
token_count = 10
tokens = []
i,j = 0,0

radius_sf = .5
height_sf = 30
width_sf = 30

token_piece_distance_sf = .00001

rate_op = 800
t = 0
dt = .001

top = vec(10, 1, 0)
zero = vec(0, 0, 0)

scene.center = vec(10,5,0)
autocenter = True
scene.range = 10

ball_x_distance = 20
ball_y_distance_true = 100
ball_y_distance = 10
xnum_parts = 5
ynum_parts = 10
x_p = int(ball_x_distance / xnum_parts)
y_p = int(ball_y_distance_true / ynum_parts)

piece = sphere (pos = vec(10,1,0), v = vec(0,0,0), a = vec(0,3,0), radius =
radius_sf, i = 0, j = 0, b = 0 , s = 0, rate = rate_op)


#y from 0 to 10
token1 = sphere (pos = vec(2,1,0), radius = .5, type = 0, color = color.cyan)

token2 = sphere (pos = vec(15,4,0), radius = .4, type = 0, color = color.cyan)

token3 = sphere (pos = vec(12,6,0), radius = .2, type = 0, color = color.cyan)

token4 = sphere (pos = vec(5,5,0), radius = .5, type = 0, color = color.cyan)

token5 = sphere (pos = vec(4,2,0), radius = .3, type = 0, color = color.cyan)

token6 = sphere (pos = vec(11,3,0), radius = .4, type = 0, color = color.cyan)

token_partitions = []

tokens_made = [token1, token2, token3, token4, token5, token6]

for j in range(ynum_parts):
    token_partitions.append([])

for y_partitions in token_partitions:
    for i in range(xnum_parts+1):
        y_partitions.append([])


def assign_partition(token):
    i_positive = math.floor((token.pos.x + token.radius) / x_p)
    i_negative = (math.floor(abs(token.pos.x - token.radius)/ x_p))

    j_positive = math.floor((token.pos.y + token.radius) / y_p)
    j_negative = (math.floor(abs(token.pos.y - token.radius) / y_p))



    token_partitions[j_positive][i_positive].append(token)
    if i_positive != i_negative:
        token_partitions[j_positive][i_negative].append(token)

    if j_positive != j_negative:
        token_partitions[j_negative][i_positive].append(token)
        if i_positive != i_negative:
            token_partitions[j_negative][i_negative].append(token)

for token in tokens_made:
    assign_partition(token)


def create_balls():
    for b in range(int(ball_y_distance_true/ynum_parts)):
        constant = ynum_parts * (b+1)
        for i in range(6):
            type = random()
            if type > .1:
                type = 0
                color_boi = color.cyan
            else:
                type = 1
                color_boi = color.orange

            radius = random() + .1
            if radius > 1:
                radius = 1

            assign_partition(sphere (pos = vec((int(ball_x_distance*random())),
            ((int(ball_y_distance*random())) + constant),0), radius = radius, type = type, color = color_boi, shape = 's'))


        piece.b = b
        yield b
create_balls = create_balls()

piece_partitions_x = []
piece_partitions_y = []

for j in range(ynum_parts+1):
    piece_partitions_y.append((y_p*j, j))
for i in range(-1,xnum_parts+3):
    piece_partitions_x.append((x_p*i, i))


boundRight = box(pos = vec(21, 49, 0),
                 height = 100,
                 width = 0.1,
                 length = 0.1,
                 up = vec(0, 1, 0),
                 color = color.white, shape = 'b')

boundLeft = box(pos = vec(-1, 49, 0),
                height = 100,
                width = 0.1,
                length = 0.1,
                up = vec(0, 1, 0),
                color = color.white, shape = 'b')

boundBottom = box(pos = vec(10, -1, 0),
                  height = 22,
                  width = 0.1,
                  length = 0.1,
                  up = vec(1, 0, 0),
                  color = color.white, shape = 'b')

boundTop = box(pos = vec(10, 100, 0),
                  height = 22,
                  width = 0.1,
                  length = 0.1,
                  up = vec(1, 0, 0),
                  color = color.blue, shape = 'b' )

box_list = [boundRight, boundLeft]

def delete_ball_bois(token):
    token.visible = False
    token.radius = .000001
    token.pos = vec(-2,-2,0)

def out_of_bounds():
    if piece.pos.y < boundBottom.pos.y:
        piece.pos = top
        piece.v = zero
        return True
    if abs((piece.pos.x + piece.radius) - (boundRight.pos.x - boundRight.length)) <= .0001 :
        #piece.pos = top
        piece.v = zero
        piece.s = 1
    if abs((piece.pos.x - piece.radius) - (boundLeft.pos.x + boundLeft.width)) <= .0001:
        #piece.pos = top
        piece.v = zero
        piece.s = 1

def slow_motion():
    piece.rate = 20
    return

# def anti_gravity():
#     return
#
# def small_boi():
#     piece.radius = .2
#     return

def increase_of_v_piece(keydown):
    if keydown.key == 'right':
        piece.a.x = 4
    if keydown.key == 'left':
        piece.a.x = -4

def decrease_of_v_piece(keyup):
    if keyup.key =='right':
        piece.a.x = 0
    if keyup.key == 'left':
        piece.a.x = 0

points = 0
def check_partitions_piece():
    if (piece.pos.x >= piece_partitions_x[piece.i+2][0]) and (piece.v.x >= 0):
        piece.i += 1

    elif (piece.pos.x <= piece_partitions_x[piece.i+1][0]) and (piece.v.x <= 0):
        piece.i -= 1

    elif (piece.pos.y >= piece_partitions_y[piece.j+1][0]) and (piece.v.y >= 0):
        piece.j += 1
        if piece.j == piece.b:
            next(create_balls)
        if piece.j >= 3:
            for x_partitions in token_partitions[piece.j-3]:

                for token_bois in x_partitions:
                    delete_ball_bois(token_bois)

    elif (piece.pos.y <= piece_partitions_y[piece.j][0]) and (piece.v.y <= 0):
        if piece.j == 0:
            piece.v = 0
            endBottom = text(text = ("Your score is: " + str(points)), align = 'center', pos = vec(50,20,0), color = color.red)
            scene.camera.pos = endBottom.pos + vec(0,0,21)
            scene.pause()
        piece.j -= 1


def collision(token):
    normalized_normal_vector = hat(piece.pos-token.pos)
    piece.v = piece.v + -2 * normalized_normal_vector.dot(piece.v) * normalized_normal_vector
    piece.v = piece.v * (1 + token.radius)

    if token.type > 0:
        if token.type == 1:
            slow_motion()
        elif token.type == 2:
            anti_gravity()
        elif token.type == 3:
            small_boi()

yPos = list(range(1,101))
def point_system():
    global points
    for index, y in enumerate(yPos):
        if y == int(piece.pos.y):
            points+=1
            yPos.pop(index)

def check_collision_piece():
    if piece.i == xnum_parts:
        token = box_list[0]
        if token.pos.x + token.length - piece.pos.x - piece.radius <= .0001:
            piece.v = 0
            endRight = text(text = ("Your score is: " + str(points)), align = 'center', pos = vec(50,20,0), color = color.red)
            scene.camera.pos = endRight.pos + vec(0,0,21)
            scene.pause()
    if piece.i == -1:
        token = box_list[1]
        if  piece.pos.x <= -.4:
            piece.v = 0
            endLeft = text(text = ("Your score is: " + str(points)), align = 'center', pos = vec(50,20,0), color = color.red)
            scene.camera.pos = endLeft.pos + vec(0,0,21)
            scene.pause()


    for token in token_partitions[piece.j][piece.i]:
        if mag(token.pos-piece.pos) - piece.radius - token.radius <= token_piece_distance_sf:
            collision(token)
            delete_ball_bois(token)
            break




#startup sequence
bouncy_boi = False
if bouncy_boi == False:
    start_up = text(text = "Welcome to Bouncy Boi!", align = 'center', pos = vec(10, -20, 0), color = color.white)
    info1 = text(text = "Use the left and right arrow keys to move.", align = 'center', pos = vec(10, -21.5, 0), color = color.white)
    info2 = text(text = "To slow things down, bounce on an orange ball.", align = 'center', pos = vec(10, -23, 0), color = color.orange)
    info3 = text(text = "Click anywhere to start.", align = 'center', pos = vec(10, -24.5, 0), color = color.white)
    scene.camera.pos = start_up.pos + vec(0,0,21)
    ev = scene.waitfor("click")
    if ev.event == "click":
        start_up.visible = False
        bouncy_boi = True
#end startup sequence




scene.bind('keydown', increase_of_v_piece)
scene.bind('keyup',decrease_of_v_piece)

next(create_balls)
next(create_balls)



while bouncy_boi == True:

    point_system()
    scene.caption = ("Points:",points)
    rate(piece.rate)

    scene.camera.pos = piece.pos + vec(0,0,21)

    check_partitions_piece()
    check_collision_piece()
    out_of_bounds()

    if piece.rate < rate_op:
        piece.rate = piece.rate + 10
    if piece.radius < radius_sf:
        piece.radius = piece.radius + .00000001
    piece.v = piece.v + piece.a * dt
    piece.pos = piece.pos + piece.v * dt

    if t == 1.5099999999999445:
        piece.a = vec(0,-3,0)

    t += dt
