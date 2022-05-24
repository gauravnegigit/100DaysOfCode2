from turtle import width
import pygame 
from settings import WIDTH , HEIGHT , level_map
from level import Level 

# constants 
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 
level = Level(level_map , WIN)

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
        level.run()
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__" :
    main()