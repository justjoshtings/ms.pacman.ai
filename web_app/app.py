"""
app.py

Test Flask App for Ms. Pacman

author: @justjoshtings
created: 3/16/2022
"""
from unittest import result
from flask import Flask, render_template, request, Response, send_file

# import cv2

# from time import sleep
# import time

# import copy

# from GameModels import DQNAgentService
# from ImageProcessor import PostProcessor

from web_server import connect_webserver
from stats import make_plot
from stats import load_plot
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# MODEL_WEIGHTS_PATH = './stream_test/flask_test/models/Dueling_DQN_Round2_weights_final_steps15000.h5f'
# GAME_ENV_NAME = 'ALE/MsPacman-v5'

app = Flask(__name__)
@app.route('/')

def index():
    return render_template("index.html")

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

@app.route('/stats', methods = ['POST', 'GET'])
def show_stats():
    '''
    this function will get updated later, for now it's displaying an image in the source folder
    so change the directory as needed. Janky but won't be here for long
    '''
    print('in the stats function')
    #fig = make_plot()
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype = 'image/png')
    im = '/Users/sahara/Documents/GW/CloudComputing/ms.pacman.ai/tempfig.png'
    return send_file(im, mimetype='image/png')

if __name__ == "__main__":
    print('Running App')
    someport = 8080
    app.run(host = '0.0.0.0', port = someport, debug = True, threaded = True)