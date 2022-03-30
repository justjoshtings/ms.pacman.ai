"""
app.py

Test Flask App for Ms. Pacman

author: @justjoshtings
created: 3/16/2022
"""
from unittest import result
from flask import Flask, render_template, request, Response, send_file

from web_server import connect_webserver
from stats import make_plot
from stats import load_plot
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__, template_folder = 'build', static_folder = 'build/static')
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

    def intermediate_stream_feed():
        '''
        Start connect_webserver() generator to separate score from frame
        Feed frame into Response() while set score as a global variable to access later on
        '''
        for frame in connect_webserver():
            global score
            score = int(str(frame[-10:]).split('score')[-1][:-1])
            yield frame

    response = Response(intermediate_stream_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # Initialize random scores
    global score
    score = -1

    @response.call_on_close
    def on_close():
        '''
        Does some action after response is returned and before exiting function video_feed().
        Here we pass the score into some other function for continued processing.
        '''
        do_something_with_score(score)
    
    return response

def do_something_with_score(score):
    print('SCORE!!',score)
    pass

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

if __name__ == "__main__":
    print('Running App')
    someport = 8080
    app.run(host = '0.0.0.0', port = someport, debug = True, threaded = True)