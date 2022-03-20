"""
app.py

Test Flask App for Ms. Pacman

author: @justjoshtings
created: 3/16/2022
"""
from unittest import result
from flask import Flask, render_template, request, Response

# import cv2

# from time import sleep
# import time

# import copy

# from GameModels import DQNAgentService
# from ImageProcessor import PostProcessor

from web_server import connect_webserver

# MODEL_WEIGHTS_PATH = './stream_test/flask_test/models/Dueling_DQN_Round2_weights_final_steps15000.h5f'
# GAME_ENV_NAME = 'ALE/MsPacman-v5'

app = Flask(__name__)
@app.route('/')

def index():
    return render_template("index.html")

# def load_model(model_path, env_name):
#     # Model parameters
#     window_length = 4
#     input_shape = (105, 105)
    
#     ms_pacman_model = DQNAgentService(model_height=input_shape[0], model_width=input_shape[1], env_name=env_name, window_length=window_length, model_name='Final_Model', model_channels=0)
#     ms_pacman_model.build_model()
#     ms_pacman_model.build_agent(policy_value_max=1., policy_value_min=.1, policy_value_test=.1, policy_nb_steps=8000, 
#                         enable_double_dqn=False, enable_dueling_network=True, dueling_type='avg', nb_steps_warmup=2500)
#     ms_pacman_model.load_weights(model_path)

#     return window_length, input_shape, ms_pacman_model

# def stream_gameplay(params):
#     print('Parameters:',params)

#     # Load model and environment
#     window_length, input_shape, ms_pacman_model = load_model(MODEL_WEIGHTS_PATH, GAME_ENV_NAME)

#     # Init objects to calculate and maintain fps
#     n_frame = 1
#     n_frames = []
#     start_time = time.time()
#     fps_maintain = 20
#     last_n_frames = 5

#     # Post-processor on observations returned from gameplay
#     broadcast_processor = PostProcessor()

#     # Start gameplay
#     for observation, observation_deprocessed, action, done in ms_pacman_model.play_gen():
        
#         # Calc most recent last_n_frames fps
#         if len(n_frames) < last_n_frames:
#             fps = 0
#         else:
#             fps = round(last_n_frames/sum(n_frames[-last_n_frames:]))

#         # Post-processor on observations returned from gameplay
        # observation_broadcast = copy.deepcopy(observation_deprocessed)
#         observation_broadcast = broadcast_processor.broadcast_ready(observation_broadcast, n_frame, fps)
        
#         # Encode image to JPEG then to bytes
#         frame = cv2.imencode('.JPEG', observation_broadcast, [cv2.IMWRITE_JPEG_QUALITY,100])[1].tobytes()
        
#         # Maintain fps of fps_maintain
#         processing_end_time = time.time()
#         processing_time = processing_end_time - start_time
#         sleep_time = (1/fps_maintain) - (processing_time)
#         if sleep_time < 0:
#             sleep_time = 0

#         time.sleep(sleep_time)

#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
#         frame_end_time = time.time()
#         n_frames.append(frame_end_time-start_time)
#         start_time = time.time()
        
#         n_frame += 1
        
#         if done:
#             break

@app.route('/res', methods = ['POST', 'GET'])
def res():
    global result
    if request.method == 'POST':
        result = request.form.to_dict()
        return render_template('results.html')

@app.route('/results')
def video_feed():
    global result
    params = result
    # return Response(stream_gameplay(params), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(connect_webserver(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True,threaded=True)