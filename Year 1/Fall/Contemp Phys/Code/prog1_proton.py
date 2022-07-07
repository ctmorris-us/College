from vpython import *



class Quark:
    def __init__(self, position, color, type, charge):
        self.position = position
        self.type = type
        if self.type == 'up':
            axis = vec(0,.2,0)
        elif self.type == 'down':
            axis = vec(0,-.2,0)
        else:
            axis = vec(0,0,0)
        self.axis = axis
            #exec('sc = color.{}'.format(str(color)))
            #Weird error with inputing strings
        self.color = color
            #c = cone(radius=.1, axis = self.axis, color = self.color)
            #s = sphere(radius=.1, color = self.color)
            #self.quark = compound([c,s], pos = vec(*position), color = self.color, radius = .5)
        self.quark = arrow(pos = vec(*position), color = self.color,
        axis = self.axis, shaftwidth = .2, headwidth = .3)
        self.txt = text(text = '{}'.format(charge), pos = vec(*position) + vec(.2,0,0),
        allign = 'center', billboard = True, depth = 0, height = .1)



class Proton:
    def __init__(self):
            self.proton = sphere(opacity = .3, shininess = 0)
            self.txt = text(text = 'Proton', pos = vec(-.5,1.2,0),
            allign = 'center', billboard = True, depth = 0, height = .3)


a = Proton()
quarks = [Quark((.5,-.3,-.2),color.red, 'up', '+2/3'), Quark((-.3,.5,-.2), color.blue, 'down', '-1/3'),
         Quark((-.3,-.2,.5), color.green, 'up', '+2/3')]
