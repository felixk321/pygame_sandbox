from pymunk import Vec2d,Body, Poly, Space, PivotJoint, ShapeFilter, SimpleMotor, GearJoint, PinJoint, RotaryLimitJoint
from pygame import Surface, draw, image, transform, Vector2, mixer
from utils import convert
from components.ball import Ball
from typing import List, Tuple
from math import degrees, sin, cos


class PolyComponent:
    def __init__(self, origin: Vec2d, center: Vec2d, space:Space, img_path: str, points: Tuple[Tuple[int,int]], filter: ShapeFilter)-> None:
        self.origin = origin
        self.body = Body()
        self.center = center
        self.body.position = origin + self.center



        self.shape = Poly(self.body,
                          [
            convert(Vec2d(*p) - self.center, abs(self.center.y *2))
            for p in points

            ])
        self.shape.filter = filter
        self.shape.density = 1
        space.add(self.body, self.shape)

        self.image = image.load(img_path)
        
    def render(self, display: Surface, shift_x: float)->None:
        

        h = display.get_height()


        points = [

        convert(self.body.local_to_world(v), h)

        for v in self.shape.get_vertices()
        ]

        rotate_image = transform.rotate(self.image, degrees(self.body.angle))
        pos = convert(self.body.position,h) - Vector2(shift_x, 0)


        dest = rotate_image.get_rect(center = pos)

        display.blit(rotate_image,dest)

class Wheel(Ball):
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)
        self.image = image.load("./assets/wheel.png", "png")

    def render(self, display: Surface, shift_x: float)->None:
        h = display.get_height()
        rotated_img = transform.rotate(self.image , degrees(self.body.angle))
        pos = Vector2(convert(self.body.position, h)) - Vector2(shift_x,0)
        dest = rotated_img.get_rect(center = pos)

        display.blit(rotated_img, dest)
        

class Rear_Wheel(Wheel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)

        tb: PolyComponent = kwargs["tb"]
        space: Space = self.body.space

        self.image = image.load("./assets/rear_wheel.png", "png")
        self.motor = SimpleMotor(self.body,tb.body, 1)
        space.add(self.motor)
class Ammo(Ball):
    pass

class Tank: 
    def __init__(self, origin : Vec2d, space: Space) -> None:
        self.fire_sound = mixer.Sound("assets/explosion_sound.flac")
        self.origin = origin
        self.cf = ShapeFilter(group = 1) #collision filter
        self.ammo_generated = False
        self.space = space
        


        self.tb = PolyComponent(
            origin = origin + Vec2d(0,-30),
              center = Vec2d(104,-22),
              space = space,
              img_path = "./assets/tank_base.png",
              points = (
            Vec2d(0,0),
            Vec2d(48,0),
            Vec2d(73,6),
            Vec2d(204,10),
            Vec2d(200,28),
            Vec2d(172,34),
            Vec2d(38,33),
            Vec2d(10,20),
            Vec2d(0,20)), filter = self.cf )
        
        self.turret = PolyComponent(
            origin = origin + Vec2d(35,0),
            center = Vec2d(66, -18),
            space = space,
            img_path ="./assets/turret.png",
            points =  [(0,16), (47,15), (71,0), (91,0), (66,14), (124,20),(132,27),(117,36), (43,36), (38,30), (16,26), (2,25),  ],
            filter = self.cf

        )
        
        turret_rect = self.turret.shape.bb

        left_attachment = turret_rect.left, turret_rect.bottom
        right_attachment = turret_rect.right, turret_rect.bottom

        space.add(PivotJoint(
            self.tb.body,
            self.turret.body,
            self.tb.body.world_to_local(left_attachment),
            self.turret.body.world_to_local(left_attachment)
                  ))
        
        space.add(PivotJoint
                  (self.tb.body,
                    self.turret.body,
                    self.tb.body.world_to_local(right_attachment),
                    self.turret.body.world_to_local(right_attachment)
                             ))
        self.gun = PolyComponent(
            
            origin = origin + Vec2d(156,-30),
            center = Vec2d(47,4),
            space = space,
            img_path = "./assets/gun.png",
            points = ((0,0),(13,2),(25,2),(33,3),(35,0),(45,0),(49,3),(90,4),(90,2),(94,4),(94,8),(0,8)),
            filter = self.cf
                                 )
        
        attachment_point = self.gun.origin + Vec2d(-10,-5)


        space.add(PivotJoint(self.turret.body, self.gun.body, self.turret.body.world_to_local(attachment_point), self.gun.body.world_to_local(attachment_point)))
    
        self.gun_angle = RotaryLimitJoint(self.turret.body,self.gun.body,0,0.1)
        space.add(self.gun_angle)


        self.wheels = self.create_wheels(space)

        self.rw = self.create_rear_wheels(space)

        for wheel in self.wheels:
            space.add(GearJoint(self.rw.body,wheel.body,0, 1))

        self.ammo_coord = self.gun.center + Vec2d(43,0)

        self.ammo, self.ammo_joint = self.generate_ammo(space)
        
        

    def generate_ammo(self, space : Space)-> Tuple[Ammo, PivotJoint]:
        bb = self.gun.shape.bb #imaginary box surrounding shape, for ease of getting coords
        x = bb.right-5
        y = bb.top - 15
        ammo = Ammo((x,y),5, space)
        ammo.shape.filter = self.cf

        joint = (PivotJoint
                  
                  (self.gun.body,ammo.body, self.gun.body.world_to_local(ammo.body.position), ammo.body.world_to_local(ammo.body.position))
                  )
        
        space.add(joint)

        
        return ammo, joint

    def create_wheels(self, space: Space) ->List[Wheel]:
        r = 9

    

        wheel_coords = [
            Vec2d(38,-54),
            Vec2d(57,-54),
            Vec2d(76,-54),
            Vec2d(96,-54),
            Vec2d(116,-54),
            Vec2d(136,-54),
            Vec2d(160,-54),
            Vec2d(184, -42)
        ]

        result = []

        for coord in wheel_coords:


            wheel = Wheel(self.origin + coord +Vec2d(r,-r), r, space)
            wheel.shape.filter = self.cf
            wheel.shape.friction = 1
            tb_local = self.tb.body.world_to_local(wheel.body.position)  
            wheel.shape.filter = self.cf
            space.add(PivotJoint
                (
                wheel.body,
                self.tb.body,
                (0,0),
                tb_local

                )
                  
                  )
            result.append(wheel)
        return result
    
    def create_rear_wheels(self, space: Space)-> Rear_Wheel:
        r = 9

        coord = self.origin + Vec2d(14, -42) + Vec2d(r,-r)
        
        wheel = Rear_Wheel(coord, r, space, tb = self.tb)
        wheel.shape.filter = self.cf

        space.add(PivotJoint(wheel.body, self.tb.body, (0,0), self.tb.body.world_to_local(wheel.body.position) ))

        return wheel

    def move(self, direction: int)->None:
        self.rw.motor.rate += -1 * direction

    def update_gun_angle(self, diff: float)->None:
        if self.gun_angle.min < 0 and diff < 0:
            return
        if self.gun_angle.max > 1.12 and diff > 0:
            return

        self.gun_angle.min += diff
        self.gun_angle.max += diff

    def fire(self)->Ammo:
        self.fire_sound.play()
        self.ammo.body.angle = 0

        self.space.remove(self.ammo_joint)


        max_force = 10**5

        r = self.ammo.shape.radius

        angle = self.gun.body.angle
        impulse = Vec2d(max_force * cos(angle), max_force * sin(angle))

        point = -1 * Vec2d(cos(angle)*r, sin(angle)*r)

        self.ammo.body.apply_impulse_at_local_point(impulse, (-5,0))
        
        old_ammo = self.ammo
        self.ammo, self.ammo_joint = self.generate_ammo(self.space)
        return old_ammo

    


    def render(self, display: Surface, shift_x: float)->None:
        

        for wheel in self.wheels:
            wheel.render(display, shift_x)

        self.tb.render(display, shift_x)
        self.rw.render(display, shift_x)
        self.gun.render(display, shift_x)
        self.turret.render(display, shift_x)
        #self.ammo.render2(display, shift_x)
        
    
        
        


        