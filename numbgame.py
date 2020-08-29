#!/usr/local/bin/python3
import random
import time

count=0

print("Hello There!\n")
time.sleep(2)
n=input("Enter Your Name -- \n")
time.sleep(1)
print(("Cool name ;) "+n.swapcase()+"!!!\n"))
time.sleep(3)
print("Lets Begin...\n")
time.sleep(2)
print("There are '4' numbers in a list...(1 through 9)\n")
time.sleep(5)
print("All you have to do is guess the numbers one by one\n")
time.sleep(5)
print("THE INDEXING OF NUMBERS IS AS FOLLOWS ----")
time.sleep(4)
print("1ST NUMBER = '0'\n2ND NUMBER = '1'\n3RD NUMBER = '2'\n4TH NUMBER = '3'")
time.sleep(4)
print("DONT GET CONFUSED!!\n")
time.sleep(4)
print("Remember... Numbers in every position in the list are always random (no repetitions). So when you try next time, numbers wont be the same.\n")
time.sleep(5)
print("And dont worry... we are not cheating.. you can see the list in the end :D\n")
time.sleep(5)
print("Get Ready...\n")

def gen():
    a=[random.randint(1,9),random.randint(1,9),random.randint(1,9),random.randint(1,9)]
    for x in a:
        if a.count(x)>1:
            a=gen()
    return a

a=gen()
#print a
time.sleep(3)

print(("Ok "+n.capitalize()+", the list is ready... START GUESSING!!! ;)\n"))
print("Have Fun!\n\n")
time.sleep(3)

def guess(x):
    time.sleep(2)
    try:
        global a
        global count
        if x in a:
            print("Correct!\n")
            print("Position of your number is in")
            print((a.index(x)))
            count+=1
            print("\n")
        else:
            print("OOPS! Wrong Guess :( )\n")
    except:
        exit("wtf")

b=eval(input("Guess the 1st number--\n"))
guess(b)

c=eval(input("Guess the 2nd number--\n"))
guess(c)

d=eval(input("Guess the 3rd number--\n"))
guess(d)

e=eval(input("Guess the 4th number--\n"))
guess(e)

time.sleep(2)
print("No of correct guesses out of 4- ")
print(count)
print("\n\n\n")
time.sleep(2)
print("Actual List ---")
time.sleep(2)
print(a)
print("\n")
time.sleep(2)
print((n.capitalize()+" your Result -- "))
time.sleep(2)
if(count==1):
    print("Poor Guesses")
elif(count==2):
    print("Not Bad")
elif(count==3):
    print("Good...just miss")
elif(count==4):
    print("You deserve a cookie, Mister")
else:
    print("You suck at guessing :(")
