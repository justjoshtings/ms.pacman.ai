you will need:
    
public subnet and private subnet for your public and private ec2s respectively

public ec2 and private gpu ec2. you will ssh forward into private ec2
I used 'Deep Learning AMI (Amazon Linux 2) Version 59.0' with family = g4dn.xlarge for the private ec2

nat gateway so private subnet can connect to internet

elastic IP for nat gateway

s3 bucket (with access key and secret key) to be able to store results



helpful resources:

Securely Connect to Linux Instances Running in a Private Amazon VPC - https://aws.amazon.com/blogs/security/securely-connect-to-linux-instances-running-in-a-private-amazon-vpc/

AWS VPC Public and Private Subnets - https://www.youtube.com/watch?v=4T9G9nv0GIk&

Connecting to internet from EC2 Instance in private subnet of AWS VPC - https://www.linkedin.com/pulse/connecting-internet-from-ec2-instance-private-subnet-aws-thandra/

The Way to Deep Learning on AWS - https://towardsdatascience.com/the-way-to-deep-learning-on-aws-851fad7e5725

Running Python scripts on an AWS EC2 Instance | by Praneeth Kandula | Medium - https://towardsdatascience.com/the-way-to-deep-learning-on-aws-851fad7e5725

how to keep a python script running when I close putty - Unix & Linux Stack Exchange - https://unix.stackexchange.com/questions/362115/how-to-keep-a-python-script-running-when-i-close-putty

Tmux Cheat Sheet & Quick Reference - https://tmuxcheatsheet.com/



other stuff:

sudo yum update before you start

want to close the session and still have the code run?: sudo yum install tmux
to create a new session you can come back to: tmux
after you close putty/your terminal, the python code will still be running
to come back to the session you were working on: tmux attach
to list all current sessions: tmux ls
to kill a session: tmux kill-session

use 'source activate tensorflow2_p38' once you get into the gpu instance in order to activate the gpu. It will prompt you. It comes with python built in.

make sure you upgrade pip. if you pip install gym and it tells you to upgrade pip, upgrade pip and then do the command to install gym again

you will have to insert your own access key and secret access key for the bucket at the end.

feel free to edit any parameters (window length, steps, etc.)

feel free to also change directories and edit S3 code at the bottom if you want a cleaner bucket result.



run the following in your ec2 before you start:

pip install gym gym[atari,accept-rom-license]==0.22.0

pip install pygame

pip install keras-rl2

pip install tensorflow

pip install numpy

pip install boto3

pip install pillow

mkdir results



remember to: 
delete nat gateway
stop ec2 instances
release elastic IP