import pygame 
from constants import * 
import random

# OOP implementation 
class BG(pygame.sprite.Sprite):
    def __init__(self , groups , scale_factor):
        super().__init__(groups)

        full_image  = pygame.transform.scale(BACKGROUND , (BACKGROUND.get_width() * scale_factor , BACKGROUND.get_height() * scale_factor))

        self.image = pygame.Surface((full_image.get_width() * 2 , full_image.get_height() ))
        self.image.blit(full_image , (0 , 0 ))
        self.image.blit(full_image  , (full_image.get_width() , 0))

        self.rect = self.image.get_rect(topleft = (0 , 0 ))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    
    def update(self , dt):
        self.pos.x -= -300 * dt 

        if self.rect.centerx <= 0 :
            self.pos.x = 0 
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups , scale_factor) -> None:
        super().__init__(groups)

        self.sprite_type = 'ground'

        # image 
        self.image = pygame.transform.scale(GROUND , pygame.math.Vector2(GROUND.get_size()) * scale_factor)

        # position 
        self.rect  = self.image.get_rect(bottomleft = (0 , HEIGHT)) 
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # creating masks for collision handling 
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self , dt):
        self.pos.x -= 360 * dt 

        if self.rect.centerx <= 0 :
            self.pos.x = 0 
        
        self.rect.x = round(self.pos.x)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # extra attributes 
        self.gravity = 700 
        self.direction = 0 

        self.mask = pygame.mask.from_surface(self.image)
        JUMP.set_volume(0.3)

    def import_frames(self , scale_factor):
        self.frames = []

        for i in range(3):
            surf = pygame.image.load(f'Assets\\red{i}.png').convert_alpha()

            surface = pygame.transofrm.scale(surf , pygame.math.vector2(surf.get_size()) * scale_factor)

            self.frames.append(surface)
        
    
    def apply_gravity(self , dt):
        self.direction += self.gravity * dt 
        self.pos.y += self.direction * dt 
        self.rect.y = round(self.pos.y)
    
    def jump(self):
        JUMP.play()
        self.direction = -400

    def animate(self , dt):
        self.frame_index += 10 * dt 

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self ):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.06,1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self , dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self , groups , scale_factor) -> None:
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        ch = random.choice(('up' , 'down'))
        surf = pygame.image.load(f'Assets/{random.choice((0 , 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf , pygame.math.Vector2(surf.get_size()) * scale_factor)

        x = WIDTH + random.randint(40 , 100)

        if ch == 'up' :
            y = HEIGHT + random.randint(10 , 50)
            self.rect =  self.image.get_rect(midbottom = (x , y))
        else :
            y = random.randint(- 50 , -10)
            self.image = pygame.transform.flip(self.image  , False , True )
            self.rect = self.image.get_rect(midtop = (x , y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # creating masks for collision
        self.mask = pygame.mask.from_surface(self.image)


    def update(self,dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)

        if self.rect.right <= -100:
            self.kill()
