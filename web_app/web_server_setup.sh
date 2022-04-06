#!/bin/bash

echo "Executing Ms.Pacman.AI WebServer setup"

echo "Minimum AWS EC2 system requirements t2.micro, 1GB RAM, 30GB SSD"

sudo apt update
sudo apt install -y python3-pip

# clone ms.pacman.ai
cd ~/
git clone https://github.com/justjoshtings/ms.pacman.ai.git

cd /home/ubuntu/ms.pacman.ai/web_app
python3 -m venv mspacman
source mspacman/bin/activate

pip3 install opencv-python
# To allow cv2 imports
sudo apt install -y libgl1-mesa-glx

pip3 install flask
pip3 install flask_cors
pip3 install waitress
pip3 install mysql-connector-python
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn

# create socket_server_credentials.py from socket_server_credentials_template.py and edit IP/PORTs
cd ~/ms.pacman.ai/web_app/MsPacmanAI/
cp socket_server_credentials_template.py socket_server_credentials.py

# commands I ran to set up webserver
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

cd ~/ms.pacman.ai/
# pip install -r requirements.txt
pip3 install gunicorn flask
pip3 install wheel
sudo apt install nginx

sudo ufw allow 8080

sudo apt install -y npm

cd ~/ms.pacman.ai/web_app/
npm install .

#Update node version to latest
curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -
sudo apt-get install -y nodejs

# Update npm version to latest
sudo npm install npm -g

echo "node version should be >= 14.0.0"
node -v

echo "npm version should be >= 5.6"
npm -v

# Run npm build
npm run build

echo "Please update socket credentials in /ms.pacman.ai/web_app/MsPacmanAI/socket_server_credentials.py"

echo "app.run(host='0.0.0.0', port='8080', debug=True,threaded=True)"

# Mysql password handling
FILE=~/ms.pacman.ai/web_app/mysql_config.txt
echo "Store password in $FILE"

if test -f "$FILE"; then
    echo "$FILE exists."
else
    echo "some_temp_password" >> $FILE
fi

mysql_password=$(cat $FILE)
echo "$mysql_password"
deactivate

echo "[Unit]
Description=Gunicorn instance to serve mspacman
After=network.target

[Service]
User=ubuntu
Group=www-data

WorkingDirectory=/home/ubuntu/ms.pacman.ai/web_app
Environment="PATH=/home/ubuntu/ms.pacman.ai/web_app/mspacman/bin"
ExecStart=/home/ubuntu/ms.pacman.ai/web_app/mspacman/bin/gunicorn --bind 0.0.0.0:8080 wsgi:app --timeout 300

[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/mspacman.service

echo "if you haven't used this server before run:"
echo "sudosystemctl start mspacman"
echo "sudosystemctl enable mspacman"
echo "sudosystemctl status mspacman"



