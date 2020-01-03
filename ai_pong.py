import pygame 
import random

FPS = 60

window_width = 400
window_height = 420
game_height = 400

paddle_width = 15
paddle_height = 60
paddle_buffer = 15

ball_width = 20
ball_height = 20

paddle_speed  = 3

ball_x_speed = 2
ball_y_speed = 2

white = (255, 255, 255)
black = (0, 0, 0)
cornflower_blue = (39,58,93)

screen = pygame.display.set_mode((window_width, window_height))


def drawPaddle(switch, paddleYPos):

	if switch == "left":
		paddle = pygame.Rect(paddle_buffer, paddleYPos, paddle_width, paddle_height)
		pygame.draw.rect(screen, white, paddle)

	elif switch == "right":
		paddle = pygame.Rect(window_width - paddle_buffer - paddle_width, paddleYPos, paddle_width, paddle_height)
		pygame.draw.rect(screen, cornflower_blue, paddle)

def drawBall(ballXPos, ballYPos):

	ball = pygame.Rect(ballXPos, ballYPos, ball_width, ball_height)
	pygame.draw.rect(screen, white, ball)

def updatePaddle (switch, action, paddleYPos, ballYPos):
	dft = 7.5

	if switch == "left":

		if action == 1:
			paddleYPos = paddleYPos - paddle_speed*dft

		if action == 2:
			paddleYPos = paddleYPos + paddle_speed*dft

		if paddleYPos < 0 :
			paddleYPos = 0

		if paddleYPos > game_height - paddle_height:
			paddleYPos = game_height - paddle_height

		return paddleYPos
		
	elif switch == "right":
		if paddleYPos + paddle_height/2 < ballYPos + ball_height/2:
			paddleYPos = paddleYPos + paddle_speed*dft

		if paddleYPos + paddle_height/2 > ballYPos + ball_height/2:
			paddleYPos = paddleYPos - paddle_speed*dft

		if paddleYPos < 0 :
			paddleYPos = 0

		if paddleYPos > game_height - paddle_height:
			paddleYPos = game_height - paddle_height

		return paddleYPos

def updateBall (paddle1YPOS, paddle2YPOS, ballXPos, ballYPos, ballXDirection, ballYDirection, dft):

	dft = 7.5

	ballXPos = ballXPos + ballXDirection*ball_x_speed*dft

	ballYPos = ballYPos + ballYDirection*ball_y_speed*dft

	score = -0.05

	if (ballXPos <= (paddle_buffer + paddle_width)) and ((ballYPos + ball_height) >= paddle1YPOS) and (ballYPos <= (paddle1YPOS + paddle_height)) and (ballXDirection == -1):
		ballXDirection = 1

		score = 10


	elif (ballXPos <= 0):
		ballXDirection = 1

		score = -10 

		return [score, ballXPos, ballYPos, ballXDirection, ballYDirection]

	if ((ballXPos >= (window_width - paddle_width - paddle_buffer)) and ((ballYPos + ball_height)>= (paddle2YPOS )) and (ballYPos <= (paddle2YPOS + paddle_height)) and (ballXDirection == 1)):
		ballXDirection = -1

	elif ballXPos >= (window_width - ballYDirection):
		ballXDirection = -1

		return [score, ballXPos, ballYPos, ballXDirection, ballYDirection]

	if ballYPos <= 0:
		ballYPos = 0
		ballYDirection = 1

	elif ballYPos >= window_height - ball_height:
		ballYPos = window_height - ball_height
		ballYDirection = -1

	return [score, ballXPos , ballYPos ,ballXDirection ,ballYDirection]


class PongGame():

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("CTU PongGame")

		self.paddle1YPOS = game_height/2 - paddle_height/2
		self.paddle2YPOS = game_height/2 - paddle_height/2

		self.ballXDirection = random.sample([-1,1],1)[0]
		self.ballYDirection = random.sample([-1,1],1)[0]

		self.ballXPos = window_width/2
		self.ballYPos = random.randint(0, 9)*(window_height - ball_height) / 9

		self.clock = pygame.time.Clock()
		self.GScore = 0.0
	def InitialDisplay(self):

		pygame.event.pump()
		screen.fill(black)

		drawPaddle("left", self.paddle1YPOS)
		drawPaddle("right", self.paddle2YPOS)

		drawBall(self.ballXPos, self.ballYPos)

		pygame.display.flip()

	def PlayNextMove(self, action):
		
		DeltaFrameTime = self.clock.tick(FPS)
		pygame.event.pump()

		score = 0
		screen.fill(black)

		self.paddle1YPOS =  updatePaddle("left", action, self.paddle1YPOS, self.ballYPos)
		drawPaddle("left", self.paddle1YPOS)

		self.paddle2YPOS =  updatePaddle("right", action, self.paddle2YPOS, self.ballYPos)
		drawPaddle("right", self.paddle2YPOS)

		[score, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection] = updateBall(self.paddle1YPOS, self.paddle2YPOS, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection, DeltaFrameTime)

		drawBall(self.ballXPos, self.ballYPos)

		if (score > 0.5 or score < -0.5):
			self.GScore =self.GScore*0.9 + 0.1*score 

		ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())

		pygame.display.flip()

		return [score, ScreenImage]













