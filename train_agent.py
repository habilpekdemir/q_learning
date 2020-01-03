import agent, ai_pong

import numpy as np
import skimage as skimage
from skimage.color import lab2rgb, lch2lab
from skimage.transform import resize
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


total_train_time = 100000

image_height = 40
image_width = 40
image_history = 4

def process_game_image(raw_image):

	grey_image = skimage.color.rgb2gray(raw_image)

	cropped_image = grey_image[0:400, 0:400]

	reduced_image = skimage.transform.resize(cropped_image,(image_height, image_width))
	reduced_image = skimage.exposure.rescale_intensity(reduced_image, out_range = (0, 255))

	reduced_image = reduced_image / 128

	return reduced_image

def train_experiment():
	train_history = []

	the_game = ai_pong.PongGame()

	the_game.InitialDisplay()

	the_agent = agent.Agent()

	best_action = 0

	[Initialscore, InitialScreenImage] = the_game.PlayNextMove(best_action)

	InitialGameImage =  process_game_image(InitialScreenImage)

	game_state = np.stack((InitialGameImage, InitialGameImage, InitialGameImage, InitialGameImage), axis = 2)

	game_state = game_state.reshape(1, game_state.shape[0], game_state.shape[1], game_state.shape[2])

	for i in range(total_train_time):

		best_action = the_agent.find_best_action(game_state)
		[return_score, new_screen_image] = the_game.PlayNextMove(best_action)

		new_game_image =  process_game_image(new_screen_image)

		new_game_image = new_game_image.reshape(1, new_game_image.shape[0], new_game_image.shape[1], 1)

		next_state = np.append(new_game_image, game_state[:,:,:,:3], axis = 3)

		the_agent.capture_sample((game_state, best_action, return_score, next_state))

		the_agent.process()

		game_state = next_state

		if i % 250 == 0:
			print("train time : ", str(i), "game score : ", the_game.GScore)
			train_history.append(the_game.GScore)

train_experiment()





