import pygame 
from support import import_folder
from settings import *
from tiles import AnimatedTile, StaticTile
import random 

class Particle(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump':
			self.frames = import_folder('../graphics/character/dust_particles/jump')
		if type == 'land':
			self.frames = import_folder('../graphics/character/dust_particles/land')
		
		if type == 'explosion' :
			self.frames = import_folder('../graphics/enemy/explosion')			
		
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

class Sky :
	def __init__(self , horizon) -> None:
		self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
		self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
		self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
		self.horizon = horizon
	
	def draw(self , surface):
		for i in range(WIDTH//self.top.get_width() + 1):
			for row in range(vertical_tile_number):
				y = row * tile_size 

				if row < self.horizon :
					x = i * self.top.get_width()
					surface.blit(self.top , (x , y))
				elif row == self.horizon :
					surface.blit(self.middle , (x , y))
				
				else :
					surface.blit(self.bottom , ( x ,y))
		
class Water :
	def __init__(self , top , level_width):
		water_start = - WIDTH 
		water_tile_width = 192
		tile_x = int((level_width + WIDTH * 2)/water_tile_width)
		self.water_sprites = pygame.sprite.Group()

		for tile in range(tile_x):
			x , y = tile * water_tile_width + water_start , top 

			sprite = AnimatedTile(192 , x , y ,'../graphics/decoration/water' )
			self.water_sprites.add(sprite)
		
	def draw(self , surface , shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Cloud :
	def __init__(self , horizon , level_width , cloud_number) -> None:
		cloud_surf_list = import_folder('../graphics/decoration/clouds')
		min_x = -WIDTH
		max_x = level_width + WIDTH 
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			cloud = random.choice(cloud_surf_list)
			x = random.randint(min_x,max_x)
			y = random.randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)	

	def draw(self , surface , shift = 0):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)