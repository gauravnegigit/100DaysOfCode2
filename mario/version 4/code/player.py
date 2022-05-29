
import math
import pygame 
from support import import_folder 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos , surface ,create_jump_particles) -> None:
        super().__init__()

        # player setup 
        self.import_assets()
        self.display_surface = surface 
        self.frame_index = 0 
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # jump particles
        self.dust_particles = import_folder('../graphics/character/dust_particles/run')
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particles = create_jump_particles 
        
        # player attributes for movement 
        self.direction = pygame.math.Vector2(0 , 0)
        self.speed = 4
        self.gravity = 0.8 
        self.jump_speed = -16
        self.status = 'idle'

        # player direction status 
        self.right = True 
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False 

        # health stats 
        self.invisible = False 
        self.hurt_time =  0 
        self.invisibility_duration = 600 
        
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] :
            self.direction.x = 1
            self.right = True 

        elif keys[pygame.K_LEFT] :
            self.direction.x = -1
            self.right = False 

        else :
            self.direction.x = 0 

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
    
    def get_status(self):
        if self.direction.y < 0 :
            self.status = 'jump'
        elif self.direction.y > 1 :
            self.status = 'fall'
        else :
            if self.direction.x != 0 :
                self.status = 'run'
            else :
                self.status = 'idle'

    def lose_health(self , update_health):
        if not self.invisible :
            update_health(-10)
            self.invisible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def timer(self):
        if self.invisible :
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invisibility_duration : 
                self.invisible = False 

    def wave_value(self):
        """
        altering the transerency of the player on the basis of sin A
        cos A can also be used for the same task 
        """

        value = math.sin(pygame.time.get_ticks())
        if value >= 0 : return 255 
        else : return 0 
    
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground :
            self.dust_frame_index += self.dust_animation_speed
            dust_particle = self.dust_particles[int(self.dust_frame_index)% len(self.dust_particles)]

            if self.right :
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)

            else :
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)          


    def import_assets(self):
        path = '../graphics/character/'
        self.animations = {'idle' : [] , 'run' : [] , 'jump' : [] , 'fall' : []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)
    

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        image = animation[int(self.frame_index) % len(animation)]

        if self.right :
            self.image = image
        else :
            self.image = pygame.transform.flip(image , True , False)

        # checking health stats 
        if self.invisible :
            alpha = self.wave_value()
            self.image.set_alpha(alpha)  # alpha referes to the transperency of the image 
        else :
            self.image.set_alpha(255) 
        
        # setting teh rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        
        elif self.on_ground and self.on_left :
             self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

        elif self.on_ground :
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.on_ceiling and self.on_right :
            self.rect = self.image.get_rect(topright = self.rect.topright)    

        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)

        elif self.on_ceiling :
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        

    def apply_gravity(self):
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y 
    
    def jump(self):
        self.direction.y = self.jump_speed 
    
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.timer()