from grpc import local_server_credentials
import pygame , time 
from constants import * 
from sprites import BG , Ground , Plane , Obstacle 

class GameInfo :
	LEVELS = 10
	def __init__(self , level = 11):
		self.level = level
		self.started = False
	def start_level(self):
		self.started = True
	def next_level(self) :
		self.level += 1
		self.started = False
	def reset(self):
		self.level = 1
		self.started = False
	def finished(self):
		return self.level > self.LEVELS

class Game :
    def __init__(self) -> None:

        pygame.init()
        pygame.display.set_caption('Flappy bird game')
        self.clock = pygame.time.Clock()
        self.active = False 
        self.game = GameInfo()

        # creating sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        self.scale_factor = HEIGHT / BACKGROUND.get_height()

        # sprite setup 
        BG(self.all_sprites,self.scale_factor)
        Ground([self.all_sprites,self.collision_sprites],int(self.scale_factor))
        #self.plane = Plane(self.all_sprites,self.scale_factor / 1.7)

        # setting timer for the obstacles
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer , 1000)

        # text
        self.font = pygame.font.SysFont('ArialBlack' , 30)
        self.score_per_level = 100 
        self.initial = (self.game.level - 1) * self.score_per_level         # it stores the initial level for eg if player is in level 2 then initial of 100 is already in the score 
        self.score = self.initial 
        
        self.lives = 3        # there are three lives for the player after completing 
        self.start_offset = 0 
        
        # menu 
        self.menu_rect = MENU.get_rect(center = (WIDTH//2 , HEIGHT//2))

        # music 
        MUSIC.play(loops = -1)
    
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane , self.collision_sprites , False , pygame.sprite.collide_mask) or self.plane.rect.top <= 0 :
            
            # killing the obstacles and the plane sprites
            for sprite in self.collision_sprites.sprites() :
                if sprite.sprite_type == 'obstacle' :
                    sprite.kill()
            
            self.active = False 
            self.plane.kill()

            if self.lives :
                self.initial = (self.game.level - 1) * self.score_per_level 
            else :
                self.initial = 0 
                self.score = 0 
                self.game.reset()

            self.lives -= 1
    
    def display_score(self):
        if self.active :
            self.score  = (pygame.time.get_ticks() - self.start_offset) // 1000 + self.initial 
            y = HEIGHT/10

        else :
            y = HEIGHT/2 + self.menu_rect.height

        # DISPLAYING SCORE 
        text = self.font.render("SCORE  :  " , 1, (0,0,0))  # text may be entered according to the programmer's wish

        digits = list(str(self.score))
        width = text.get_width()
        self.print_text(text , digits , width , 150 , y)

        # displaying level
        
        text = self.font.render("LEVEL  :  " , 1 , (0 , 0 , 0))

        digits = list(str(self.game.level))
        width = text.get_width()
        self.print_text(text , digits , width , -150  , y)
    
    def print_text(self ,text , digits  , width , x , y):
        for digit in digits :
            width += NUMBERS[int(digit)].get_width() 

        Xoffset = (WIDTH - width)//2 + x

        WIN.blit(text , (Xoffset , y))
        Xoffset += text.get_width()

        for digit in digits :
            WIN.blit(NUMBERS[int(digit)] , (Xoffset , y))
            Xoffset += NUMBERS[int(digit)].get_width()      
        
    def run(self):
        run = True 
        last_time = time.time()

        while run :
            #self.clock.tick(FPS)

            # delta timer 
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run = False 
                    pygame.quit()
                    quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if self.active :
                        self.plane.jump()
        
                    else :
                        self.plane = Plane(self.all_sprites , self.scale_factor/1.7)
                        self.active = True 
                        self.start_offset = pygame.time.get_ticks()
                
                if event.type == self.obstacle_timer and self.active :
                    Obstacle([self.all_sprites , self.collision_sprites] , self.scale_factor)

            
            WIN.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(WIN)
            self.display_score()

            # tracking the levels
            if self.score == self.game.level * self.score_per_level  :
                self.game.next_level()
                self.lives = 3
                self.game.started = True

            # condition when the game is finished

            if self.game.finished():
                self.score = 0 
                self.initial = 0 
                self.game.reset()
                self.active = False 
                text = self.font.render("YU WON", 1, (0,0,0))
                WIN.blit(text , (WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2 + 20))

                pygame.display.update()
                pygame.time.delay(1500)
                
                self.game.started = True   
                            
            #self.game.level = self.score //100 + 1

            if self.active :
                self.collisions()
                       
            else :

                plane = pygame.image.load('Assets/red0.png')
                rect = plane.get_rect(midleft = (WIDTH//15 , HEIGHT//2))
    
                WIN.blit(plane , rect)
                WIN.blit(MESSAGE1 , (int((WIDTH - MESSAGE1.get_width())/2) , int(HEIGHT*0.13)))
                WIN.blit(MESSAGE2 , (int((WIDTH - MESSAGE2.get_width())/2) , int(HEIGHT*0.26)))
                WIN.blit(MENU , self.menu_rect)

            pygame.display.update()

if __name__ == "__main__" :
    game = Game()
    game.run()
