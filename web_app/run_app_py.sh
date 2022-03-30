#!/bin/bash
nohup python3 app.py &

echo "app.py running in background"
echo "ps ax | grep app.py"
ps ax | grep app.py

echo "use 'kill PID' to kill process"
