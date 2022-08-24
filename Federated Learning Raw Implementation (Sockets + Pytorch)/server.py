from glob import glob
import socket
from threading import Thread

import torch

from model_builder import Net
from utils_info import *

""" Global Variables """

HOST = "localhost"
PORT = 9999

PATH = "./models/"
global_model = Net()

clients = dict()
client_models = list()
client_counter = 0

WAIT_TIME = 30


def main():
    global client_counter
    
    """ Creating Listening Socket """

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(10)

    """ Open Connection Sockets """
    
    Thread(target=listening_thread, args=(server,), daemon=True).start()

    Thread(target=aggregation_thread, daemon=True).start()
    
    input("[Press Enter to Exit Server]")
    


def aggregation_thread():
    global client_counter
    global global_model
    while True:
        time.sleep(WAIT_TIME)
        
        if len(glob(PATH + "model_client(*).pth")) >= 3:
            
            """ Get All Models """
            models = load_all_models(PATH)

            """ Get State Dictionaries """
            models_state_dict = list()
            for i in range(len(models)):
                models_state_dict.append(models[i].state_dict())

            global_model_state_dict = global_model.state_dict()
            for key in global_model_state_dict:
                global_model_state_dict[key] = 0
                for m_sd in models_state_dict:
                    global_model_state_dict[key] += m_sd[key]
                global_model_state_dict[key] /= client_counter

            global_model.load_state_dict(global_model_state_dict)
            
            """ Delete All Models """

            delete_all_model_files(PATH)
            print("Aggregation Complete")


""" Read All Model Files in Folder  """
""" args: 
        folder = Folder Containing Model Files """
""" return: List of Pytorch Models """
def load_all_models(folder: str):
    model_filenames = glob(folder + "model_client(*).pth")
    models = list()

    for filename in model_filenames:
        models.append(torch.load(filename))
    
    return models

""" Delete All Model Files in Folder """
""" args: 
        folder = Folder Containing Model Files """
""" return: None """
def delete_all_model_files(folder: str):
    model_filenames = glob(folder + "model_client(*).pth")

    for filename in model_filenames:
        os.remove(filename)
    
    return 


""" Daemon Thread Used to Listen For New Connections """
""" args:
        listener_sock = Listening Socket of Server """
""" return: None """
def listening_thread(listener_sock: socket.socket):
    global client_counter
    while True:
        client_sock, address = listener_sock.accept()
        ip, port = str(address[0]), str(address[1])

        client_counter += 1

        Thread(target=client_thread, args=(client_sock, ip, port)).start()

    listener_sock.close()


""" Client Thread for Each New Client """
""" args:
        client_sock = Socket File Descriptor for New Client
        ip = IP Address of Host
        port = Port of Host being Used """
""" return: None"""
def client_thread(client_sock: socket.socket, ip: str, port: str):
    global client_counter

    """ Getting Client Data """

    client_info = recv_json(sock_fd=client_sock)
    clients[client_sock] = client_info

    """ Sending Model to Client """

    send_model(sock_fd=client_sock, to_send_filename=PATH+"model_global.pth")

    """ Receiving Updated Model from Client """

    recv_model(sock_fd=client_sock, to_save_filename=PATH+f"model_client({client_counter}).pth")

    """ Signal for Client Model Received """



if __name__ == "__main__":
    main()