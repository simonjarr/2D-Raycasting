from tkinter import *
import numpy as np
import random as rn

# needed functions

# ray-block collision computing
def collisionRB(ray,blocks,event,coords):
    my_min=2000
    no_hit=True
    (x1r,y1r,x2r,y2r)=myC.coords(ray)
    (x1,y1,x2,y2)=coords
    for i in range(len(blocks)):
        (xb1,yb1,xb2,yb2)=myC.coords(blocks[i])
        d=(x1-x2)*(yb1-yb2)-(y1-y2)*(xb1-xb2)
        if d!=0:
            t=((x1-xb1)*(yb1-yb2)-(y1-yb1)*(xb1-xb2))/d
            u=-((x1-x2)*(y1-yb1)-(y1-y2)*(x1-xb1))/d
            if t<1 and t>0 and u<1 and u>0:
                p1=x1+t*(x2-x1)
                p2=y1+t*(y2-y1)
                dist = np.linalg.norm(np.array([p1-x1r,p2-y1r]))
                if dist<my_min:
                    my_min=dist
                    myC.coords(ray,x1r,y1r,p1,p2)
                    no_hit=False
    if no_hit:
        myC.coords(ray,x1r,y1r,x2,y2) 

# mouse movement tracker
def motion_func(event):
    pos_=myC.coords(lightS)
    pos=np.array([(pos_[0]+pos_[2])/2,(pos_[1]+pos_[3])/2])
    myC.move(lightS,event.x-pos[0],event.y-pos[1])
    for i in range(ray):
        l_coords[i]=(l_coords[i][0]+event.x-pos[0],l_coords[i][1]+event.y-pos[1],l_coords[i][2]+event.x-pos[0],l_coords[i][3]+event.y-pos[1])
        myC.move(l[i],event.x-pos[0],event.y-pos[1])
        collisionRB(l[i],l_B,event,l_coords[i])

# some constants
width=640
height=480
ox=250 
oy=250
r=10
xy1=[ox-r,oy-r]
xy2=[ox+r,oy+r]

root =Tk() # set up root window

myC=Canvas(root,width=width,height=height, background="black") # create Canvas

lightS=myC.create_oval(xy1,xy2, fill="white") # create "light source"

# more constant related to the rays and blocks
pi=3.14
ray=360
div=360/ray
block_n=7

# pre-allocate necessary memory for arrays
l=np.empty(ray,dtype=Canvas) # rays
l_B=np.empty(block_n,dtype=Canvas) # blocks
l_coords=np.empty(ray,dtype=list) # coordinates

# create random blocks
for i in range(len(l_B)):
    l_B[i] = myC.create_line(rn.randint(0,width),rn.randint(0,height),rn.randint(0,width),rn.randint(0,height),fill="white") 

# create initial ray lines
for i in range(ray):
    xy1=[1*np.sin(i*div*pi/180)+250,20*np.cos(i*div*pi/180)+250]
    xy2=[2000*np.sin(i*div*pi/180)+250,2000*np.cos(i*div*pi/180)+250]
    l[i]=myC.create_line(xy1,xy2,fill="white")
    l_coords[i]=myC.coords(l[i])

# pack the canvas to root
myC.pack()

# bind mouse movement event to root
root.bind("<Motion>",motion_func)

# run mainloop
root.mainloop()
