import pygame 
from support import import_folder
from settings import *
from tiles import AnimatedTile, StaticTile
import random 

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

	def draw(self , surface , shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)