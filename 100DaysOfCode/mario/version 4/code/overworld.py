import pygame 
from game_data import levels 
from support import import_folder
from misc import Sky , Cloud
from settings import WIDTH 

class Node(pygame.sprite.Sprite):
    def __init__(self , pos , status, speed , path):
        super().__init__()

        self.frames = import_folder(path)
        self.frame_index = 0 
        self.image = self.frames[self.frame_index]

        if status == 'available':
            self.status = 'available'
        else :
            self.status = 'locked'
        
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(speed/2),self.rect.centery-(speed/2),speed,speed)
    

    def animate(self):
        self.frame_index += 0.15
		
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self):
        if self.status == 'available' :
            self.animate()
        else :
            surf = self.image.copy()
            surf.fill('black' , None , pygame.BLEND_RGB_MULT)
            self.image.blit(surf , (0 ,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self , pos):
        super().__init__()

        # icon setup
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos 

class Overworld :
    def __init__(self , start_level ,max_level , surface , create_level):
        # overworld setup 
        self.display_surface = surface 
        self.max_level = max_level 
        self.current_level = start_level
        self.create_level = create_level 
    
        # movement logic 
        self.moving = False 
        self.move_directin = pygame.math.Vector2(0 , 0)
        self.speed = 8

        # sprites setup 
        self.setup_nodes()

        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

        self.sky = Sky(8)
        self.clouds = Cloud(400 ,WIDTH , 30 )

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index , node_data in enumerate(levels.values()):
            if index <= self.max_level :
                sprite = Node(node_data['node_pos'] , 'available' , self.speed , node_data['node_graphics'])
            else :
                sprite = Node(node_data['node_pos'] , 'locked' , self.speed , node_data['node_graphics'])

            self.nodes.add(sprite)
    
    def draw_paths(self):
        points = [node['node_pos'] for _ , node in enumerate(levels.values()) if _ <= self.max_level]
        pygame.draw.lines(self.display_surface , 'red' , False , points , 6)
    
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving :
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level :
                self.move_direction = self.get_movement_data(1)
                self.current_level += 1
                self.moving = True 
            elif keys[pygame.K_LEFT] and self.current_level > 0 :
                self.move_direction = self.get_movement_data(-1)
                self.current_level -= 1
                self.moving = True
            
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
            
    def get_movement_data(self , factor):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[(self.current_level + factor)].rect.center)

        '''
        if (x , y ) is a vector then its normalized value is 
        (x/d , y/d) where d = sqrt(x^2 + y^2)
        '''

        return (end - start).normalize()
    
    def update_icon_pos(self):
        if self.moving  and self.move_direction :
            self.icon.sprite.pos += self.move_direction * self.speed 
            target = self.nodes.sprites()[self.current_level]
            if target.detection_zone.collidepoint(self.icon.sprite.pos) :
                self.moving = False 
                self.move_direction = pygame.math.Vector2(0 ,0)
        
    def run(self):
        # background stuff `
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface)

        # overworld implementation 
        self.input()
        self.nodes.update()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.icon.update()

