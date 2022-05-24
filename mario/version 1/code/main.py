import pygame , sys 
from settings import * 
from level import Level 
from game_data import level_0 

# constants 
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 
level = Level(level_0 , WIN)

def main():
    run = True 
    clock = pygame.time.Clock()

    while run :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()
        
        WIN.fill('grey')
        level.run()
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__" :
    main()