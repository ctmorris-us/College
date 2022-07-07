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

#token_paritions = np.array()
    #list of tokens per partition

#partitions = np.array()...
# Make sure that the partitions account for spheres where their radi plus the radi of the piece
# Are in the appropriate partition

scene.center = vec(10,5,0)
autocenter = True
scene.range = 10


piece = sphere (pos = vec(10,1,0), v = vec(0,0,0), a = vec(0,3,0), radius =
radius_sf, i = 0, j = 0, rate = rate_op)


'''
for i in range(token_count):
    a = -1 if (random() > .5) else 1

    i = sphere(pos = vec(a*random()*(width_sf-radius_sf),random() * (height_sf-radius_sf),0))

    i.radius = random() * radius_sf

    if i.radius < .2*radius_sf:
        i.radius = .2*radius_sf
        i.color = color.red
    elif i.radius < .4*radius_sf:
        i.radius = .4*radius_sf
        i.color = color.blue
    elif i.radius < .6*radius_sf:
        i.radius = .6*radius_sf
        i.color = color.green
    else:
        i.radius = 1*radius_sf
        i.color = color.magenta
####Make checking system to make sure that the spheres don't intercept
### Get scene correct
    tokens.append(i)
'''

token1 = sphere (pos = vec(8,4,0), radius = .5)
token2 = sphere (pos = vec(3,1,0), radius = .5)
token3 = sphere (pos = vec(5,6,0), radius = .5)
token4 = sphere (pos = vec(2,7,0), radius = 0.5)
token5 = sphere (pos = vec(17,5,0), radius = 0.5)
token6 = sphere (pos = vec(10,9,0), radius = 0.5)

token_paritions = [[token1,token2,token3,token4,token5,token6]]

#Joe Code
boundRight = box(pos = vec(21, 19, 0),
                 height = 40,
                 width = 0.1,
                 length = 0.1,
                 up = vec(0, 1, 0),
                 color = color.white)

boundLeft = box(pos = vec(-1, 19, 0),
                height = 40,
                width = 0.1,
                length = 0.1,
                up = vec(0, 1, 0),
                color = color.white)

boundBottom = box(pos = vec(10, -1, 0),
                  height = 22,
                  width = 0.1,
                  length = 0.1,
                  up = vec(1, 0, 0),
                  color = color.white)

boundTop = box(pos = vec(10, 11, 0),
               height = 22,
               width = 0.1,
               length = 0.1,
               up = vec(1, 0, 0),
               visible = False)

def out_of_bounds():
    if piece.pos.y < boundBottom.pos.y:
        piece.pos = top
        piece.v = zero
        return True
    if piece.pos.x > boundRight.pos.x:
        piece.pos = top
        piece.v = zero
        return True
    if piece.pos.x < boundLeft.pos.x:
        piece.pos = top
        piece.v = zero
        return True

def randomize_tokens():
    if out_of_bounds():
        counter = -1
        for i in token_paritions[0]:
            counter += 1
            token_paritions[0][counter].pos.x = int(20 * random())
            token_paritions[0][counter].pos.y = int(10 * random())
            for j in token_paritions[0]:
                if i.pos.x == j.pos.x or i.pos.y == j.pos.y:
                    randomize_tokens()


'''
def move_up():
    if
'''
#end Joe code

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

def check_partitions_piece():
    if (piece.pos.x >= partitions[piece.i+1][piece.j]) and (piece.v.x >= 0):
        piece.i += 1
    elif (piece.pos.x <= partitions[piece.i-1][piece.j]) and (piece.v.x <= 0):
        piece.i -= 1
    elif (piece.pos.y >= partitions[piece.i][piece.j+1]) and (piece.v.y >= 0):
        piece.j += 1
    elif (piece.pos.y <= partitions[piece.i][piece.j-1]) and (piece.v.y <= 0):
        piece.j -= 1

def collision(token):
    normalized_normal_vector = hat(piece.pos-token.pos)
    piece.v = piece.v + -2 * normalized_normal_vector.dot(piece.v) * normalized_normal_vector
    piece.v = piece.v * (1 + token.radius - piece.radius)

    # del token

def check_collision_piece():
    for token in token_paritions[piece.i]:
        if mag(token.pos-piece.pos) - piece.radius - token.radius <= token_piece_distance_sf:
            collision(token)
            break         
    token.visible = False
    del token

def increase_slow_motion(keydown):
    if keydown.key == 'w':
        if piece.rate > 200:
            piece.rate -= 200

def decrease_slow_motion(keyup):
    if keyup.key == 'w':
        piece.rate = 800


scene.bind('keydown', increase_of_v_piece)
scene.bind('keyup',decrease_of_v_piece)
scene.bind('keydown', increase_slow_motion)
scene.bind('keyup', decrease_slow_motion)


while True:
    rate(piece.rate)

    scene.camera.pos = piece.pos + vec(0,0,20)

    check_collision_piece()

    randomize_tokens()

    out_of_bounds()

    piece.v = piece.v + piece.a * dt
    piece.pos = piece.pos + piece.v * dt

    if t == 1.5099999999999445:
        piece.a = vec(0,-3,0)

    t += dt

## Slow motion Stop

#I need to set a bound, like a tube in which that game will be contained
