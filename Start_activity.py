from tkinter import *
import loading_animation as ani
import time

class Interface:
    def __init__(self,obj):
        self.window=obj.window
        self.window.attributes('-fullscreen',1)
        self.wn_width,self.wn_height=self.window.maxsize()


        self.canvas = Canvas(self.window,height=self.wn_height,width=self.wn_width,bd=0,highlightthickness=0)
        self.canvas.place(x=0,y=0)

        ani.main(self)
        time.sleep(3)
        self.canvas.destroy()



if __name__=='__main__':
    i=Interface()
