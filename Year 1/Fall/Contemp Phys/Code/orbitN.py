from vpython import *
import sys

# The key parameters

n=2.
v0=1.

# python orbitN [N,v0]

if (len(sys.argv) > 1):
    n=float(sys.argv[1])
    if (len(sys.argv) > 2):
        v0=float(sys.argv[2])


sun=sphere(radius=0.1,color=color.yellow)
earth=sphere(pos=vec(1,0,0),radius=0.05,color=color.red)
earth.v=vec(0,v0,0) 
c=curve(color=color.red,pos=[earth.pos])
scene.range=3
scene.autoscale=0


dt=0.01
t=0

while (t < 100):
    rate(300)
    t+=dt
    acc=-earth.pos/pow(mag(earth.pos),n+1)
    earth.v+=acc*dt
    earth.pos+=earth.v*dt
    c.append(earth.pos)


