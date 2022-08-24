import os
import tqdm
import time

import socket
import json

""" Global Variables """

BUFFER_SIZE = 1024
SEPARATOR = "%SZ%"

""" Sending JSON """
""" args:   
        sock_fd = Socket Used to Send,
        obj = Dictionary Containing Information """
""" return: None """
def send_json(sock_fd: socket.socket, obj: dict):

    data = json.dumps(obj)
    sock_fd.send(bytes(data, encoding="utf-8"))

    return


""" Receiving JSON """
""" args: 
        sock_fd = Socket Used to Recv """
""" return: obj = Dictionary Containing Information """
def recv_json(sock_fd: socket.socket):

    obj = sock_fd.recv(BUFFER_SIZE)
    obj = json.loads(obj.decode("utf-8"))

    return obj


""" Sending Model File """
""" args:
        sock_fd = Socket Used to Send,
        to_send_filename = Name of Model '.pt' or '.pth' File to Send"""
""" return: None """
def send_model(sock_fd: socket.socket, to_send_filename: str):
    # Get File Info
    filesize = os.path.getsize(to_send_filename)
    # Send File Info
    sock_fd.send(f"{to_send_filename}{SEPARATOR}{filesize}".encode("utf-8"))
  
    # Progress Bar Sending
    progress = tqdm.tqdm(range(filesize), f"Sending {to_send_filename}", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(to_send_filename, 'rb') as fr_model:
        while True:
            data = fr_model.read(BUFFER_SIZE)
            if not data:
                break
            sock_fd.sendall(data)
            progress.update(len(data))
        fr_model.close()

    return


""" Receving Model File """
""" args:
        sock_fd = Socket Used to Send,
        to_save_filename = Name of Model '.pt' or '.pth' File to Save"""
""" return: None """
def recv_model(sock_fd: socket.socket, to_save_filename: str):
    # Recv File Info
    recv = sock_fd.recv(BUFFER_SIZE).decode("utf-8")
    # Parse File Info
    filename, filesize = recv.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # Progress Bar Receiving
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=BUFFER_SIZE)
    with open(to_save_filename, 'wb') as fw_model:
        while True:
            data = sock_fd.recv(BUFFER_SIZE)
            if not data:    
                break
            fw_model.write(data)
            progress.update(len(data))
            if len(data) < BUFFER_SIZE:
                break
        fw_model.close()

    return
