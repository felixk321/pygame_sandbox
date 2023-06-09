from scenes.abstract import BaseScene
from pymunk import Space, Vec2d
from components.floor import Segment
from components.terrain import Terrain, TerrainBlock
from components.tank import Tank, Ammo
from pygame import Surface, KEYDOWN, K_SPACE, Vector2
from pygame.event import Event
import pygame
from typing import Sequence, List
from utils import convert
from components.animation import Animation



class TankScene(BaseScene):
    def __init__(self) -> None:
        self.space = Space()
        self.space.gravity = (0,-1000)

        
        self.terrain = Terrain(1500, 5, 100, 100, self.space)
        self.tank = Tank(Vec2d(100,190), self.space)
        self.init_pos = self.tank.tb.body.position

        self.explosion = Animation("./assets/tank_explosion_animation.png", 64, Vector2(256,256))

        self.bullets:List[Ammo] = []

    def handle_event(self, event:Event) ->None:
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not self.explosion.running:
                ammo = self.tank.fire()
                explosion_pos = convert(ammo.body.position, 750)
                self.bullets.append(ammo)
                self.explosion.start(Vector2(explosion_pos) + Vector2(0,-150))



    def handle_pressed_keys(self, keys: Sequence[bool])-> None:
        if keys[pygame.K_a]:
            self.tank.move(-1)
            
        
        if keys[pygame.K_d]:
            self.tank.move(1)
            
        if keys[pygame.K_DOWN]:
            self.tank.update_gun_angle(-0.01)
        if keys[pygame.K_UP]:
                self.tank.update_gun_angle(0.01)

    def get_camera_shift(self, display: Surface)-> Vec2d:
        h = display.get_height()
        return  (self.init_pos - convert(self.tank.tb.body.position, h)) *-1
        

    def update(self, display: Surface)->None:
        self.space.step(1/60)
        self.tank.rw.motor.rate *= 0.98
        camera_shift = self.get_camera_shift(display)
        self.terrain.update(camera_shift.x)
        self.explosion.update()
    
    def render(self, display: Surface)->None:
        display.fill((255,255,255))
        

        camera_shift = self.get_camera_shift(display)
        
        print(camera_shift)
        self.terrain.render(display, camera_shift.x)
        self.tank.render(display, camera_shift.x)
        for bullet in self.bullets:
            bullet.render2(display, camera_shift.x)
        self.explosion.render(display, camera_shift.x)
        

    

    
