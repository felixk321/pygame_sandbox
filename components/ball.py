import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint
from utils import convert
from math import sin, cos,radians

class Ball:
    def __init__(self, coord: Tuple[int, int], r: int , s: pymunk.Space) -> None:
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, r)
        self.body.position = coord
        #self.body.velocity_func = self.limit_velocity

        self.radius = r
        self.lifetime = 255
        self.shape.density = 1
        self.shape.friction = 1
        self.shape.elasticity = .5
        s.add(self.body, self.shape)

    def limit_velocity(self, body, gravity, damping, dt):
        max_velocity = 500
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale
        
    
    def render(self, display: pygame.Surface):
        h = display.get_height()

        start_pos = convert(self.body.position, h)
        alpha = radians(self.body.angle)
        end_pos = convert(self.body.local_to_world((self.radius * sin(alpha),self.radius * cos(alpha) )), h)

        pygame.draw.circle(display, (240,60,80), convert(self.body.position, h), self.radius)
        pygame.draw.line(display,(0,0,0), start_pos, end_pos, 1 )

    def render2(self, display: Surface, shift_x: float)->None:
        h = display.get_height()
        pos = pygame.Vector2(*convert(self.body.position, h)) - pygame.Vector2(shift_x, 0)
        pygame.draw.circle(display, (240,60,80), pos, self.radius)

        start_pos = pos
        alpha = radians(self.body.angle)
        end_pos = convert(self.body.local_to_world((self.radius * sin(alpha),self.radius * cos(alpha) )), h)

        end_pos = pygame.Vector2(end_pos) - pygame.Vector2(shift_x, 0)
        pygame.draw.line(display,(0,0,0), start_pos, end_pos, 1 )


