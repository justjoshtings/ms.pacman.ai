# flask_test with react

## Development tests of webserver/model inference server, connection to Flask app, live-streaming, and gameplay rendering with a React front end.

## Contents
1. **models**: Save model weights here.
2. **templates**: Html templates for Flask testing app.
3. **app.py**: Flask app.
4. **GameModels.py**: Reinforcement Learning Agent object. Imported into app.py.
5. **ImageProcessor.py**: Object to perform pre & post preprocessing of Atari env game states. Imported into app.py, GameModels.py.
6. **model_inference_server.py**: Server side logic to handle model inference from client web_server.py Delivers frame by frame of model's playthrough to the web_server.py through TCP/IP connection.
7. **socket_server_credentials_template.py**: Template to store credentials, port numbers, and IP addresses.
8. **socket_server_credentials.py**: Store credentials, port numbers, and IP addresses. Use socket_server_credentials_template.py as a template. DO NOT expose to web!
9. **web_server.py**: Client side logic to receive frame by frame of model's playthrough from model_inference_server.py through TCP/IP connection. Serves image stream through flask app.py.
10. **model_inference_server_setup.sh**: Execute in model inference server to setup model inference dependencies and environment.
11. **web_server_setup.sh**: Execute in web server to setup web server dependencies and environment.
12. **public**: Public front end websites
13. **src**: javascript + css front end files
14. **build**: built react project from running 'npm build', if you launch the website like a react project it 
    points here
## Setup (instructions for local setup)

### To launch as a Flask App

#### 1. React Project  
While inside the 'stream_test_react/flask_test' folder, run the command
```
npm build
```

#### 2. Model Inference Server
Open a new terminal and run model_inference_server.py

```
python3 model_inference_server.py
```

This should print out your local IP (if it crashes, change the host name to "localhost").
Update socket credentials in ms.pacman.ai/stream_test/flask_test/socket_server_credentials.py

#### 3. Web Server
Open a seperate terminal window

* Update app.run() in app.py. Important to note that this is only for development and testing purposes. Do not deploy the Flask app into a production setting with these configurations and technology stack.
```
someport = 8080
app.run(host='0.0.0.0', port=someport, debug=True, threaded=True)
```

* Execute Flask app and web server.
```
python3 app.py
```

### To Launch as a React App (Good for debugging front end as it updates automatically)
Follow steps 2 + 3 from above.

#### Start React App  
In a third terminal window launch the React App from 'stream_test_react/flask_test'
```
npm start
```  
This should open the website in a browser window.
The webserver is listening on a port while the flask app is communicating with it (but not launching a front end).
The React App is then streaming to the browser and communicating with the flask app.

## Simplified Server Communications Architecture
![server_comms](https://github.com/justjoshtings/ms.pacman.
ai/blob/main/stream_test_react/flask_test/server_communications.jpg)
