import gym
import ale_py
import cv2
import numpy as np
from matplotlib import pyplot as plt

def build_env():
    env = gym.make('ALE/MsPacman-v5')
    height, width, channels = env.observation_space.shape
    actions = env.action_space.n

    return env, actions

env, actions = build_env()
observation = env.reset()

observation = cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)
_, img_encoded = cv2.imencode('.png', observation)
img_string = img_encoded.tobytes()
npimg = np.frombuffer(img_string, dtype=np.uint8)
img = cv2.imdecode(npimg, 1)
cv2.imshow('Image PNG', img)
cv2.waitKey(10000)

plt.imshow(img)
plt.show()

# _, img_encoded = cv2.imencode('.jpg', observation)
# img_string = img_encoded.tobytes()
# npimg = np.frombuffer(img_string, dtype=np.uint8)
# img = cv2.imdecode(npimg, 1)
# cv2.imshow('Image JPEG', img)
# cv2.waitKey(10000)