#!/bin/bash
nohup python3 model_inference_server.py &

echo "model_inference_server.py running in background"
echo "ps ax | grep model_inference_server.py"
ps ax | grep model_inference_server.py

echo "use kill PID to kill process"
