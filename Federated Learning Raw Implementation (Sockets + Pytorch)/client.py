import socket
from threading import Thread

import torch

from utils_info import *

""" Global Variables """

HOST = "localhost"
PORT = 9999

PATH = "./models/"
model = None

def main():

    """ Creating & Connecting a Socket """
    
    sock_fd = socket.socket()
    sock_fd.connect((HOST, PORT))

    """ Sending Info """

    obj = {"hello":1, "am":3, "i":2, "irtaza":4}
    send_json(sock_fd=sock_fd, obj=obj)

    """ Receiving & Saving Model """

    recv_model(sock_fd=sock_fd, to_save_filename=PATH+"model_recv.pth")

    """ Sending Model to Server """

    send_model(sock_fd=sock_fd, to_send_filename=PATH+"model_recv.pth")
    # print("Send Successful!")

    sock_fd.close()


if __name__ == "__main__":
    main()