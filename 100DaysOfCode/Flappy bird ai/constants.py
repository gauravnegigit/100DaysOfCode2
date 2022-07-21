import pygame
pygame.init()

# screen constants 
WIDTH , HEIGHT = 600 , 700
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60 

# sprites 

BACKGROUND = pygame.image.load("Assets/background.png")
GROUND = pygame.image.load("Assets/ground.png")
MENU = pygame.transform.scale((pygame.image.load('Assets/menu.png')) , (250 , 100))

# sound constants
JUMP = pygame.mixer.Sound('Sounds/jump.wav')
MUSIC = pygame.mixer.Sound('Sounds/music.wav')


# number for the score

NUMBERS = (
	pygame.image.load("Assets/numbers/0.png"),
	pygame.image.load("Assets/numbers/1.png"),
	pygame.image.load("Assets/numbers/2.png"),
	pygame.image.load("Assets/numbers/3.png"),
	pygame.image.load("Assets/numbers/4.png"),
	pygame.image.load("Assets/numbers/5.png"),
	pygame.image.load("Assets/numbers/6.png"),
	pygame.image.load("Assets/numbers/7.png"),
	pygame.image.load("Assets/numbers/8.png"),
	pygame.image.load("Assets/numbers/9.png")
)

# messages for the game
MESSAGE1 = pygame.image.load("Assets/message1.png")
MESSAGE2 = pygame.image.load("Assets/message2.png")