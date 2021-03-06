"""
GameModels.py
Reinforcement Learning Agent object.
Imported into app.py

author: @justjoshtings
created: 3/16/2022
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, backend
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D
from tensorflow.keras.optimizers import Adam

import numpy as np
from copy import deepcopy

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.callbacks import ModelIntervalCheckpoint
from rl.core import Processor

from ImageProcessor import AtariProcessor

import gym
import ale_py

# Random Seed
random_seed = 42
# Set random seed in tensorflow
tf.random.set_seed(random_seed)
# Set random seed in numpy
np.random.seed(random_seed)

class DQNAgentService:
    '''
    Object to wrap DQN keras rl model object with gym atari environment.
    '''
    def __init__(self, model_height, model_width, env_name, window_length, model_name, model_channels=0):
        '''
        Params:
            self: instance of object
            model_height (int) : height of game state images to input into DQN model, 105
            model_width (int) : width of game state images to input into DQN model, 105
            env_game (str) : env name of Atari game to load, 'ALE/MsPacman-v5']
            window_length (int) : number of image game state stacks per input, 4
            model_name (str) : name of model
            model_channels (int) : 3 if want to use RGB, 0 if grayscale
        '''
        self.model_height = model_height
        self.model_width = model_width
        self.env_name = env_name
        self.window_length = window_length
        self.model_name = model_name
        self.model_channels = model_channels

        self.env = gym.make(self.env_name)
        self.env_height, self.env_width, self.env_channels = self.env.observation_space.shape
        self.actions = self.env.action_space.n

    def build_model(self):
        '''
        Method to build model

        Params:
            self: instance of object

        Returns:
            self.model: keras model instance
        '''
        backend.clear_session()

        if self.model_channels > 0:
            self.input_shape=(self.window_length, self.model_height, self.model_width, self.model_channels)
        else:
            self.input_shape=(self.window_length, self.model_height, self.model_width)

        inputs = layers.Input(shape = self.input_shape)

        conv1 = layers.Conv2D(32, (8, 8), strides=(4,4), activation='relu', padding='same', name='conv1')(inputs)
        conv2 = layers.Conv2D(64, (4, 4), strides=(2,2), activation='relu', padding='same', name='conv2')(conv1)
        conv3 = layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv3')(conv2)

        flatten = layers.Flatten()(conv3)

        dense1 = layers.Dense(512, activation='relu')(flatten)
        dense2 = layers.Dense(256, activation='relu')(dense1)
        final_layer = layers.Dense(self.actions, activation='linear')(dense2)

        self.model = models.Model(inputs=inputs, outputs=final_layer, name=self.model_name)

        return self.model

    def build_agent(self, policy_value_max, policy_value_min, policy_value_test, policy_nb_steps, enable_double_dqn, enable_dueling_network, dueling_type, nb_steps_warmup, replay_memory=None):
        '''
        Method to build agent

        Params:
            self: instance of object
            policy_value_max (float) : between 0 and 1 representing max value of epsilon in epsilon-greedy linear annealing
            policy_value_min (float) : between 0 and 1 representing min value of epsilon in epsilon-greedy linear annealing
            policy_value_test (float) : between 0 and 1 representing value of epsilon during testing
            policy_nb_steps (int) : number of steps from start of training to decrease epsilon before setting epsilon to policy_value_min
            enable_double_dqn (Boolean) : enable double dqn
            enable_dueling_network (Boolean) : enable dueling dqn
            dueling_type (str) : 'avg'
            nb_steps_warmup (int) : number of steps to warmup before training
            replay_memory (SequentialMemory): if not None, replay memory to load into DQNAgent() for continuiation of training. Otherwise, create new SequentialMemory.

        Returns:
            dqn: dqn model
        '''
        # Policy hyperparameters
        self.policy_value_max = policy_value_max
        self.policy_value_min = policy_value_min
        self.policy_value_test = policy_value_test
        self.policy_nb_steps = policy_nb_steps

        # Agent hyperparameters
        self.enable_double_dqn = enable_double_dqn
        self.enable_dueling_network = enable_dueling_network
        self.dueling_type = dueling_type
        self.nb_steps_warmup = nb_steps_warmup

        self.policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.1, nb_steps=8000) # For 1 million total steps, I think having the policy nb_steps around 600k is a good slope.
        self.processor = AtariProcessor((self.model_height,self.model_width))
        # If we want to load from saved memory
        if replay_memory:
            self.memory = replay_memory
        else:
            self.memory = SequentialMemory(limit=10000, window_length=self.window_length)
            
        self.dqn = DQNAgent(model=self.model, memory=self.memory, policy=self.policy,
                        enable_double_dqn=False,
                        enable_dueling_network=True, dueling_type='avg',
                        processor=self.processor,
                        nb_actions=self.actions, nb_steps_warmup=2500 #nb_steps_warmup reduces instability of first few steps https://datascience.stackexchange.com/questions/46056/in-keras-library-what-is-the-meaning-of-nb-steps-warmup-in-the-dqnagent-objec
                        )
        return self.dqn

    def load_weights(self, model_path):
        '''
        Method to load weights

        Params:
            self: instance of object
            model_path (str) : path of saved model weights
        '''
        self.dqn.compile(Adam(learning_rate=1e-4))
        try:
            self.dqn.load_weights(model_path)
        except OSError:
            print("Weights file {} not found".format(model_path))
    
    def get_model(self):
        '''
        Method to return dqn model
        '''
        return self.dqn

    def play(self, n_episodes, render_mode='human'):
        '''
        Method to play game with model iteratively (one step of env at a time)

        Params:
            self: instance of object
            render_mode (str) : mode to render gameplay in ['human', 'rgb', None]
        '''
        self.env = gym.make(self.env_name, render_mode=render_mode) #render_mode = ('human','rgb',None)

        self.dqn.training = False
        action_repetition = 1

        for i in range(n_episodes):
            episode_reward = 0.
            observation = deepcopy(self.env.reset())
            if self.dqn.processor is not None:
                observation = self.dqn.processor.process_observation(observation)
            assert observation is not None

            action = 0
            done = False
            # Run the episode until we're done.
            while not done:
                action = self.dqn.forward(observation)
                if self.dqn.processor is not None:
                    action = self.dqn.processor.process_action(action)
                reward = 0.
                for _ in range(action_repetition):
                    observation, r, d, info = self.env.step(action)
                    observation = deepcopy(observation)
                    if self.dqn.processor is not None:
                        observation, r, d, info = self.dqn.processor.process_step(
                            observation, r, d, info)
                    reward += r
                    if d:
                        done = True
                        break
                
                self.dqn.backward(reward, terminal=done)
                episode_reward += reward

                self.dqn.step += 1

    def play_gen(self, n_episodes=1, render_mode=None):
        '''
        Method to play game with model iteratively, yielding observation, action after each iteration of game step.
        Acts as a generator.

        Params:
            self: instance of object
            n_episodes (int) : number of episodes to play
            render_mode (str) : mode to render gameplay in ['human', 'rgb', None]
        '''
        self.env = gym.make(self.env_name, render_mode=render_mode) #render_mode = ('human','rgb',None)

        self.dqn.training = False
        action_repetition = 1

        for i in range(n_episodes):
            episode_reward = 0.
            observation = deepcopy(self.env.reset())
            observation_deprocessed = deepcopy(observation)
            if self.dqn.processor is not None:
                observation = self.dqn.processor.process_observation(observation)
            assert observation is not None

            action = 0
            done = False
            # Run the episode until we're done.
            while not done:
                yield (observation, observation_deprocessed, action, done)

                action = self.dqn.forward(observation)
                if self.dqn.processor is not None:
                    action = self.dqn.processor.process_action(action)
                reward = 0.
                for _ in range(action_repetition):
                    observation, r, d, info = self.env.step(action)
                    observation = deepcopy(observation)
                    observation_deprocessed = deepcopy(observation)
                    if self.dqn.processor is not None:
                        observation, r, d, info = self.dqn.processor.process_step(
                            observation, r, d, info)
                    reward += r
                    if d:
                        done = True
                        break
                
                self.dqn.backward(reward, terminal=done)
                episode_reward += reward

                self.dqn.step += 1


if __name__ == "__main__":
    print('Executing test play', __name__)

    def load_model(model_path, env_name):
        '''
        Method to load model

        Params:
            model_path (str) : path to model weights file
            env_name (str) : name of game environment
        '''
        # Model parameters
        window_length = 4
        input_shape = (105, 105)
        
        ms_pacman_model = DQNAgentService(model_height=input_shape[0], model_width=input_shape[1], env_name=env_name, window_length=window_length, model_name='Final_Model', model_channels=0)
        ms_pacman_model.build_model()
        ms_pacman_model.build_agent(policy_value_max=1., policy_value_min=.1, policy_value_test=.1, policy_nb_steps=8000, 
                            enable_double_dqn=False, enable_dueling_network=True, dueling_type='avg', nb_steps_warmup=2500)
        ms_pacman_model.load_weights(model_path)

        return window_length, input_shape, ms_pacman_model

    path = './models/Dueling_DQN_Round2_weights_final_steps15000.h5f'
    window_length, input_shape, ms_pacman_model = load_model(path, 'ALE/MsPacman-v5')
    ms_pacman_model.play(2)

    # for ob, action, done in ms_pacman_model.play_gen():
    #     print(ob,action,done)
    #     if done:
    #         break
    
else:
    print('Importing', __name__)

