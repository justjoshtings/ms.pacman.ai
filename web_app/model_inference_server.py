"""
model_inference_server.py

Server side logic to handle model inference from client web_server.py
Delivers frame by frame of model's playthrough to the web_server.py through TCP/IP connection.

author: @justjoshtings
created: 3/16/2022
"""

import socket
import threading
import numpy as np
import cv2
import pickle
import struct
import os
from time import sleep
import time
import copy
from datetime import datetime
import atexit

from MsPacmanAI.Logger import MyLogger
from MsPacmanAI.GameModels import DQNAgentService
from MsPacmanAI.ImageProcessor import PostProcessor
from MsPacmanAI import socket_server_credentials

def get_ip():
    '''
    Gets IP of machine to listen on

    Returns:
        IP (str) : IP address of current machine
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    
    MY_LOGGER.info(f'{datetime.now()} -- Server IP: {IP}')
    return IP

def start():
    '''
    Start server listening procedure and passes connections to handle_client() with multithread.
    '''
    LOG_FILENAME = '../logs/model_inference_server.log'

    # Set up a specific logger with our desired output level
    mylogger = MyLogger(LOG_FILENAME)
    global MY_LOGGER
    MY_LOGGER = mylogger.get_mylogger()

    PORT = socket_server_credentials.PORT
    HOST_NAME = socket.gethostname()
    HOST_IP = socket.gethostbyname(HOST_NAME)
    HOST_IP = get_ip()
    ADDR = (HOST_IP, PORT)

    print("[STARTING] Sever is starting...")
    MY_LOGGER.info(f"{datetime.now()} -- {datetime.now()} --[STARTING] Sever is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server listening on IP: {HOST_IP} and PORT: {PORT}")
    MY_LOGGER.info(f"{datetime.now()} -- [LISTENING] Server listening on IP: {HOST_IP} and PORT: {PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        MY_LOGGER.info(f"{datetime.now()} -- [ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    atexit.register(MY_LOGGER.goodbye)

def handle_client(conn, addr):
    '''
    Handles new client connection and sends message.

    Params:
        conn (socket.socket object) : object representing connection to client
        addr (tuple) : (IP address of client connection as str, port number as int)

    '''
    print(f"[NEW CONNECTION] {addr} connected.")
    MY_LOGGER.info(f"{datetime.now()} -- [NEW CONNECTION] {addr} connected.")

    connected = True
    try:
        while connected:
            for frame in stream_gameplay():
                serialise_frame = pickle.dumps(frame)
                message = struct.pack("Q",len(serialise_frame))+serialise_frame #Q: unsigned long long format, 8 bytes size
                # message consists of first n bytes of message + byte stream of image frame
                # print('Sending Packets, Packet Size',len(message))
                # MY_LOGGER.info(f'{datetime.now()} -- Sending Packets, Packet Size {len(message)}')
                conn.sendall(message)

            # For testing, send static
            # for i in range(100):
            #     img = np.random.randint(0,255,size=(400,400))
            #     serialise_img = pickle.dumps(img)
            #     message = struct.pack("Q",len(serialise_img))+serialise_img #Q: unsigned long long format, 8 bytes size
            #     # message consists of first n bytes of message + byte stream of image frame
            #     conn.sendall(message)
            #     img = img.astype(np.uint8)
            
            connected = False
    except BrokenPipeError:
        print(f"[LOST CONNECTION] Lost/Broken connection to {addr}.")
        MY_LOGGER.info(f"{datetime.now()} -- [LOST CONNECTION] Lost/Broken connection to {addr}.")
    except Exception as e:
        MY_LOGGER.error("[LOST CONNECTION] Sending packets error: %s", e)
        MY_LOGGER.debug("", exc_info=True)

    
    conn.close()
    print(f"[CLOSED CONNECTION] {addr} successfully closed.")
    MY_LOGGER.info(f"{datetime.now()} -- [CLOSED CONNECTION] {addr} successfully closed.")

def load_model(model_path, env_name):
    '''
    Loads weights of specified DQN RL model

    Params:
        model_path (str) : path to model weights
        env_name (str) : name of game environment

    Returns:
        window_length (int) : number of image game state stacks per input, 4
        input_shape (tuple) : shape of model environment input (105,105)
        ms_pacman_model (keras-rl model) : model with loaded weights
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

def load_controller(controller_path, env):
    '''
    Loads controller assets

    Params:
        controller_path (str) : path to controller assets
    
    Returns:
        action_controls (dict) : {action (int) : control image (np.array)}
    '''
    action_meanings = env.unwrapped.get_action_meanings()
    action_controls = {i:cv2.imread(controller_path+action_meanings[i]+'.png') for i in range(len(action_meanings))}

    return action_controls

def stream_gameplay():
    '''
    Yields frame by frame gameplay for each episode using trained agent.
    '''
    
    MODEL_WEIGHTS_PATH = './models/Dueling_DQN_Round2_weights_final_steps15000.h5f'
    GAME_ENV_NAME = 'ALE/MsPacman-v5'
    CONTROLLER_PATH = '../assets/controller/'
    broadcast_dimensions = (1000,500)

    # Load model and environment
    window_length, input_shape, ms_pacman_model = load_model(MODEL_WEIGHTS_PATH, GAME_ENV_NAME)
    MY_LOGGER.info(f"{datetime.now()} -- Loaded model and environment.")

    # Load controller actions
    action_controls = load_controller(CONTROLLER_PATH, ms_pacman_model.env)
    MY_LOGGER.info(f"{datetime.now()} -- Loaded controller and actions.")

    # Init objects to calculate and maintain fps
    n_frame = 1
    n_frames = []
    start_time = time.time()
    fps_maintain = 20
    last_n_frames = 5

    # Post-processor on observations returned from gameplay
    broadcast_processor = PostProcessor()

    # Start gameplay
    MY_LOGGER.info(f"{datetime.now()} -- Starting Gameplay.")
    for observation, observation_deprocessed, action, done in ms_pacman_model.play_gen():
        
        # Calc most recent last_n_frames fps
        if len(n_frames) < last_n_frames:
            fps = 0
        else:
            fps = round(last_n_frames/sum(n_frames[-last_n_frames:]))

        # Post-processor on observations returned from gameplay
        observation_broadcast = copy.deepcopy(observation_deprocessed)
        observation_broadcast = broadcast_processor.broadcast_ready(broadcast_dimensions, observation_broadcast, n_frame, fps, action, action_controls)
        
        yield observation_broadcast
        
        # Maintain fps of fps_maintain
        processing_end_time = time.time()
        processing_time = processing_end_time - start_time
        sleep_time = (1/fps_maintain) - (processing_time)
        if sleep_time < 0:
            sleep_time = 0

        time.sleep(sleep_time)

        frame_end_time = time.time()
        n_frames.append(frame_end_time-start_time)
        start_time = time.time()
        
        n_frame += 1
        
        if done:
            MY_LOGGER.info(f"{datetime.now()} -- Gameplay completed.")
            break

if __name__ == "__main__":
    start()
