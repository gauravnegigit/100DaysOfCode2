from csv import reader
from settings import tile_size
from os import walk 
import pygame 

def import_folder(path):
    assets_list = []

    for _ , __ , inf in walk(path):
        for image in inf :
            full_path = f'{path}/{image}'
            image_surf = pygame.image.load(full_path).convert_alpha()
            assets_list.append(image_surf)
        
    return assets_list

def import_csv_layout(path):
    terrain_map = []

    with open(path) as f :
        level = reader(f , delimiter = ',')
        for row in level :
            terrain_map.append(list(row))
        return terrain_map

def import_graphics(path):
    surf = pygame.image.load(path).convert_alpha()
    tile_x , tile_y = int(surf.get_size()[0]/tile_size) , int(surf.get_size()[1]/tile_size)

    tiles= []

    for row in range(tile_y):
        for col in range(tile_x):
            x , y = col * tile_size , row * tile_size 
            new_surf = pygame.Surface((tile_size , tile_size) , flags = pygame.SRCALPHA)
            new_surf.blit(surf , (0 , 0) , pygame.Rect(x , y , tile_size , tile_size))
            tiles.append(new_surf)
        
    return tiles 
