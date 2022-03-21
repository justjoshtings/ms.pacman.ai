"""
ImageProcessor.py
Object to perform pre & post processing of Atari env game states. To preprocess env images to grayscale and compress shape: https://github.com/keras-rl/keras-rl/blob/master/examples/dqn_atari.py
Imported into app.py, GameModels.py

author: @justjoshtings
created: 3/16/2022
"""

from rl.core import Processor
from PIL import Image
import numpy as np
import cv2

# Random Seed
# The random seed
random_seed = 42
# Set random seed in numpy
np.random.seed(random_seed)

class AtariProcessor(Processor):
  '''
  AtariProcessor to perform pre-processing on game state images before input into model
  '''
  def __init__(self, input_shape):
    '''
    Params:
      self: instance of object
      input_shape (tuple) : (height,width) of desired input into DQN model, (105,105)
    '''
    self.input_shape = input_shape

  def process_observation(self, observation):
    '''
    Method to process observations from game state
    
    Params:
      self: instance of object
      observation (np.array) : game state observation

    Returns:
      processed observation (np.array)
    '''
    assert observation.ndim == 3  # (height, width, channel)
    img = Image.fromarray(observation)
    img = img.resize(self.input_shape).convert('L')  # resize and convert to grayscale
    processed_observation = np.array(img)
    assert processed_observation.shape == self.input_shape
    
    return processed_observation.astype('uint8')  # saves storage in experience memory

  def process_state_batch(self, batch):
    '''
    Method to process game state batch
    
    Params:
      self: instance of object
      batch (np.array) : batch of game state observation

    Returns:
      processed batch (np.array)
    '''
    # We could perform this processing step in `process_observation`. In this case, however,
    # we would need to store a `float32` array instead, which is 4x more memory intensive than
    # an `uint8` array. This matters if we store 1M observations.
    processed_batch = batch.astype('float32') / 255.
    return processed_batch

  def process_reward(self, reward):
    '''
    Method to process reward
    
    Params:
      self: instance of object
      reward (int) : reward

    Returns:
      reward (int) : reward
    '''
    return reward

  
class PostProcessor:
  '''
  PostProcessor object to perform post-processing before broadcasting to live stream.
  '''
  def __init__(self):
    pass
  
  def broadcast_ready(self, observation, n_frame, fps):
    '''
    Method to perform post-processing on observation game state images to be broadcast ready.

    Params:
      self: instance of object
      observation (np.array) : game state observation
      n_frame (int) : current frame number in episode
      fps (int) : most recent steps' fps

    Returns:
      observation_broadcast(np.array) : game state observation with post-processing
    '''
    observation_broadcast = observation
    observation_broadcast = cv2.resize(observation_broadcast, dsize=(700,600), interpolation=cv2.INTER_AREA)
    observation_broadcast = cv2.cvtColor(observation_broadcast, cv2.COLOR_RGB2BGR)
    
    observation_broadcast = cv2.putText(observation_broadcast,
                                text='Frame {}, {}FPS'.format(n_frame, fps), 
                                org=(50,560), 
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                fontScale=0.4,
                                color=(255,255,255), #BGR
                                thickness=1)

    return observation_broadcast


if __name__ == "__main__":
    print('Executing', __name__)
else:
    print('Importing', __name__)