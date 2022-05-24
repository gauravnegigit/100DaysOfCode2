import pygame 
from support import import_folder 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos ) -> None:
        super().__init__()

        # player setup 
        self.import_assets()
        self.frame_index = 0 
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # player attributes for movement 
        self.direction = pygame.math.Vector2(0 , 0)
        self.speed = 8
        self.gravity = 0.981 
        self.jump_speed = -16
        self.status = 'idle'

        # player direction status 
        self.right = True 
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False 
        
    
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
        elif self.direction.y > 0.1 :
            self.status = 'fall'
        else :
            if self.direction.x != 0 :
                self.status = 'run'
            else :
                self.status = 'idle'
    
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
        self.direction .y = self.jump_speed 
    
    def update(self):
        self.get_input()
        self.get_status()
        #self.apply_gravity()
        self.animate()
        self.rect.x += self.direction.x * self.speed 
