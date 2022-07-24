from doctest import DocTestCase
import pygame 
import neat 
import time 
import os 
import random
pygame.font.init()

# SCREEN COSTANTS 
WIDTH , HEIGHT = 500 , 800
FPS = 30
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
DRAW_LINES = False 

# image asstes
BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("assets" , f"bird{i}.png")) , (60 , 40)) for i in range(1 , 4) ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets" , "pipe.png")))
BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets" , "base.png")) , (WIDTH , 200))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("assets" , "bg.png")))



class Bird :
    IMGS = BIRD_IMGS 
    MAX_ROTATION = 25 
    ROT_VEL = 20 
    ANIMATION_TIME = 5

    def __init__(self , x , y):
        self.x = x
        self.y = y 
        self.tilt = 0 
        self.vel = 0 
        self.tick_count = 0
        self.height = self.y 
        self.img_count = 0 

        self.frame_index = 0 
        self.img = self.IMGS[self.frame_index]

        self.mask = pygame.mask.from_surface(self.img)
    
    def jump(self):
        self.vel = -10.5 
        self.tick_count = 0  
        self.height = self.y 

    def move(self):
        self.tick_count += 1

        # for downward acceleration 
        d = self.vel * self.tick_count + 2 * self.tick_count ** 2

        # terminal velocity
        if d >= 16 :
            d = 16 
        if d < 0 :
            d -= 2

        self.y += d
    
        if d< 0 or self.y + self.height < 50 :
            if self.tilt < self.MAX_ROTATION :
                self.tilt = self.MAX_ROTATION
        
        else :
            if self.tilt > -90 :
                self.tilt -= self.ROT_VEL
    
    def draw(self , win , dt):
        self.frame_index += 10 * dt 

        if self.tilt < -80 :
            self.frame_index = 0

        if self.frame_index >= len(self.IMGS):
            self.frame_index = 0
        self.img = self.IMGS[int(self.frame_index)]

        rotated_image = pygame.transform.rotate(self.img , self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x , self.y)).center)
        win.blit(rotated_image , new_rect.topleft)

class Pipe :
    GAP = 200 
    VEL = 5

    def __init__(self , x) -> None:
        self.x = x 
        self.height = 0 
        self.top = 0 
        self.bottom = 0 
        self.UP = pygame.transform.flip(PIPE_IMG , False , True)
        self.DOWN  = PIPE_IMG 
        self.passed = False 

        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50 , 430)

        # calculating and y - coordinate for the both up and down pipe 
        self.top = self.height - self.UP.get_height()   # gives the 
        self.bottom = self.height + self.GAP 
    
    def move(self):
        self.x -= self.VEL 

    def collide(self , bird ):
        
        """
        this method implements the perefct pixel collison for the two masks 
        """
        bird_mask = bird.mask 
        top_mask = pygame.mask.from_surface(self.UP)
        bottom_mask = pygame.mask.from_surface(self.DOWN)

        top_offset = (self.x - bird.x , self.top - round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom - round(bird.y))

        if bird_mask.overlap(bottom_mask , bottom_offset) or bird_mask.overlap(top_mask , top_offset) :
            return True 

        return False 


    def draw(self , win):
        win.blit(self.UP , (self.x , self.top))
        win.blit(self.DOWN , (self.x , self.bottom))

class Ground :
    def __init__(self , scale_factor) -> None:
        # image 
        self.image = pygame.transform.scale(BASE_IMG , (BASE_IMG.get_width() * scale_factor , BASE_IMG.get_height())) # here the scale factor is 1 , it can be changed according to teh convinience

        # position
        self.rect = self.image.get_rect(bottomleft = (0 , HEIGHT + 100))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # creating masks for collision handling 
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self , dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

    def draw(self  , win , dt):
        self.update(dt)
        win.blit(self.image , self.pos)

def draw(birds , pipes , base, dt , pipe_ind) :
    WIN.blit(BG_IMG , (0, 0))

    for pipe in pipes :
        pipe.draw(WIN)
    
    base.draw(WIN , dt)

    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        bird.draw(WIN , dt)

    pygame.display.update()

def main(genomes , config):


    base = Ground(2)
    pipes = [Pipe(700)]
    score = 0 
    run = True 
    clock = pygame.time.Clock()

    dt = 1/FPS

    # AI implementation 
    nets = []
    birds = []
    ge = []
    for _, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    while run :
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
                quit()
            
        pipe_ind = 0 
        if len(birds) > 0 :
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].UP.get_width():  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input
        else :
            break 

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5 :
                bird.jump()

        # few attrabiutes regrading motion of pipes
        rem  =[]
        add_pipe = False

        for pipe in pipes:
            pipe.move()
            # check for collision
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.UP.get_width() < 0:
                pipes.remove(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        for pipe in pipes :
            if pipe.collide(bird):
                pass 
            if pipe.x + pipe.UP.get_width() < 0 :
                pipes.remove(pipe)
            
            if not pipe.passed and pipe.x < bird.x :
                pipe.passed = True 
                add_pipe = True 

        if add_pipe :
            score += 1
            for genome in ge :
                genome.fitness += 5
            pipes.append(Pipe(WIDTH))
        


        for bird in birds:
            if bird.y + bird.img.get_height() > HEIGHT or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw(birds , pipes , base , dt , pipe_ind)

def run_neat(config_file):
    """
    run the NEAT ALGORITHM TO TRAIN A NEURAL NETWORK TO PLAY THE AGME 
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    # Run for up to 50 generations.
    winner = p.run(main, 5)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run_neat(config_path)
