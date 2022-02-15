# loading obstacles
import numpy as np
dimension=2
N=1
obc=np.zeros((N, 10 if dimension == 3 else 7, dimension), dtype=np.float32)
for i in range(0, N):
    obs_dat_file=open('obstacle_control0'+ '.npy',"r")
    obs_dat=obs_dat_file.read()
    obs_dat=obs_dat.split("\n")
    obs_dat=np.array(obs_dat)
    obs_dat=obs_dat[0:14]
    obs_dat=obs_dat.astype(np.float)
    obs = np.array(obs_dat).astype(np.float32).reshape(7, 2)
    for j in range(0, 10 if dimension == 3 else 7):
        for k in range(0, dimension):
            obc[i][j][k] = obs[j][k]
print(obc)
