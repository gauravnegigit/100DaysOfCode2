from pong import Game 
import pygame  
import os 
import time 
import pickle 


class PongGame :
    def __init__(self , window , width , height) -> None:
        self.game = Game(window , width , height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle 
        self.right_paddle = self.game.right_paddle 
    
    def test_ai(self , net):
        """
        test the ait against a human player by passign a NEAT neural network
        """

        clock = pygame.time.Clock()
        run = True 
        while run :
            clock.tick(FPS)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    run = False 
                    break 
            
            output = net.activate((self.right_paddle.y , abs(self.right_paddle.x - self.ball.x) , self.ball.y))
            decision = output.index(max(output))

            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.game.move_paddle( True , up = True )
            elif keys[pygame.K_s] :
                self.game.move_paddle( True , up = False)

            self.game.draw(draw_score = True)
            pygame.display.update()
    
    def run(self ):
        clock = pygame.time.Clock()
        run = True 

        while run :
            clock.tick(FPS)
            game_info  = self.game.loop()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    run = False 
                    break 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] :
                self.game.move_paddle(left = True , up = True )
            elif keys[pygame.K_s]:
                self.game.move_paddle(left = True , up = False)

            if keys[pygame.K_UP]:
                self.game.move_paddle( False , up = True )
            elif keys[pygame.K_DOWN] :
                self.game.move_paddle(False , up = False)

            self.game.draw(draw_score = False)
            pygame.display.update()

    """def run_neat(config):
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(1))

        winner = p.run(eval_genomes , 50)

        with open("best.pickle" , "wb") as f :
            pickle.dump(winner , f)"""


if __name__ == "__main__":
    # main screen constants 
    WIDTH , HEIGHT = 1000 , 600 
    FPS = 60 
    WIN = pygame.display.set_mode((WIDTH , HEIGHT))
    pygame.display.set_caption("Pong game")
    
    pong = PongGame(WIN , WIDTH , HEIGHT)
    pong.run()
