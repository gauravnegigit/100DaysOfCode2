import pygame

class UI :
    def __init__(self , surface):
        # setup 
        self.display_surface = surface 

        self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54 , 39)
        self.bar_height = 4 
        self.bar_width = 152 

        # coins 
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50 , 61))
        self.font = pygame.font.SysFont('Arial Black', 30)
    
    def display_health(self , current , full):
        self.display_surface.blit(self.health_bar , (20 , 10))
        health_bar_rect = pygame.Rect(self.health_bar_topleft , ((self.bar_width * current/full) , self.bar_height))
        pygame.draw.rect(self.display_surface , 'red' , health_bar_rect)
    
    def display_coins(self , amount):
        self.display_surface.blit(self.coin , self.coin_rect)
        text = self.font.render(str(amount) , False , 'white')
        self.display_surface.blit(text , text.get_rect(midleft = (self.coin_rect.right + 4 , self.coin_rect.centery)))
