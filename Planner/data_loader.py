
import os

import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, dimension):
        size = 2800 if dimension == 2 else 6000
        super(Encoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(size, 512), nn.PReLU(), nn.Linear(512, 256), nn.PReLU(),
                                     nn.Linear(256, 128), nn.PReLU(), nn.Linear(128, 28))

    def forward(self, x):
        x = self.encoder(x)
        return x

# N=number of environments; NP=Number of Paths; s=starting environment no.; sp=starting_path_no
# Unseen_environments==> N=10, NP=2000,s=100, sp=0
# seen_environments==> N=100, NP=200,s=0, sp=4000


def load_test_dataset(dataset_path, dimension, N=10, NP=100, s=0, sp=0):
    obc = np.zeros((N, 10 if dimension == 3 else 7, dimension), dtype=np.float32)
    
    #temp = np.fromfile(dataset_path + '/obs.dat')
    #obs = temp.reshape(len(temp) // dimension, dimension)

    #temp = np.fromfile(dataset_path + '/obs_perm2.dat', np.int32)
    #if dimension == 3:
        #perm = temp.reshape(184756, 10)  # change it
    #elif dimension == 2:
        #perm = temp.reshape(77520, 7)

    
    

    # loading obstacles
    for i in range(0, N):
        obs_dat_file=open(dataset_path+'/obstacle_controls/obstacle_control' + str(i) + '.npy',"r")
        obs_dat=obs_dat_file.read()
        obs_dat=obs_dat.split("\n")
        obs_dat=np.array(obs_dat)
        obs_dat=obs_dat[0:14]
        obs_dat=obs_dat.astype(np.float)
        obs = np.array(obs_dat).astype(np.float32).reshape(7, 2)
        for j in range(0, 10 if dimension == 3 else 7):
            for k in range(0, dimension):
                obc[i][j][k] = obs[j][k]

    Q = Encoder(dimension)
    if dimension == 2:
        path = 'Models/encoders/2D/cae_encoder.pkl'
    else:
        path = 'Models/encoders/3D/cae_encoder.pkl'
    Q.load_state_dict(torch.load(path))
    if torch.cuda.is_available():
        Q.cuda()
    # change it
    obs_rep = np.zeros((N, 28), dtype=np.float32)
    k = 0
    for i in range(s, s + N):
        #temp = np.fromfile(dataset_path + '/obs_cloud/obs_cloud' + str(i) + '.npy')
        obs_dat_file=open(dataset_path+'/obs_cloud/obs_cloud' + str(i) + '.npy',"r")
        obs_dat=obs_dat_file.read()
        obs_dat=obs_dat.split("\n")
        obs_dat=np.array(obs_dat)
        obs_dat=obs_dat[0:2800]
        obs_dat=obs_dat.astype(np.float)
        obs = np.array(obs_dat).astype(np.float32).reshape(1400, 2)
        #temp = temp.reshape(len(temp) // dimension, dimension)
        # change it
        obstacles = np.zeros((1, 6000 if dimension == 3 else 2800), dtype=np.float32)
        obstacles[0] = obs.flatten()
        inp = torch.from_numpy(obstacles)
        inp = Variable(inp).cuda()
        output = Q(inp)
        output = output.data.cpu()
        obs_rep[k] = output.numpy()
        k = k + 1
    ## calculating length of the longest trajectory
    max_length = 0
    path_lengths = np.zeros((N, NP), dtype=np.int8)
    for i in range(0, N):
        for j in range(0, NP):
                
            fname = dataset_path + '/e' + str(i + s) + '/path' + str(j + sp) + '.txt'
            if os.path.isfile(fname):
                path_file=open(fname,"r")
                path=path_file.read()
                path=path.split("\n")
                path=np.array(path)
                path_size=len(path)
                path=path[0:path_size-1]
                path=path.astype(np.float)
                path = path.reshape(-1, 2)
                #path = np.fromfile(fname)
                #path = path.reshape(len(path) // dimension, dimension)
                path_lengths[i][j] = len(path)
                if len(path) > max_length:
                    max_length = len(path)

    paths = np.zeros((N, NP, max_length, dimension), dtype=np.float32)  ## padded paths

    for i in range(0, N):
        for j in range(0, NP):
            fname = dataset_path + '/e' + str(i + s) + '/path' + str(j + sp) + '.txt'
            # print(" : "+fname)
            if os.path.isfile(fname):
                path_file=open(fname,"r")
                path=path_file.read()
                path=path.split("\n")
                path=np.array(path)
                path_size=len(path)
                path=path[0:path_size-1]
                path=path.astype(np.float)
                path = path.reshape(-1, 2)
                #path = np.fromfile(fname)
                #path = path.reshape(len(path) // dimension, dimension)
                for k in range(0, len(path)):
                    paths[i][j][k] = path[k]

    return obc, obs_rep, paths, path_lengths
