from vpython import *
import sys

m=1.0 # By definition
star=[]
trail=[]
acc=[]

# Create two stars with a center of mass at the origin
star.append(sphere(radius=0.2,pos=vec(1,0,0),color=color.yellow))
trail.append(curve(pos=[star[0].pos],color=star[0].color))
star[0].v=vec(0,0.5,0)

star.append(sphere(radius=0.2,pos=vec(-1,0,0),color=color.blue))
trail.append(curve(pos=[star[1].pos],color=star[1].color))
star[1].v=vec(0,-0.5,0)

thirdStar=False
U=-0.5 # By default
alpha=0.2 # How fast is the incoming star?
if (len(sys.argv) > 1):
    alpha=float(sys.argv[1])

v0=alpha*sqrt(2*abs(U))

scene.range=12
scene.autoscale=0
scene.width=1000
scene.height=1000
print("Click on the LHS position to place a third (horizontal) star")
while (thirdStar == False):
    ev=scene.waitfor('mousedown')
    if ev.event == 'mousedown':
        star.append(sphere(radius=0.2,pos=ev.pos,color=color.red))
        trail.append(curve(pos=[star[2].pos],color=star[2].color))
        star[2].v=vec(v0,0,0)
        thirdStar=True
    
for i in range(len(star)):
    acc.append(vec(0,0,0))

dt=0.01
t=0
tmax=100
eps=0.01 # A force smoother


while(t < tmax):
    rate(1/dt)
    for i in range(len(star)):
        acc[i]=vec(0,0,0)
        for j in range(len(star)):
            if (i != j):
                acc[i]+=-(star[i].pos-star[j].pos)/pow(mag(star[i].pos-star[j].pos)+eps,3)
    for i in range(len(star)):
        star[i].pos+=star[i].v*dt
        star[i].v+=acc[i]*dt
        trail[i].append(star[i].pos)
    t+=dt

