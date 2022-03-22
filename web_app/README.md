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

## Setup
#### Model Inference Server
Create new machine (Ubuntu) and clone repo. Ensure machine have open inbound/outbound ports for desired TCP/IP port ranges for transmitting live-stream to web server.

```
git clone https://github.com/justjoshtings/ms.pacman.ai.git
cd ./ms.pacman.ai/web_app/
chmod u+x model_inference_server_setup.sh
./model_inference_server_setup.sh
```

Update socket credentials in ms.pacman.ai/web_app/socket_server_credentials.py

```
python3 model_inference_server.py
```

Consider using a (public-bastion | private subnet | NAT gateway) servers setup for better privacy and security. Sample setup example:

1. Create private EC2 in private subnet.
2. Create public EC2 to act as bastion to ssh into private EC2.
3. Create elastic IP.
4. Create NatGateway and allocated elastic IP.
5. [Set up route tables of private subnet.](https://docs.axway.com/bundle/SecureTransport_54_on_AWS_InstallationGuide_allOS_en_HTML5/page/Content/AWS/securitygroups/st_nat_gateway_subnet_routing.htm)
6. SSH Agent forward into bastion EC2.
```
ssh -A user@<bastion-IP-address>
```
7. SSH from bastion EC2 into private EC2.
```
ssh user@<instance-IP-address>
```
8. Test internet connection from private EC2.
```
ping google.com
```
9. Apply setup steps from above.

#### Web Server
* Create new machine (Ubuntu) and clone repo. Ensure machine have open inbound/outbound ports for desired TCP/IP port ranges for receiving live-stream from model inference server. Also ensure proper inbound/outbound ports for Flask app and HTTP/HTTPS connections.

```
git clone https://github.com/justjoshtings/ms.pacman.ai.git
cd ./ms.pacman.ai/web_app/
chmod u+x web_server_setup.sh
./web_server_setup.sh
```

* Update socket credentials in ms.pacman.ai/web_app/socket_server_credentials.py

* Update app.run() in app.py. Important to note that this is only for development and testing purposes. Do not deploy the Flask app into a production setting with these configurations and technology stack.
```
someport = 8080
app.run(host='0.0.0.0', port=someport, debug=True, threaded=True)
```

* Execute Flask app and web server.
```
python3 app.py
```
## Simplified Server Communications Architecture
![server_comms](https://github.com/justjoshtings/ms.pacman.ai/blob/main/web_app/server_communications.jpg)
