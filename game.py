#!/usr/local/bin/python3
import time
import pygame

pygame.init()

#Screen size, title, color etc
screenWidth = 1366
screenHeight = 768
Display = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Don't cross the line!")
Display.fill((255,255,255))

#FPS of movement
clock = pygame.time.Clock()
FPS = 30

#No. of blocks to be moved
blockSize = 20

#Communication with user
font = pygame.font.SysFont(None,25)
def message(msg,color):
    text=font.render(msg, True, color)
    Display.blit(text,[screenWidth/4.5,screenHeight/2.8])


#Main logic and event handling
def gameLoop():

    gameOver = False
    gameExit = False


    #Initial position of rectangle
    x=screenWidth/2
    y=screenHeight/2

    #New position of rectangle
    x1 = 0
    y1 = 0

    x2=screenWidth/2
    y2=screenHeight/2

    x3=0
    y3=0

    while not gameExit:
        while gameOver == True:
            Display.fill((255,255,255))
            message("Game over. You literally crossed the line this time! ['r' to restart or 'q' to close]".upper(), (255,0,0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False


                    if event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y1=y1-blockSize
                    y3=y3-blockSize
                elif event.key == pygame.K_DOWN:
                    y1=y1+blockSize
                    y3=y3+blockSize
                elif event.key == pygame.K_LEFT:
                    x1=x1-blockSize
                    x3=x3-blockSize
                elif event.key == pygame.K_RIGHT:
                    x1=x1+blockSize
                    x3=x3+blockSize
                elif event.key == pygame.K_SPACE:
                   x1=0
                   y1=0
                   x3=0
                   y3=0

        x=x+x1
        y=y+y1
        x2=x2+x3
        y2=y2+y3

    #Setting boundaries
        if x >= screenWidth or y >= screenHeight or x<=0 or y<=0:
            gameOver = True


        Display.fill((255,255,255))
        pygame.draw.rect(Display,(0,0,0),[x,y,blockSize,blockSize])
        pygame.display.update()

        clock.tick(FPS)


    pygame.quit()
    quit()

gameLoop()
