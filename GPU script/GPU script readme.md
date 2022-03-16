you will need:
    
public subnet and private subnet for your public and private ec2s respectively

public ec2 and private gpu ec2. you will ssh forward into private ec2
I used 'Deep Learning AMI (Amazon Linux 2) Version 59.0' with family = g4dn.xlarge for the private ec2

nat gateway so private subnet can connect to internet

elastic IP for nat gateway



helpful resources:

Securely Connect to Linux Instances Running in a Private Amazon VPC - https://aws.amazon.com/blogs/security/securely-connect-to-linux-instances-running-in-a-private-amazon-vpc/

AWS VPC Public and Private Subnets - https://www.youtube.com/watch?v=4T9G9nv0GIk&

Connecting to internet from EC2 Instance in private subnet of AWS VPC - https://www.linkedin.com/pulse/connecting-internet-from-ec2-instance-private-subnet-aws-thandra/

The Way to Deep Learning on AWS - https://towardsdatascience.com/the-way-to-deep-learning-on-aws-851fad7e5725

Running Python scripts on an AWS EC2 Instance | by Praneeth Kandula | Medium - https://towardsdatascience.com/the-way-to-deep-learning-on-aws-851fad7e5725



other stuff:

use 'source activate tensorflow2_p38' once you get into the gpu instance in order to activate the gpu. It will prompt you. It comes with python built in.

make sure you upgrade pip. if you pip install gym and it tells you to upgrade pip, upgrade pip and then do the command to install gym again

you will have to insert your own access key and secret access key for the bucket at the end.

feel free to edit any parameters (window length, steps, etc.)

feel free to also change directories and edit S3 code at the bottom if you want a cleaner bucket result.



run the following in your ec2 before you start:

pip install gym gym[atari,accept-rom-license]==0.22.0

pip install ale_py (i forgot to check if you can skip this, think you can)

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