import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint
from components.floor import Segment
from utils import convert
from components.catapult import Catapult
pygame.init()

display = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
h = display.get_height()

bullets = []

space = pymunk.Space()
space.gravity = (0,-1000)





catapult = Catapult(250,300,75,space)

line = Segment((0,100),(500,100),5,space)




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                catapult.reload()
            

        

        
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        catapult.move_arm()
    if pressed_keys[pygame.K_SPACE]:
        catapult.shot()
    if pressed_keys[pygame.K_d]:
        catapult.move(-1)
    if pressed_keys[pygame.K_a]:
        catapult.move(1)
    catapult.update_motor_rate()

    
    ammo = catapult.detach_ammo()
    if ammo:
        bullets.append(ammo)
    
    display.fill((255,255,255))

    
        


    line.render(display)
    catapult.render(display)

    for b in bullets:
        b.render(display)

    

    
    
    

    
    

    pygame.display.update()
    space.step(1/60)
    clock.tick(60)

        


