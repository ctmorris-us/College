from vpython import *
import sys

def addPt(ev):
    pts.append(sphere(radius=0.02,pos=ev.pos,v=vec(-ev.pos.y*omega,ev.pos.x*omega,0)))



m1=1.0 # By definition, the mass of the first star
m2=0.03 # everything else is defined in terms of this
if (len(sys.argv) > 1):
    m2=float(sys.argv[1])

# Create two stars with a center of mass at the origin
star1=sphere(radius=0.1*m1,pos=vec(m2/m1,0,0),color=color.yellow)
star1.rpos=mag(star1.pos)
trail1=curve(pos=[star1.pos],color=star1.color)

star2=sphere(radius=0.1*sqrt(m2/m1),pos=vec(-1,0,0),color=color.green)
star2.rpos=mag(star2.pos)
trail2=curve(pos=[star2.pos],color=star2.color)
scene.range=2
scene.autoscale=0
scene.width=1000
scene.height=800
scene.bind('mousedown', addPt)

# test particles
pts=[]

# Compute the angular frequency
mtot=m1+m2
omega=sqrt(m1**3/(star2.rpos**3*(mtot)**2))
print('Omega='+str(omega))

dt=0.002
t=0
tmax=100



while(t < tmax):
    rate(.1/dt)
    star1.pos=vec(star1.rpos*cos(omega*t),star1.rpos*sin(omega*t),0)
    trail1.append(star1.pos)
    star2.pos=-vec(star2.rpos*cos(omega*t),star2.rpos*sin(omega*t),0)
    trail2.append(star2.pos)

    for i in range(len(pts)):
        pts[i].pos+=pts[i].v*dt
        acc1=-m1*(pts[i].pos-star1.pos)/pow(mag(pts[i].pos-star1.pos),3)
        acc2=-m2*(pts[i].pos-star2.pos)/pow(mag(pts[i].pos-star2.pos),3)
        pts[i].v+=(acc1+acc2)*dt

    t+=dt
