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
pip3 install mysql-connector-python

# To allow cv2 imports
sudo apt install -y libgl1-mesa-glx

# create socket_server_credentials.py from socket_server_credentials_template.py and edit IP/PORTs
cd ~/ms.pacman.ai/web_app/MsPacmanAI/
cp socket_server_credentials_template.py socket_server_credentials.py

echo "Please update socket credentials in ~/ms.pacman.ai/web_app/MsPacmanAI/socket_server_credentials.py"

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

# Setup mysql db
# sudo mysql
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY $mysql_password; FLUSH PRIVILEGES;"
mysql -u root -e "exit"

# sudo mysql -p
mysql -h "localhost" -u root -p$mysql_password -e "show databases"
mysql -h "localhost" -u root -p$mysql_password -e "CREATE DATABASE IF NOT EXISTS mspacmanai;"
mysql -h "localhost" -u root -p$mysql_password -e "USE mspacmanai;"
mysql -h "localhost" -u root -p$mysql_password -e "USE mspacmanai; CREATE TABLE IF NOT EXISTS stats_table (entry_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
, game_score DOUBLE(10,2), time_alive DOUBLE(10,2), mean_fps DOUBLE(10,2), timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"

cd ~/
sudo vim /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart

mysql -h "localhost" -u root -p$mysql_password -e "CREATE USER 'root'@'%' IDENTIFIED BY '$mysql_password';"
mysql -h "localhost" -u root -p$mysql_password -e "GRANT ALL PRIVILEGES ON *.* to root@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;"