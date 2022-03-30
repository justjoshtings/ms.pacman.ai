"""
web_server.py

Client side logic to receive frame by frame of model's playthrough from model_inference_server.py through TCP/IP connection.
Serves image stream through flask app.py

author: @justjoshtings
created: 3/16/2022
"""

import socket
import cv2
import numpy as np
import struct
import pickle
from datetime import datetime

from MsPacmanAI.Logger import MyLogger
from MsPacmanAI import socket_server_credentials


def connect_webserver():
    '''
    Connect to webserver and process received message(s)
    '''
    LOG_FILENAME = '../logs/web_server.log'

    # Set up a specific logger with our desired output level
    mylogger = MyLogger(LOG_FILENAME)
    global MY_LOGGER
    MY_LOGGER = mylogger.get_mylogger()

    PORT = socket_server_credentials.PORT
    HOST_IP = socket_server_credentials.HOST_IP
    ADDR = (HOST_IP, PORT)
    payload_size = struct.calcsize("Q") #8 bytes size

    try:
        print(f'Attempting Connection to IP:{HOST_IP}, PORT:{PORT}')
        MY_LOGGER.info(f'{datetime.now()} -- Attempting Connection to IP:{HOST_IP}, PORT:{PORT}')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
    except ConnectionRefusedError:
        HOST_IP = socket_server_credentials.HOST_IP_alt
        ADDR = (HOST_IP, PORT)
        print(f'Failed... Attempting Connection to IP:{HOST_IP}, PORT:{PORT}')
        MY_LOGGER.info(f'{datetime.now()} -- Failed... Attempting Connection to IP:{HOST_IP}, PORT:{PORT}')
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(ADDR)
        except Exception as e:
            MY_LOGGER.error("Connection to server error: %s", e)
            MY_LOGGER.debug("", exc_info=True)
    
    MY_LOGGER.info(f'{datetime.now()} -- Connected to IP:{HOST_IP}, PORT:{PORT}')
    MY_LOGGER.info(f'{datetime.now()} -- Receiving packets...')
    while True:
        try:
            obj,rewards = recv_obj(client_socket, payload_size)
        except TypeError:
            obj = None
        if obj is None:
            break
        for frame in process_object(obj):
            yield frame+str.encode(f"score{rewards}")
    
    client_socket.close()
    MY_LOGGER.info(f'{datetime.now()} -- Connection closed...')

    
def recv_obj(client_socket, payload_size):
    '''
    Run recvall() twice. First time to get message packet size and second time to use packet size to get rest of mesage.

    Params:
        client_socket (socket.socket() object) : client socket connection to webserver 
        payload_size (int) : struct.calcsize("Q")

    Returns:
        python object from converted byte string message
    '''
    data = recvall(client_socket, payload_size)
    if len(data) < payload_size:
        if not data:
            # client closed after last message, assume all is well
            return None
        else:
            MY_LOGGER.info(f'{datetime.now()} -- Truncated message')
            raise IOError("Truncated message")
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    remaining_data = recvall(client_socket, msg_size)
    if len(remaining_data) < msg_size:
        MY_LOGGER.info(f'{datetime.now()} -- Truncated message')
        raise IOError("Truncated message")
    rewards = str(remaining_data[-15:]).split('score')[-1].split('.')[0]
    obj = pickle.loads(data + remaining_data)
    return obj,rewards

def recvall(client_socket, packet_size):
    """
    Keep receiving up to `packet_size` bytes, returning partial result
    if connection closed normally by remote.

    Params:
        client_socket (socket.socket() object) : client socket connection to webserver
        packet_size (int) : packet size of message
    
    Returns:
        byte string of message received from webserver
    """
    data_buffer = []
    # i = 0
    while packet_size:
        # print('Packet Size',packet_size)
        try:
            data = client_socket.recv(packet_size)
        except Exception as e:
            MY_LOGGER.error("Receiving packets error: %s", e)
            MY_LOGGER.debug("", exc_info=True)
        # print('Receiving Packets, Packet Size', len(data))
        if not data:
            break
        packet_size -= len(data)
        data_buffer.append(data)
        # print('Number of Iterations per Recvall Call',i)
        # i+=1
    return b"".join(data_buffer)


def process_object(obj):
    '''
    Perform object processing here
    
    Params:
        obj (python object, nparray): object to be procesed as image
    '''
    # Encode image to JPEG then to bytes
    frame = cv2.imencode('.JPEG', obj, [cv2.IMWRITE_JPEG_QUALITY,100])[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    connect_webserver()
