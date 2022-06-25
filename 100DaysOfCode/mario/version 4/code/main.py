import pygame  , sys 
from settings import * 
from overworld import Overworld 
from level import Level 
from ui import UI 

class Game :
    def __init__(self):
        # game setup 
        self.max_level = 2
        self.max_health = 100 
        self.cur_health = 100 
        self.coins = 0 

        # overworld setup 
        self.overworld = Overworld(0 , self.max_level , WIN , self.create_level)       # in python , functions are first class objects so they can be passed as arguments in a method or funciotn
        self.status = 'overworld'

        self.ui = UI(WIN)
    
    def create_level(self , current_level):
        self.level = Level(current_level , WIN , self.create_overworld , self.update_coins, self.update_health)
        self.status = 'level'
    
    def create_overworld(self , current_level , new_max_level ):
        if new_max_level > self.max_level :
            self.max_level = new_max_level
        
        self.overworld = Overworld(current_level , self.max_level , WIN , self.create_level)
        self.status = 'overworld'
    
    def update_coins(self , amount):
        self.coins += amount 
    
    def update_health(self , amount):
        self.cur_health += amount 
    
    def reset(self):
        self.max_level = 2
        self.max_health = 100 
        self.cur_health = 100 
        self.coins = 0 
        self.overworld = Overworld(0 , self.max_level , WIN , self.create_level)       # in python , functions are first class objects so they can be passed as arguments in a method or funciotn
        self.status = 'overworld'
    
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else :
            self.level.run()
            self.ui.display_health(self.cur_health , self.max_health)
            self.ui.display_coins(self.coins)
            
            if self.cur_health <= 0 :
                self.reset()
            

# initializing pygame 
pygame.init()

# constants 
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60
game = Game()

def main():
    run = True 
    clock = pygame.time.Clock()

    while run :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()
        
        WIN.fill('black')
        game.run()
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()