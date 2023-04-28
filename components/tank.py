from pymunk import Vec2d,Body, Poly, Space, PivotJoint, ShapeFilter
from pygame import Surface, draw, image, transform
from utils import convert
from components.ball import Ball
from typing import List
from math import degrees




class TankBase:
    def __init__(self, origin:Vec2d, space: Space)-> None:
        self.body = Body()
        self.center = Vec2d(104, -22)
        self.body.position = origin + self.center
       

        points = (
            Vec2d(0,0),
            Vec2d(48,0),
            Vec2d(73,6),
            Vec2d(204,10),
            Vec2d(200,28),
            Vec2d(172,34),
            Vec2d(38,33),
            Vec2d(10,20),
            Vec2d(0,20)
        )


        self.shape = Poly(self.body,
                          [
            convert(Vec2d(*p) - self.center, 44)
            for p in points

            ])
        
        self.shape.density = 1
        space.add(self.body, self.shape)

        self.image = image.load("./assets/tank_base.png", "png")

    def render(self, display: Surface)->None:
        h = display.get_height()

        
        points = [

        convert(self.body.local_to_world(v), h)
        
        for v in self.shape.get_vertices()
        ]

        rotate_image = transform.rotate(self.image, degrees(self.body.angle))

        dest = rotate_image.get_rect(center = convert(self.body.position,h))

        display.blit(rotate_image,dest)

        draw.polygon(display,(30,65,50), points, 1)

class Wheel(Ball):
    pass


class Tank: 
    def __init__(self, origin : Vec2d, space: Space) -> None:
        self.origin = origin
        self.cf = ShapeFilter(group = 1) #collision filter

        self.tb = TankBase(origin + Vec2d(0,-30), space)
        self.tb.shape.filter = self.cf

        self.wheels = self.create_wheels(space)

    def create_wheels(self, space: Space) ->List[Wheel]:
        r = 9
        wheel = Wheel(self.origin + Vec2d(38,-56)+Vec2d(r,-r), r, space)
        tb_local = self.tb.body.world_to_local(wheel.body.position)  #TRY TO GET IMAGE TO MATCH BODY
        wheel.shape.filter = self.cf
        space.add(PivotJoint
            (
            wheel.body,
            self.tb.body,
            (0,0),
            tb_local

            )
                  
                  )
        return [wheel, ]
        



    def render(self, display: Surface)->None:
        

        for wheel in self.wheels:
            wheel.render(display)

        self.tb.render(display)


        