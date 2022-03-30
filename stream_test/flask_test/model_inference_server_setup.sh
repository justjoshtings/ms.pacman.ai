#!/bin/bash

echo "Executing Ms.Pacman.AI Model Inference Server setup"

echo "Minimum AWS EC2 system requirements t2.micro, 1GB RAM, 30GB SSD"

sudo apt update
sudo apt install -y python3-pip

# clone ms.pacman.ai
cd ~/
git clone https://github.com/justjoshtings/ms.pacman.ai.git

pip3 install tensorflow-cpu
pip3 install opencv-python
pip3 install Pillow
pip3 install matplotlib
pip3 install seaborn

# To allow cv2 imports
sudo apt install -y libgl1-mesa-glx

# create socket_server_credentials.py from socket_server_credentials_template.py and edit IP/PORTs
cd ~/ms.pacman.ai/stream_test/flask_test/
cp socket_server_credentials_template.py socket_server_credentials.py

echo "Please update socket credentials in ms.pacman.ai/stream_test/flask_test/socket_server_credentials.py"

# Install Keras-rl2 without full tensorflow GPU
cd ~/
git clone https://github.com/wau/keras-rl2.git
cd ~/keras-rl2
sed -i 's/tensorflow/tensorflow-cpu/' setup.py
#vim setup.py
#change 'tensorflow' to 'tensorflow-cpu'
pip3 install .

# install gym and atari rom
pip3 install 'gym[atari,accept-rom-license]==0.22.0'

# install mysql
sudo apt install -y mysql-server
sudo systemctl status mysql

echo "Do these steps manually to set up mysqldb"
echo "sudo mysql"
echo "mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password_here';"
echo "mysql> FLUSH PRIVILEGES;"
echo "mysql> exit"
echo "sudo mysql -u root -p:"
echo "mysql> CREATE DATABASE mspacmanai;"
echo "mysql> USE mspacmanai;"
echo "mysql> CREATE TABLE stats_table (entry_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
, game_score );"

sudo mysql

mysql -h "localhost" -u root -pmspacman7 -e "show databases"