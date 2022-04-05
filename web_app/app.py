"""
app.py

Flask app for Ms. Pacman AI

author: @justjoshtings
created: 3/16/2022
"""
from unittest import result
from flask import Flask, render_template, request, Response, send_file
from flask_cors import CORS

from web_server import connect_webserver
from stats import make_plot
from stats import load_plot
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import mysql.connector
import numpy as np


app = Flask(__name__, template_folder = 'build', static_folder = 'build/static')
CORS(app)
global FLAG
FLAG = False
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
    from time import sleep
    global result
    params = result
    global FLAG
    FLAG = False

    global score

    def intermediate_stream_feed():
        '''
        Start connect_webserver() generator to separate score from frame
        Feed frame into Response() while set score as a global variable to access later on
        '''
        global score
        for frame in connect_webserver():
            score = int(str(frame[-10:]).split('score')[-1][:-1])
            yield frame


    response = Response(intermediate_stream_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @response.call_on_close
    def on_close():
        '''
        Does some action after response is returned and before exiting function video_feed().
        Here we pass the score into some other function for continued processing.
        '''
        global FLAG
        FLAG = True

    return response

@app.route('/scorestream')
def do_something_with_score():
    def get_score():
        if FLAG:
            yield f'data: {score} \n\n'
        else:
            pass

    return Response(get_score(), mimetype='text/event-stream')

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
    im = 'tempfig.png'
    return send_file(im, mimetype='image/png')

@app.route('/avg', methods = ['GET'])
def get_avg():

    with open('mysql_app_config.txt', 'r') as f:
        host = str(f.read()).strip()

    with open('mysql_config.txt', 'r') as f:
        password = str(f.read()).strip()

    mydb = mysql.connector.connect(
        #host = "ip-42-0-136-127",
        host = host,
        user = "root",
        password = password,
        database = "mspacmanai"
    )
    cursor = mydb.cursor()
    q = 'SELECT * from stats_table;'
    cursor.execute(q)
    res = np.array(cursor.fetchall())
    avg_score = np.mean(res[:,1])
    avg_time = np.mean(res[:,2])
    last_score = res[-1, 1]
    return {'avg_score': avg_score, 'avg_time': avg_time, 'last_score':last_score}


if __name__ == "__main__":
    print('Running App')
    from waitress import serve
    someport = 8080
    serve(app, host="0.0.0.0", port=someport)
    # app.run(host = '0.0.0.0', port = someport, debug = True, threaded = True)
