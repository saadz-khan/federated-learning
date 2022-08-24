from model_builder import Net
import torch
import os

""" Global Variables """

PATH = "./models/"
SEPARATOR = "%SZ%"

def main():
    net = Net()
    torch.save(net, PATH + "model_global.pth")
    
    # file_stats = os.stat(PATH + "model_global.pth")
    # size = file_stats.st_size

    # os.rename(PATH + "model_global.pth", PATH + "model_global" + SEPARATOR + f"{size}" + ".pth")

if __name__ == "__main__":
    main()