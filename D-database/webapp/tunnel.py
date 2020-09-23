import json
from .model import Image_Base
import socket,base64
from json import JSONDecoder
from PIL import Image
import sys
import pickle


def server():
    listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("192.168.43.237",12345))
    listener.listen(0)
    connections=[]
    while len(connections)<1:
        conn ,addr = listener.accept()
        connections.append((conn))

    return (conn,addr)

def reliable_send(ip,data):
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.connect((ip,12345))
    data=pickle.dumps(data)
    HEADERSIZE = 10
    data = bytes(f'{len(data):<{HEADERSIZE}}','utf-8') + data
    connection.send(data)

def reliable_recv(connection):
    HEADERSIZE=10
    full_data=b''
    meta_data = True
    full_data_recvd = True
    while full_data_recvd:
        data = connection.recv(1024)
        if meta_data:
            print(f'length of the message:{data[:HEADERSIZE]}')
            data_len=int(data[:HEADERSIZE])
            meta_data=False
        full_data+=data

        if len(full_data)-HEADERSIZE >= data_len:
            print("Full data received...!")
            data = full_data[HEADERSIZE:]
            data = pickle.loads(data)
            full_data_recvd = False
            print(data)
    if data['command']=='send':
        image=Image_Base.query.filter_by(image_name=data['name']).first()
        dict={'image':image.image,'width':image.width,'height':image.height,'color':image.color,'command':'dasasas','image_name':image.image_name}
        print(data['ip'])
        reliable_send(data['ip'],dict)
        return None
    return data
