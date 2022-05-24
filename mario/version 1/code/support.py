from os import walk 
import pygame 

def import_folder(path):
    """
    this function is useful in capturing the information regarding the files in a particular directory
    return : assets_list 
    """

    assets_list = []

    for _ , __ ,  inf in walk(path):
        for image in inf :
            full_path = f'{path}/{image}'
            image_surf = pygame.image.load(full_path).convert_alpha()
            assets_list.append(image_surf)
    
    return assets_list 