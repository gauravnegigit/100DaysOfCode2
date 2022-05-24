import pygame 
from support import import_csv_layout , import_graphics 
from tiles import Tile , StaticTile , Crate , Coin , Palm 
from player import Player 
from enemy import Enemy 
from misc import Particle , Sky , Water , Cloud 
from settings import *

class Level :
    def __init__(self , level_data , surface) -> None:
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # player and enemy setup 
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        # constraints sprites for enemy movement 
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout , 'constraint')

        # dust 
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False 

        ''' main backgroud stuff '''

        # terrain setup 
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        # grass setup 
        grass_layout = import_csv_layout(level_data['terrain'])
        self.grass_sprites = self.create_tile_group(grass_layout , 'grass')

        # crates 
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        # coins 
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        # foreground palms 
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

        # background palms 
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

        # collidable sprites for collision
        self.collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
    
        # decoration stuff 
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size 
        self.water = Water(HEIGHT - 20 , level_width)
        self.clouds = Cloud(400 , level_width , 30)

    def create_tile_group(self , layout , type):
        sprites = pygame.sprite.Group()

        for i , row in enumerate(layout):
            for j , val in enumerate(row):
                if val != '-1' :
                    x , y = j * tile_size , i * tile_size

                    if type == 'terrain':
                        terrain_list = import_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surf = terrain_list[int(val)]
                        sprite = StaticTile(tile_size , x , y , tile_surf)
                    
                    if type == 'grass' :
                        grass_list = import_graphics('../graphics/decoration/grass/grass.png')
                        tile_surf = grass_list[int(val) % len(grass_list)]
                        sprite = StaticTile(tile_size , x , y , tile_surf)
                    
                    if type == 'crates' :
                        sprite = Crate(tile_size , x , y)
                    

                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '0': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)
                        if val == '1': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_bg',64)  

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'constraint':
                        sprite = Tile(tile_size,x,y)

                    sprites.add(sprite)
    
        return sprites 
    
    def player_setup(self , layout):
        for i , row in enumerate(layout):
            for j , val in enumerate(row):
                x , y = j * tile_size , i * tile_size

                if val == '0':
                    sprite = Player((x,y) , self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)
        
    def enemy_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy , self.constraint_sprites , False) :
                enemy.reverse()
    
    def create_jump_particles(self , pos):

        if self.player.sprite.facing_right :
            pos -= pygame.math.vector2(10 , 5)
        else :
            pos += pygame.math.Vector2(10 , -5)
        
        jump_particle_sprite = Particle(pos , 'jump' )
        self.dust_sprite.add(jump_particle_sprite)

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = Particle(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)


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
        '''player.rect.x += player.direction.x * player.speed'''
        for sprite in self.collidable_sprites :
            
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
        player.rect.x += player.direction.x * player.speed

        for sprite in self.collidable_sprites :
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
        
        if player.on_ceiling and player.direction.y > 0.1 :
            player.on_ceiling = False
    
    def get_on_ground(self):
        if self.player.sprite.on_ground :
            self.player_on_ground = True 
        else :
            self.player_on_ground = False 
    
    def run(self):

        """
        This function would update the game .
        Note : the background stuff , player , enemy must be in order as mentioned below otherwise the game would be seen to be clumsy 

        return : None 
        """
		
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface , self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface) 

        # terrain 
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
		
        # enemy 
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate 
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins 
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # dust particles 
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_collision()
		
        self.get_on_ground()
        self.vertical_collision()
        '''self.create_landing_dust()'''
		
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)    

        # to make the water visible in all time it is updated over top of other surfaces
        self.water.draw(self.display_surface  , self.world_shift)