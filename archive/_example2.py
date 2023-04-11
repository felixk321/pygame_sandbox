import pygame
from pygame.surface import Surface
import pymunk
from typing import Tuple, List
from random import randint

pygame.init()

display = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
h = display.get_height()

space = pymunk.Space()
space.gravity = (0,-1000)




class Ball:
    def __init__(self, coord: Tuple[int, int], r: int , s: pymunk.Space) -> None:
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, r)
        self.body.position = coord
        self.body.velocity_func = self.limit_velocity

        self.radius = r
        self.lifetime = 255
        self.shape.density = 1
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
        pygame.draw.circle(display, (240,60,80), convert(self.body.position, h), self.radius)


class Segment:
    def __init__(self, startCoord: Tuple[int, int], endCoord: Tuple[int,int], thickness: int, s: pymunk.Space) -> None:
        self.startCoord = startCoord
        self.endCoord=endCoord
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, startCoord, endCoord, thickness)
        self.shape.elasticity = 1
        s.add(self.body,self.shape)

    def render(self, display :pygame.Surface):
        h = display.get_height()
        pygame.draw.line(display, (255,0,0),convert(self.startCoord,h),convert(self.endCoord,h),5)

  

def convert(coord : Tuple[int,int],height : int) -> Tuple[int,int]:
    return (int(coord[0]),int(h-coord[1]))

def clean_up(balls: List[Ball])->List[Ball]:
    new_balls = []
    for b in balls:
        if b.body.position.y >= 0:
            new_balls.append(b)
            continue
        space.remove(b.body,b.shape)
        

    return new_balls

def clean_dead(balls: List[Ball]):
    new_balls = []
    for b in balls:
        b.lifetime -= 1
        if b.lifetime >= 0:
            new_balls.append(b)
            continue
        space.remove(b.body,b.shape)
    return new_balls

def draw_joint(display: pygame.Surface,joint: pymunk.PinJoint)->None:
    a,b = joint.anchor_a, joint.anchor_b
    world_a = joint.a.local_to_world(a)
    world_b = joint.b.local_to_world(b)
    pygame.draw.line(
        display,
        (255,255,0),
        convert(world_a, h),
        convert(world_b, h),
        5
    )

                     



balls = []

line = Segment((0,100),(500,125),5,space)

ball1 = Ball((250,250),20,space)
ball2 = Ball((350,250),20,space)
c1 = pymunk.PinJoint(ball1.body,ball2.body, (20,0),(-20,0))
c2 = pymunk.PivotJoint(ball1.body,space.static_body,(0,0),(250,250))

space.add(c1)
space.add(c2)

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        
   

    
    display.fill((255,255,255))

    
    ball1.render(display)
    ball2.render(display)
    draw_joint(display,c1)


    


    line.render(display)

    

    
    
    

    
    

    pygame.display.update()
    space.step(1/60)
    clock.tick(60)

        


