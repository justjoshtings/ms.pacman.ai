# web_app

## Webapp for Ms. Pacman Reinforcement Learning Agent AI gameplay streaming.

## Contents
1. **models**: Save model weights here.
2. **templates**: Html templates for Flask testing app.
3. **app.py**: Flask app.
4. **MsPacmanAI.GameModels.py**: Reinforcement Learning Agent object. Imported into app.py.
5. **MsPacmanAI.ImageProcessor.py**: Object to perform pre & post preprocessing of Atari env game states. Imported into app.py, GameModels.py.
6. **model_inference_server.py**: Server side logic to handle model inference from client web_server.py Delivers frame by frame of model's playthrough to the web_server.py through TCP/IP connection.
7. **MsPacmanAI.socket_server_credentials_template.py**: Template to store credentials, port numbers, and IP addresses.
8. **MsPacmanAI.socket_server_credentials.py**: Store credentials, port numbers, and IP addresses. Use socket_server_credentials_template.py as a template. DO NOT expose to web!
9. **web_server.py**: Client side logic to receive frame by frame of model's playthrough from model_inference_server.py through TCP/IP connection. Serves image stream through flask app.py.
10. **model_inference_server_setup.sh**: Execute in model inference server to setup model inference dependencies and environment.
11. **web_server_setup.sh**: Execute in web server to setup web server dependencies and environment.
12. **MsPacmanAI.Logger**: Logger object to handle logging DEBUG and INFO.
13. **public**: Public front end websites
14. **src**: javascript + css front end files
15. **build**: built react project from running 'npm build', if you launch the website like a react project it 
    points here
16. **run_app_py.sh**: To run app.py front end as a background process in the webserver so that the python script doesn't end when SSH disconnects.
17. **run_model_inference_server_py**: To run model_inference_server.py as background process in the model inference server so that the python script doesn't end when SSH disconnects.
18. **mysql_config.txt**: Enter your mysql db password here in order to connect.
19. **test_sql.py**: To test connection to mysql db is working correctly. Should return data from stats_table.

## Setup
#### Model Inference Server
Create new machine (Ubuntu) and clone repo. Ensure machine have open inbound/outbound ports for desired TCP/IP port ranges for transmitting live-stream to web server. 

```
git clone https://github.com/justjoshtings/ms.pacman.ai.git
cd ~/ms.pacman.ai/web_app/
```
Enter the mysql db password in ~/ms.pacman.ai/web_app/mysql_config.txt
```
vim ~/ms.pacman.ai/web_app/mysql_config.txt
[enter password]
:wq [enter]
```
Run setup shell script
```
chmod u+x model_inference_server_setup.sh
./model_inference_server_setup.sh
```

Update socket credentials in ms.pacman.ai/stream_test/flask_test/socket_server_credentials.py

#### Web Server
* Create new machine (Ubuntu) and clone repo. Ensure machine have open inbound/outbound ports for desired TCP/IP port ranges for receiving live-stream from model inference server. Also ensure proper inbound/outbound ports for Flask app and HTTP/HTTPS connections.

```
git clone https://github.com/justjoshtings/ms.pacman.ai.git
cd ~/ms.pacman.ai/web_app/
```
Enter the mysql db password in ~/ms.pacman.ai/web_app/mysql_config.txt
```
vim ~/ms.pacman.ai/web_app/mysql_config.txt
[enter password]
:wq [enter]
```
Run setup shell script
```
chmod u+x web_server_setup.sh
./web_server_setup.sh
```

### To launch as a Flask App

#### 1. React Project  
While inside the 'web_app' folder, run the command
```
npm install .
```  
Then run the command 
```
npm run build
```


#### 2. Model Inference Server
Open a new terminal and run model_inference_server.py

```
python3 model_inference_server.py
```

This should print out your local IP.
Update socket credentials in ms.pacman.ai/stream_test/flask_test/socket_server_credentials.py

Or to run it as a background process to prevent script breaking when SSH disconnects.
```
chmod +x run_model_inference_server_py.sh
./run_model_inference_server_py.sh
```

To check if background process is running and get PID
```
ps ax | grep model_inference_server.py
```

To kill PID where PID is the process ID
```
kill PID
```

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

Or to run it as a background process to prevent script breaking when SSH disconnects.
```
chmod +x run_app_py.sh
./run_app_py.sh
```

To check if background process is running and get PID
```
ps ax | grep app.py
```

To kill PID where PID is the process ID
```
kill PID
```
### To Launch as a React App (Good for debugging front end as it updates automatically)
Follow steps 2 + 3 from above.

#### Start React App  
In a third terminal window launch the React App from 'web_app'
```
npm start
```  
This should open the website in a browser window.
The webserver is listening on a port while the flask app is communicating with it (but not launching a front end).
The React App is then streaming to the browser and communicating with the flask app.

## Simplified Server Communications Architecture
![server_comms](https://github.com/justjoshtings/ms.pacman.ai/blob/main/stream_test_react/flask_test/server_communications.jpg)
