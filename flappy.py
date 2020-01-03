import random
import pygame


pygame.init()

white = (255,255,255)
black = (0,0,0)

cornflower_blue = (39,58,93)

size = (1280,720)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("code to use")

clock = pygame.time.Clock()

arial30 = pygame.font.SysFont('arial',30, False, False)

pipes = []

score = 0

class Bird():
    def __init__(self):
        self.x = 250
        self.y = 250
        self.yV = 0
    
    def flap(self):
        self.yV = -10
    
    def update(self):
        self.yV += 0.5
        self.y += self.yV

    def draw(self):
        pygame.draw.rect(screen,cornflower_blue,(self.x,self.y,40,40))
    
    def reset(self):
        self.x = 250
        self.y = 250
        self.yV = 0

bird = Bird()

class Pipe():
    def __init__(self):
        self.centerY = random.randrange(130,520)
        self.x = 1280
        self.size = 100
    
    def update(self):
        global pipes
        global bird
        global gameState
        global score
        self.x -= 4
        if self.x == 500:
            pipes.append(Pipe())

        if self.x <= -80:
            del pipes[0]

        if self.x >= 170 and self.x <= 290 and bird.y <= (self.centerY - self.size) or self.x >= 170 and self.x <= 290 and (bird.y + 40) >= (self.centerY + self.size):
            gameState = 3

        if self.x == 168 and bird.y > (self.centerY - 100) and bird.y < (self.centerY + 100):
            score += 1

        if bird.y >= 640:
            gameState = 3
    
    def draw(self):
        pygame.draw.rect(screen,black,(self.x,0,80,(self.centerY - self.size)))
        pygame.draw.rect(screen,black,(self.x,(self.centerY + self.size),80,(580 - self.centerY)))

pipes.append(Pipe())
gameState = 2

done = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            if gameState == 3:
                bird.reset()
                pipes = []
                pipes.append(Pipe())
                gameState = 2
                score = 0
            else:
                bird.flap()
    
    screen.fill(white)
    pygame.draw.rect(screen,black,(0,680,1280,40))

    if gameState == 2:
        bird.update()
        bird.draw()

        for pipe in pipes:
            pipe.update()
            pipe.draw()

        center_position_of_bird = bird.y + 20.0
        center_position_of_pipe = pipes[0].centerY
        distance_between_pipe_and_bird = pipes[0].x - 290
        if distance_between_pipe_and_bird <= 0:
        	distance_between_pipe_and_bird = 0 
        
        text = arial30.render('score = '+str(distance_between_pipe_and_bird),True,cornflower_blue)
        screen.blit(text,(640, 20))
    	 
        text = arial30.render('gen = '+str(center_position_of_bird),True,cornflower_blue)
        screen.blit(text,(320, 20))
    	 
        text = arial30.render('alive = '+str(center_position_of_pipe),True,cornflower_blue)
        screen.blit(text,(960, 20))
    	
    if gameState == 3:
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()