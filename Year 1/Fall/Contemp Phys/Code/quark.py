from vpython import *
import numpy.random as random

def quark(type='up',color=color.red,pos=vec(random.random()-0.5,random.random()-0.5,random.random()-0.5)):
    if (type == 'up'):
        myaxis=vec(0.2,0,0)
    else:
        myaxis=vec(-0.2,0,0)
    myarrow=cone(radius=0.1,axis=myaxis,color=color)
    mysphere=sphere(radius=0.1,color=color,opacity=0.5)
    myquark=compound([myarrow,mysphere])
    myquark.pos=pos
    myquark.v=0.25*vec(random.random()-0.5,random.random()-0.5,random.random()-0.5)
    myquark.radius=mysphere.radius
    myquark.axis=vec(0,1,0)
    myquark.type=type
    return myquark

neutron=sphere(opacity=0.3)
q=[]
q.append(quark(type='up',color=color.red))
q.append(quark(type='down',color=color.blue))
q.append(quark(type='down',color=color.green))

dt=0.2
tmax=1500
t=0
tau=881.5
mytext = label(text='t=0.0', align='center', color=color.green,pos=vec(-2.0,1.5,0),height=20,box=False)
scene.autoscale=0

isDecayed=False
while (t<tmax):
    rate(100)
    for i in range(len(q)):
        q[i].pos+=q[i].v*dt
        vout=q[i].pos.dot(q[i].v)/mag(q[i].pos)
        if (mag(q[i].pos) > 1-q[0].radius) and (vout > 0) and (q[i].type != 'lepton'):
            # Bounce
            q[i].v=q[i].v-2*vout*q[i].pos/mag(q[i].pos)
    # Do we decay:
    if (isDecayed == False) and (random.random() < dt/tau):
        print("decay!",t)
        isDecayed=True
        mytext.color=color.red
        neutron.color=vec(1,0.8,0.8)
        q[2].axis=-q[2].axis
        nhat=vec(random.random(),random.random(),random.random())
        nhat=nhat/mag(nhat)
        v0=0.02
        q.append(sphere(radius=0.05,pos=q[2].pos,v=v0*nhat,type='lepton'))
        q.append(sphere(radius=0.05,pos=q[2].pos,v=-v0*nhat,type='lepton'))
    t+=dt
    if (isDecayed==False):
        mytext.text='t='+str(round(t,1))
