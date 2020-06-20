import turtle
import time
from tkinter import *

def main(self):
    
    l = [turtle.RawTurtle(self.canvas) for i in range(4)]
    c=['#961208','#919607','#0E4F15','#0817D6']

    for i,tu in enumerate(l):
        tu.pensize(20)
        tu.speed(0)
        tu.pencolor(c[i])


    s=l[0].getscreen()
    s.bgcolor('#292921')
    s.tracer(1,0)
        

    for i in l:
        i.pu()
        i.backward(200)
        i.lt(90)
        i.fd(100)
        i.rt(90)
        i.pd()
    l[0].lt(70)
    l[0].penup()
    l[0].fd(90)


    l[1].lt(115)
    l[1].penup()
    l[1].fd(100)


    l[2].lt(165)
    l[2].penup()
    l[2].fd(140)


    l[3].lt(190)
    l[3].penup()
    l[3].fd(140)


    a=[70,115,165,190]

    for i,tu in enumerate(l):
        tu.hideturtle()
        tu.rt(a[i])

    for tu in l:
        tu.speed(0)

    for tu in l[:2]:
        tu.pd()
        tu.rt(110)
        tu.fd(200)
    
    for tu in l[2:]:
        tu.pd()
        tu.fd(200)

    tu=l[0]
    tu.pu()
    tu.fd(20)
    tu.lt(110)
    tu.pensize(0)
    tu.fd(150)
    tu.pd()
    tu.color('springgreen')
    tu.write('CodeBeaters',font=('candara',60,'bold'))

