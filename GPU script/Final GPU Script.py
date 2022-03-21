# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:18:13 2022

@author: adamkritz
"""

import gym
import tensorflow as tf
from tensorflow import keras
import os
import numpy as np
import warnings
import random

print('First Imports Complete')

# Ignore warnings
warnings.filterwarnings('ignore')

# Random Seed

# The random seed
random_seed = 42

# Set random seed in tensorflow
tf.random.set_seed(random_seed)

# # Set random seed in numpy
np.random.seed(random_seed)

# Check what version of TF we are using
print(tf.version.VERSION)

# Print the number of GPUs available
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Test to see if GPU is found and connected
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  print('GPU device not found')
else:
  print('\nFound GPU at: {}'.format(device_name))

print('Gpu Finding Complete')


abspath_curr = os.getcwd()

print(os.getcwd())

env = gym.make('ALE/MsPacman-v5')
height, width, channels = env.observation_space.shape
actions = env.action_space.n

print(height, width, channels)

env.unwrapped.get_action_meanings()

print('Environment Loaded')

print('Begin Random Model')

skip = False

if not skip:
  # Run for 1000 games
  episodes = 1000

  random_model_scores = []
  random_model_steps = []

  for episode in range(1, episodes+1):
      state = env.reset()
      done = False
      score = 0
      steps = 0
      
      while not done:
          action = random.choice([0,1,2,3,4,5,6,7,8])
          n_state, reward, done, info = env.step(action)
          score += reward
          steps += 1
      print('Episode:{} Score:{} Steps:{}'.format(episode, score, steps))
      # env.play()

      random_model_scores.append(score)
      random_model_steps.append(steps)

  env.close()

print('random model finished playing')

# Make scores results directory; 

random_model_scores_file = abspath_curr + '/results/random_model_scores_1k_episodes_3_9_22.txt'
random_model_steps_file = abspath_curr + '/results/random_model_steps_1k_episodes_3_9_22.txt'

print('Made Random Model Text Files')

# Save random_model_scores
random_model_scores = np.array(random_model_scores)
random_model_steps = np.array(random_model_steps)
np.savetxt(random_model_scores_file, random_model_scores, fmt='%d')
np.savetxt(random_model_steps_file, random_model_steps, fmt='%d')

print('Saved Random Model Scores')

from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.callbacks import ModelIntervalCheckpoint
from rl.core import Processor

from PIL import Image

print('More Importants Complete')

window_length = 4
INPUT_SHAPE = (105, 105) 

class AtariProcessor(Processor):
  def process_observation(self, observation):
    assert observation.ndim == 3  # (height, width, channel)
    img = Image.fromarray(observation)
    img = img.resize(INPUT_SHAPE).convert('L')  # resize and convert to grayscale
    processed_observation = np.array(img)
    assert processed_observation.shape == INPUT_SHAPE
    
    return processed_observation.astype('uint8')  # saves storage in experience memory

  def process_state_batch(self, batch):
    # We could perform this processing step in `process_observation`. In this case, however,
    # we would need to store a `float32` array instead, which is 4x more memory intensive than
    # an `uint8` array. This matters if we store 1M observations.
    processed_batch = batch.astype('float32') / 255.
    return processed_batch

  def process_reward(self, reward):
    return reward
    # clipping rewards messes up the rewards output
    # return np.clip(reward, -1., 1.)
   
print('created atari class')   
    
# This model approximates the target Q function
def build_model(height, width, actions, window_length, model_name, channels=0):
  '''
  Function to build a copy of DeepMind's DQN model that approximates the optimal target Q function
  '''
  keras.backend.clear_session()

  if channels > 0:
    input_shape=(window_length, height, width, channels)
  else:
    input_shape=(window_length, height, width)
  inputs = layers.Input(shape = input_shape)

  conv1 = layers.Conv2D(32, (8, 8), strides=(4,4), activation='relu', padding='same', name='conv1')(inputs)
  conv2 = layers.Conv2D(64, (4, 4), strides=(2,2), activation='relu', padding='same', name='conv2')(conv1)
  conv3 = layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv3')(conv2)

  flatten = layers.Flatten()(conv3)

  dense1 = layers.Dense(512, activation='relu')(flatten)
  dense2 = layers.Dense(256, activation='relu')(dense1)
  final_layer = layers.Dense(actions, activation='linear')(dense2)

  model = models.Model(inputs=inputs, outputs=final_layer, name=model_name)

  return model

model_name = 'Dueling_DQN_Beta'
model = build_model(INPUT_SHAPE[0], INPUT_SHAPE[1], actions, window_length, model_name)

model.summary()

print('Finished Building Model')

def build_agent(model, actions, window_length, replay_memory=None):
  '''
  Function to build agent

  Parameters:
    model (keras model): keras model object
    actions (list): list of of integers representing actions
    window_length (int): integer represent the number of steps to stack as inputs from step time t, t-1, t-2, ...
    replay_memory (SequentialMemory): if not None, replay memory to load into DQNAgent() for continuiation of training. Otherwise, create new SequentialMemory.

  Returns:
    dqn: dqn model
  '''
  policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.1, nb_steps=600000) # For 1 million total steps, I think having the policy nb_steps around 600k is a good slope.
  processor = AtariProcessor()
  # If we want to load from saved memory
  if replay_memory:
    memory = replay_memory
  else:
    memory = SequentialMemory(limit=500000, window_length=window_length)
    
  dqn = DQNAgent(model=model, memory=memory, policy=policy,
                enable_double_dqn=False,
                enable_dueling_network=True, dueling_type='avg',
                processor=processor,
                nb_actions=actions, nb_steps_warmup=2500 #nb_steps_warmup reduces instability of first few steps https://datascience.stackexchange.com/questions/46056/in-keras-library-what-is-the-meaning-of-nb-steps-warmup-in-the-dqnagent-objec
                )
  return dqn

print('finished building agent')

def train_model(model, actions, window_length, loading_from_step, total_steps_to_train, interval_steps_to_save, save_dir, model_name, opt, memory_file=None, weights_file=None):
  '''
  Wrapper function to wrap the training in order to have ability to save and load model weights & replay memory over x number of intervals.
  Also allows for continuation of training from a loaded model.

  Parameters:
    model (keras model): keras model object
    actions (list()): list of of integers representing actions
    window_length (int): integer represent the number of steps to stack as inputs from step time t, t-1, t-2, ...
    save_dir (str): directory to save model weights and memory replay
    mode (str): training mode of form string with options from ['from_scratch', 'resuming_from_load']
    loading_from_step (int): The last step that was finished training model/memory were saved, will resume on last_finished_training_step + 1. Set to 0 if completely new model.
    total_steps_to_train (int): the total number of steps to train
    interval_steps_to_save (int): the intervals to save model and memory
    model_name (str): name of model to load from in model.name
    opt (keras optimizer): model optimizer
    memory_file (str): name of memory file to load for resume training, pickle file
    weights_file (str): name of weights file to load for resume training, .h5f file

  Returns:
    dqn: dqn model

  https://github.com/keras-rl/keras-rl/issues/186
  '''
  directory = os.path.dirname(save_dir)
  if not os.path.exists(directory):
      os.makedirs(directory)

  # If start of first training round, build clean agent model to train
  if not memory_file and not weights_file:
    print('Training Mode: From Scratch', '\n\n')
    checkpoint_weights_filename = save_dir+model_name+'_weights_{step}.h5f'
    
    dqn = build_agent(model, actions, window_length)
    dqn.compile(opt)
  # Else if just resuming training from a previous load, we rebuild the agent model with the reloaded memory and reload weights
  elif memory_file and weights_file:
    print('Training Mode: From Loaded Model', '\n\n')
    checkpoint_weights_filename = save_dir+model_name+'_weights_'+str(loading_from_step)+'+{step}.h5f'

    # try:
    #   memory = pickle.load(open(save_dir+memory_file, "rb"))
    # except (FileNotFoundError, EOFError):
    #   print("Memory file {} not found".format(save_dir+memory_file))
    dqn = build_agent(model, actions, window_length)
    dqn.compile(opt)
    try:
      dqn.load_weights(save_dir+weights_file)
    except (OSError):
      print("Weights file {} not found".format(save_dir+weights_file))
  
  # Build call backs:
  callbacks = []
  # 1. Tensorboard logging (not working, need to downgrade TF to 2.3, currently 2.8)
  # logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
  # tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)
  # callbacks.append(tensorboard_callback)

  # 2. ModelIntervalCheckpoint
  model_interval_checkpoint = ModelIntervalCheckpoint(checkpoint_weights_filename, interval=interval_steps_to_save, verbose=1)
  callbacks.append(model_interval_checkpoint)
  
  # Train
  print('Training...')
  dqn.fit(env, nb_steps=total_steps_to_train-loading_from_step, visualize=False, verbose=2, callbacks=callbacks)

  print('Saving Weights and Replay Memory')
  # Save weights, .h5f objects cannot be pickled
  dqn.save_weights(save_dir+'{}_weights_final_steps{}.h5f'.format(model_name, total_steps_to_train), overwrite=True)

  # Save replay experience memory
  #pickle.dump(dqn.memory, open(save_dir+"{}_memory_final_steps{}.pkl".format(model_name, total_steps_to_train), "wb"))

  return dqn

print('finished building train model')

#Dueling_DQN_Round2 (Beta) [Avg Score 625.7] 35mins: dueling, window = 4, shape = (105,105), gamma = commented out, warmup = 2500, exploration=8000, test_eps = 0.1

save_dir = abspath_curr + '/results/'
opt = Adam(lr=1e-4)

# The last step that was finished training model/memory were saved, will resume on loading_from_step + 1. 
loading_from_step = 0
# The total number of steps to train
total_steps_to_train = 1000000
# The intervals to save model and memory
interval_steps_to_save = 40000

dqn = train_model(model, actions, window_length, loading_from_step, total_steps_to_train, interval_steps_to_save, save_dir, model_name, opt, memory_file=None, weights_file=None)

print('Ran Train Model')

os.chdir(abspath_curr + '/results')

#Uploads all of the results folder to AWS bucket

import boto3

# This is my access and secret key for Josh's account

ACCESS_KEY =  'access key here'
SECRET_KEY =  'secret key here'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False

x = os.listdir()

for i in x :
    upload_to_aws(i, 'insert_aws_bucket_name', i)

print('Uploaded All Files')

