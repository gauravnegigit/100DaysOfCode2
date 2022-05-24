import pygame 
from tiles import Tile 
from settings import tile_size  , WIDTH 
from player import Player 

class Level :
    def __init__(self , level_data , surface) -> None:

        # level setup 
        self.display_surface = surface 
        self.level_data = level_data 
        self.setup_level(level_data)

        self.world_shift = 0 
        self.current_x = 0 
    
    def setup_level(self , layout) :
        """
        method created to setup te level for the game 
        """

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for i , row in enumerate(layout):
            for j , cell in enumerate(row):

                if cell == 'X' :
                    tile = Tile((j * tile_size , i * tile_size) , tile_size)
                    self.tiles.add(tile)
                
                if cell == 'P' :
                    player = Player((j * tile_size , i * tile_size) )
                    self.player.add(player)
    
    def scroll_x(self):
        player = self.player.sprite 
        player_x = player.rect.centerx 
        direction_x = player.direction.x 

        if player_x < 200 and direction_x < 0:
            self.world_shift = 8 
            player.speed = 0 
        elif player_x  > WIDTH - 200 and direction_x > 0:
            self.world_shift = -8 
            player.speed = 0 
        else :
            self.world_shift = 0 
            player.speed = 8
    
    def horizontal_collision(self):
        """
        This function will handle the horizontal collisions of the player
        return : None 
        """

        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed 

        for sprite in self.tiles.sprites() :
            rect = pygame.Surface((32 , 64)).get_rect(center = player.rect.center)
            if sprite.rect.colliderect(player.rect) :
                if player.direction.x < 0 :
                    player.rect.left = sprite.rect.right
        
                    player.on_left = True 
                    self.current_x = player.rect.left

                elif player.direction.x > 0 :
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right 

            
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0) :
            player.on_left = False 
        
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False 

        
        
    def vertical_collision(self):

        """
        This function will handle the horizontal collisions of the player
        return : None 
        """

        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites() :
            if sprite.rect.colliderect(player.rect) :
                if player.direction.y > 0 :
                    player.rect.bottom = sprite.rect.top

                    # to counter the gravity when the player is standing 
                    player.direction.y = 0 
                    player.on_ground = True 

                elif player.direction.y < 0 :
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 
                    player.on_ceiling = True 
        
        # condition while the player is jumping 
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1 :
            player.on_ground = False
        
        if player.on_ceiling and player.direction.y > 0 :
            player.on_ceiling = False
    
    def run(self) :

        # updating teh tiles 
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface )
        self.scroll_x()

        # updating the player 

        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()
