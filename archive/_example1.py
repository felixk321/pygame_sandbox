import pygame
from typing import Tuple
from math import atan2 , cos, sin, tan, sqrt , degrees , radians

pygame.init()

color = pygame.color.Color("white")
circleColor = pygame.color.Color("lightgreen")

coords = [250,250]

display = pygame.display.set_mode((500,500))

clock = pygame.time.Clock()

Coord = Tuple[int,int]

class Triangle:
    def __init__(self, a: Coord, b: Coord, c: Coord) -> None:
        self.coords = set((a,b,c))

        xs,ys = (

            [x for x, _ in self.coords],
            [y for _ , y in self.coords] 
        )

        self.x0, self.y0 = sum(xs)/3 , sum(ys)/3
    
    def rotate(self, alpha:float)-> None:
        x0, y0 = 0,0
        new_coords = []
        for xV, yV in self.coords:
            a = xV - x0
            b = yV - y0
            
            r = sqrt((a)**2 + (b)**2)
            phi = degrees(atan2(b*-1,a)) 
            delta_y = r * sin (radians(phi-alpha))
            delta_x = r * cos(radians(phi-alpha))
            newX,newY = x0+delta_x,y0 - delta_y
            new_coords.append((newX,newY))

            self.coords = (*new_coords,)



    
    def render(self,display: pygame.Surface)->None:
        pygame.draw.polygon(display,(255,0,0) , (*self.coords,) , 2)



t = Triangle((300,100),(250,400),(100,300))

def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
         
        display.fill(color)    
       
        t.render(display)
        
        
        if pygame.mouse.get_pressed()[0]:
            t.rotate(0.5)



            
        
        
        pygame.display.update()

        clock.tick(60)
mainloop()

pygame.quit()




 #     if event.type == pygame.QUIT:
        #         return
            
        #     if pygame.mouse.get_pressed()[0]:

        #         x, y = event.dict["pos"]
                 

        #         squareX = (x-coords[0])**2
        #         squareY = (y - coords[1])**2

        #         if (squareX +squareY) ** 0.5 <= 100:
        #             coords[0] = x
        #             coords[1] = y
                


        # button = pygame.BUTTON_LEFT
        
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_d]:
        #     coords[0] += 1
        # if keys[pygame.K_a]:
        #     coords[0] -= 1
        # if keys[pygame.K_w]:
        #     coords[1] -= 1
        # if keys[pygame.K_s]:
        #     coords[1] += 1

        #pygame.draw.circle(display,circleColor,coords , 100)