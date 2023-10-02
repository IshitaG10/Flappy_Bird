#!C:\Users\ishit\OneDrive\Desktop\Projects\Python_Projects\Flappy_Bird\myenv\Scripts\python.exe
import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 35


screen_width  = 447
screen_height = 490

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93',30)

#define colors
white = (255, 255, 255)

#defining game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 80
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() -pipe_frequency #when the last pipe was created- in the beginning no pipe is created and we here assign the initial time
score = 0
pass_pipe = False

#loading images
bg = pygame.image.load('bg.png')
ground = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


#creating sprite class for bird
class Bird(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        # controls the speed at which the animation runs
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity acting on the bird
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 400:
                self.rect.y += int(self.vel)
        
        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -6
            

            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True and game_over == False:
                self.clicked = False
            

            #handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]


            #rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)            


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        self.rect.topleft = [x,y]
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]

    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: #once the pipe has gone off the screen the pipe is removed from the memory
            self.kill()


class Button:
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):

        action = False

        #get maouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


#group is like a python list
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Bird(100,int(screen_height/2))
bird_group.add(flappy)


#create restart button instance
button = Button(screen_width//2 - 50, screen_height//2-100, button_img)


game_on = True
while game_on:

    clock.tick(fps)

    #draw background
    screen.blit(bg,(0,0))


    #draw is a default function in sprite class and group
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    

    #draw the ground
    screen.blit(ground,(ground_scroll,400))


    #check the score
    if len(pipe_group)> 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
         and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
         and pass_pipe == False:
            pass_pipe = True
        
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width/2),20)

    #checking collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #check if bird has hit the ground
    if flappy.rect.bottom >= 400:
        game_over = True
        flying = False 

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-80,80)
            btm_pipe = Pipe(screen_width,int(screen_height / 2) + pipe_height,-1)
            top_pipe = Pipe(screen_width,int(screen_height / 2) + pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #scroll ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 22:
            ground_scroll = 0
            
        pipe_group.update()


    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False:
            flying = True

    pygame.display.update()

pygame.quit()