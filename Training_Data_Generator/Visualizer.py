import sys

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import struct
import numpy as np
import argparse

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


def main(args):
    # visualize point cloud (obstacles)
    #obs = []
    #temp = np.fromfile(args.obs_file)
    #obs.append(temp)
    #obs = np.array(obs).astype(np.float32).reshape(-1, 2)
    
    obs_dat_file=open(args.obs_file,"r")
    obs_dat=obs_dat_file.read()
    obs_dat=obs_dat.split("\n")
    obs_dat=np.array(obs_dat)
    obs_dat=obs_dat[0:2800]
    obs_dat=obs_dat.astype(np.float)
    obs = np.array(obs_dat).astype(np.float32).reshape(1400, 2)
    
    
    plt.scatter(obs[:, 0], obs[:, 1], c='blue')

    # visualize path
    #path = np.loadtxt(args.path_file)
    #print(path)
    #path = path.reshape(-1, 2)
    #path_x = []
    #path_y = []
    #for i in range(len(path)):
        #path_x.append(path[i][0])
        #path_y.append(path[i][1])


    path_file=open(args.path_file,"r")
    path=path_file.read()
    path=path.split("\n")
    path=np.array(path)
    path_size=len(path)
    path=path[0:path_size-1]
    path=path.astype(np.float)
    path = path.reshape(-1, 2)
    print(path)
    path_x = []
    path_y = []
    for i in range(len(path)):
        path_x.append(path[i][0])
        path_y.append(path[i][1])


    plt.plot(path_x, path_y, c='r', marker='o')

    plt.show()


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

    def open_obstacle(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select your Environment",
            "",
            "All Files (*);;Image Files (*.dat)",
            options=options)
        return fileName

    def open_path(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select your Path",
            "",
            "All Files (*);;Image Files (*.txt)",
            options=options)
        return fileName


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # for training
    app = QApplication([])
    window = Main()
    window.show()
    parser.add_argument('--obs_file', type=str, default=window.open_obstacle(),
                        help='obstacle point cloud file')
    parser.add_argument('--path_file', type=str, default=window.open_path(), help='path file')

    args = parser.parse_args()
    print(args)
    main(args)
    sys.exit(app.exec_())