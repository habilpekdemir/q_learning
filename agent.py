import random
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D
from collections import deque

number_of_actions = 3
image_height = 40
image_width = 40
image_history = 4


observe_period = 2000
gamma = 0.975
batch_size = 64

experience_capacity = 2000

class Agent :

	def __init__(self):
		self.model = self.create_model()
		self.experience_replay = deque()
		self.steps = 0 
		self.epsilon = 1.0




	def create_model(self):
		model = Sequential()

		model.add(Conv2D(32, kernel_size = 4, strides = (2,2), input_shape = (image_height, image_width, image_history),padding = "same"))
		model.add(Activation("relu"))

		model.add(Conv2D(64, kernel_size = 4, strides = (2,2), padding = "same"))
		model.add(Activation("relu"))

		model.add(Conv2D(64, kernel_size = 3, strides = (1,1), padding = "same"))
		model.add(Activation("relu"))
		
		model.add(Flatten())
		model.add(Dense(512))

		model.add(Activation("relu"))
		model.add(Dense(units = number_of_actions, activation = "linear"))

		model.compile(loss = "mse", optimizer = "adam")

		return model

	def find_best_action(self, s):
		if random.random() < self.epsilon or self.steps < observe_period:
			return random.randint(0,number_of_actions - 1)

		else:
			qvalue = self.model.predict(s)
			best_action = np.argmax(qvalue)
			return best_action

	def capture_sample(self, sample):
		self.experience_replay.append(sample)
		if len(self.experience_replay) > experience_capacity:
			self.experience_replay.popleft()

		self.steps += 1

		self.epsilon = 1.0

		if self.steps > observe_period:
			self.epsilon = 0.75

			if self.steps > 7000:
				self.epsilon = 0.5

			if self.steps > 14000:
				self.epsilon = 0.25

			if self.steps > 30000:
				self.epsilon = 0.15

			if self.steps > 45000:
				self.epsilon = 0.1

			if self.steps > 70000:
				self.epsilon = 0.05


	def process(self):
		if self.steps > observe_period:
			mini_batch = random.sample(self.experience_replay, batch_size)
			batch_len = len(mini_batch)

			inputs = np.zeros((batch_size, image_height, image_width, image_history))
			targets = np.zeros((inputs.shape[0], number_of_actions))

			q_sa = 0

			for i in range(batch_len):
				state_t = mini_batch[i][0]
				action_t = mini_batch[i][1]
				reward_t = mini_batch[i][2]
				state_t1 = mini_batch[i][3]

				inputs[i:i + 1] = state_t
				targets[i] = self.model.predict(state_t)
				q_sa = self.model.predict(state_t1)

				if state_t1 is None:
					targets[i, action_t] = reward_t

				else:
					targets[i, action_t] = reward_t + gamma*np.max(q_sa)

			self.model.fit(inputs, targets, batch_size, epochs = 1, verbose = 0)





























