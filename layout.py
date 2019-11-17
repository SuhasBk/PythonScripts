#!/usr/bin/python3
from tkinter import *
import tkinter

root = Tk()
root.configure(bg='black')
root.geometry("1366x768")
root.title('Saavn')
centy=768/2-70
centx=1366/2-120

font = ('Ubuntu',15,'normal')

def delete(event):
    f.place(x=centx+50,y=centy-200)
    b.destroy()


f=Frame(root)
#f.configure(bg='black')

l = Label(root,text='Welcome to Saavn...',font=('Ubuntu Condensed',20,'bold','italic'))
b = Button(root,text='Start?',font=font)
b1 = Button(f,text='Play',font=font,bg='green',fg='white')
b2 = Button(f,text='Pause',font=font,bg='green',fg='white')
b3 = Button(f,text='Next Song',font=font,bg='green',fg='white')
b4 = Button(f,text='Previous Song',font=font,bg='green',fg='white')

b.bind('<Button-1>',delete,add=True)

l.grid(padx=centx)
b.grid(pady=centy,padx=centx)
b1.grid(pady=20)
b2.grid(pady=20)
b3.grid(pady=20)
b4.grid(pady=20)

root.mainloop()
