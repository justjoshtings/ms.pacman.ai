#!/bin/bash

echo "Executing Ms.Pacman.AI WebServer setup"

echo "Minimum AWS EC2 system requirements t2.micro, 1GB RAM, 30GB SSD"

sudo apt update
sudo apt install -y python3-pip

# clone ms.pacman.ai
cd ~/
git clone https://github.com/justjoshtings/ms.pacman.ai.git

pip3 install opencv-python
# To allow cv2 imports
sudo apt install -y libgl1-mesa-glx

pip3 install flask

# create socket_server_credentials.py from socket_server_credentials_template.py and edit IP/PORTs
cd ~/ms.pacman.ai/web_app/MsPacmanAI/
cp socket_server_credentials_template.py socket_server_credentials.py

# commands I ran to set up webserver
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

cd ~/ms.pacman.ai/
pip install -r requirements.txt
pip install gunicorn flask
pip install wheel

sudo ufw allow 8080

sudo apt install npm

cd ~/ms.pacman.ai/web_app/
npm install .
npm run build



echo "Please update socket credentials in /ms.pacman.ai/web_app/MsPacmanAI/socket_server_credentials.py"

echo "app.run(host='0.0.0.0', port='8080', debug=True,threaded=True)"