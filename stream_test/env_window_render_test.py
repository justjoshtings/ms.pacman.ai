# pip3 install 'gym[atari,accept-rom-license]==0.22.0'

import matplotlib.pyplot as plt
import gym
from gym import wrappers
import random
import numpy as np

env = gym.make('ALE/MsPacman-v5', render_mode='rgb_array')
height, width, channels = env.observation_space.shape
actions = env.action_space.n

episodes = 1

random_model_scores = []

# Saves .mp4 and .json files
# env = wrappers.Monitor(env, "./gym-results", force=True)

game_arrays = []

for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        # action = random.choice([0,1,2,3,4,5,6,7,8])
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        game_arrays.append(env.render(mode='rgb_array'))
        # action: int - 0,1,2,3,4,5,6,7,8
        # n_state: numpy array - dimensions (210, 160, 3) --> (height, width, RGB channels)
        # reward: float - 0.0
        # done: boolean - True, False
        # info: dictionary - {'lives': 1, 'episode_frame_number': 1892, 'frame_number': 1892}
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
    # env.play()

    random_model_scores.append(score)

env.close()

# Get numpy array of game to plot later on
game_array = np.stack(game_arrays, axis=3)
game_array = np.rollaxis(game_array, -1)
print(game_array.shape)

for i in range(20):
    plt.imshow(game_array[i,:,:,:])
    plt.show()

# Create video stream from numpy arrays in matplotlib
# https://ben.bolte.cc/matplotlib-videos
