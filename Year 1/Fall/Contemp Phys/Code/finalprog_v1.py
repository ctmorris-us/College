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

Powerups: Slowmotion, Make ball bigger, Anti-gravity

Lives: 3 Lives

Scoring:

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

collision_recoil_factor = 1

rate_op = 800
t = 0
dt = .001

#token_paritions = np.array()
    #list of tokens per partition

#partitions = np.array()...
# Make sure that the partitions account for spheres where their radi plus the radi of the piece
# Are in the appropriate partition

#scene.center = vec(0,L,0)

piece = sphere (pos = vec(0,6,0), v = vec(0,0,0), a = vec(0,-3,0), radius =
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

token1 = sphere (pos = vec(0,4,0), radius = .5, type = 0)
token2 = sphere (pos = vec(3,1,0), radius = .5, type = 0)
token3 = sphere (pos = vec(5,-1,0), radius = .5, type = 0)

token_paritions = [[token1,token2,token3]]

def slow_motion():
    piece.rate = 200
    return

def anti_gravity():
    return

def big_boi():
    piece.radius = 3
    return

def scroll_up():
    delete(token_paritions[piece.j])
    return

def scroll_down():
    return

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
    piece.v = collision_recoil_factor * piece.v + -2 * normalized_normal_vector.dot(piece.v) * normalized_normal_vector

    if piece.radius > radius_sf:
        piece.radius -= .2

    if token.type > 0:
        if token.type == 1:
            slow_motion()
        elif token.type == 2:
            anti_gravity()
        elif token.type == 3:
            big_boi()



def check_collision_piece():
    for token in token_paritions[piece.i]:
        if mag(token.pos-piece.pos) - piece.radius - token.radius <= token_piece_distance_sf:
            collision(token)

'''
def increase_slow_motion(keydown):
    if keydown.key == 'w':
        if piece.rate > 200:
            piece.rate -= 200

def decrease_slow_motion(keyup):
    if keyup.key == 'w':
        piece.rate = 800
'''

scene.bind('keydown', increase_of_v_piece)
scene.bind('keyup',decrease_of_v_piece)
# scene.bind('keydown', increase_slow_motion)
# scene.bind('keyup', decrease_slow_motion)


while True:
    rate(piece.rate)

    check_collision_piece()

    if piece.rate < 800:
        piece.rate += 20

    piece.v = piece.v + piece.a * dt
    piece.pos = piece.pos + piece.v * dt

    t += dt

## Slow motion Stop###
#
