from pygame.surface import Surface
from pymunk import Space, Body, Poly, Shape
import pygame
from utils import convert



class Rectangle:
    def __init__(self, x: float, y: float, width: int, height: int, space: Space) -> None:
        self.body = Body()
        self.body.position = x , y
        
        self.shape = Poly(self.body,vertices = ((-width/2,-height/2), (-width/2, height/2), (width/2,height/2),(width/2,-height/2)))
        self.shape.density = 1
        space.add(self.body,self.shape)


    def render(self, display:Surface)->None:
        h = display.get_height()
        
        points = [

            convert(self.body.local_to_world(v),h)
            for v in self.shape.get_vertices()
        ]
        
        pygame.draw.polygon(display,(0,255,0),points)