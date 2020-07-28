#!/usr/bin/python3
import turtle
import time

x=-500
y=330

def init():
    global x
    global y
    #turtle.clear()
    turtle.title("WOO-HOO")
    turtle.setup(1366,768,0,0)
    turtle.speed(5)
    turtle.hideturtle()
    turtle.up()
    turtle.goto(x,y)
    turtle.pensize(5)
    turtle.bgcolor("black")
    turtle.pencolor("white")

def square():
    turtle.write("I am here",font=('Times New Roman','20','bold italic'))
    global x
    a=x
    while(a<=100):
        turtle.down()
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(100)
        turtle.right(90)
        (a,b)=turtle.pos()
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(100)
        turtle.up()        #Comment for the diagonal line...
        turtle.goto(a,b)
        turtle.right(90)
    #turtle.up
    turtle.left(90)
    turtle.forward(100)
    turtle.down()
    turtle.write("I am here now",font=('Times New Roman','20','bold italic'))

def dance():
    def circles(r):
        turtle.goto(0,0)
        turtle.down()
        turtle.showturtle()
        turtle.circle(r)
        turtle.down()
        turtle.left(90)
        turtle.forward(2*r)
        turtle.right(180)
        turtle.forward(r)
        turtle.right(90)
        turtle.forward(r)
        turtle.right(180)
        turtle.forward(2*r)
        turtle.up()

    turtle.write("\nGOTO CMD OR TERMINAL!",font=('Monospace','20','bold'))
    a=eval(input("Enter the starting radius of pattern\n"))
    b=eval(input("Enter the last radius of pattern\n"))
    c1=input("Enter the color of the pen\n")
    c2=input("Enter your favorite color(surprise)\n")

    turtle.pencolor(c1)
    turtle.speed(10)

    for r in range(a,b,10):
        #init()
        #r=200 #input("enter radius\n")
        circles(-r)
        circles(r)
        turtle.right(90)
        circles(r)
        circles(-r)

        turtle.down()
        turtle.pencolor(c2)
        turtle.pensize("8")

        turtle.right(-45)
        turtle.forward(turtle.sqrt(pow((2*r),2)+pow((2*r),2)))
        turtle.left(135)
        turtle.forward(2*r)
        turtle.left(135)
        turtle.forward(turtle.sqrt(pow((2*r),2)+pow((2*r),2)))
        turtle.left(-135)
        turtle.forward(2*r)
        turtle.right(90)
        turtle.forward(2*r)
        turtle.right(90)
        turtle.forward(2*r)
        turtle.right(90)
        turtle.forward(2*r)
        turtle.up()
        turtle.goto(0,0)

        turtle.pencolor(c1)
        turtle.pensize("5")

def animate(x,y,len):
    turtle.hideturtle()
    turtle.speed(0)
    def square(len):
        turtle.forward(len)
        turtle.right(90)
        turtle.forward(len)
        turtle.right(90)
        turtle.forward(len)
        turtle.right(90)
        turtle.forward(len)
        turtle.seth(0)
        turtle.up()

    for i in range(10,300,20):
        turtle.up()
        turtle.clear()
        turtle.goto(x+i,y-i)
        turtle.down()
        turtle.circle(25)
        square(len)


init()
dance()
animate(x,y,100)


turtle.exitonclick()
