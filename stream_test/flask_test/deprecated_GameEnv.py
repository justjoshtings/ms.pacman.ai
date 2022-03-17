"""
GameEnv.py
Atari Gym Game Environment Object.
Imported into app.py
"""

import gym
import ale_py

class ENV:
    def __init__(self, env_name):
        self.env_name = env_name
        self.env = gym.make(self.env_name)
        self.height, self.width, self.channels = self.env.observation_space.shape
        self.actions = self.env.action_space.n


if __name__ == "__main__":
    print('Executing', __name__)
else:
    print('Importing', __name__)


def stream(params):
    print('Parameters:',params)

    window_length, input_shape, ms_pacman_model = load_model(MODEL_WEIGHTS_PATH, GAME_ENV_NAME)

    
    

    observation = ms_pacman_env.env.reset()
    done = False

    n_frame = 1
    n_frames = []
    start_time = time.time()
    fps_maintain = 20

    while not done:
        observation_broadcast = copy.copy(observation)

        observation_broadcast = cv2.resize(observation_broadcast, dsize=(700,600), interpolation=cv2.INTER_AREA)
        observation_broadcast = cv2.cvtColor(observation_broadcast, cv2.COLOR_RGB2BGR)

        last_n_frames = 5
        if len(n_frames) < last_n_frames:
            fps = 0
        else:
            fps = round(last_n_frames/sum(n_frames[-last_n_frames:]))

        observation_broadcast = cv2.putText(observation_broadcast,
                                    text='Frame {}, {}FPS'.format(n_frame, fps), 
                                    org=(50,560), 
                                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                    fontScale=0.4,
                                    color=(255,255,255), #BGR
                                    thickness=1)

        frame = cv2.imencode('.JPEG', observation_broadcast, [cv2.IMWRITE_JPEG_QUALITY,100])[1].tobytes()
        # frame = cv2.imencode('.JPEG', observation, [cv2.IMWRITE_JPEG_QUALITY,100])[1].tobytes()
        
        # Maintain fps of fps_maintain
        processing_end_time = time.time()
        processing_time = processing_end_time - start_time
        sleep_time = (1/fps_maintain) - (processing_time)
        if sleep_time < 0:
            sleep_time = 0

        time.sleep(sleep_time)

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        frame_end_time = time.time()
        n_frames.append(frame_end_time-start_time)
        start_time = time.time()
        
        observation = ms_pacman_model.dqn.process_observation(observation)

        # Random action
        # action = randrange(1,8)

        # Model decided action
        action = ms_pacman_model.dqn.forward(observation)

        observation, r, done, info = ms_pacman_env.env.step(action)
        n_frame += 1