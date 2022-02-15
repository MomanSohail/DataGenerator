import numpy as np


def load_dataset(dataset_path, dimension, EPB, N=100, NP=1000):
    obs_size = 2800 if dimension == 2 else 6000
    obstacles = np.zeros((N, obs_size), dtype=np.float32)
    for i in range(0, N):
        #temp = np.fromfile(dataset_path+'/obs_cloud/obs_cloud' + str(i) + '.npy')
        #temp=temp[0:6782]

        obs_dat_file=open(dataset_path+'/obs_cloud/obs_cloud' + str(i) + '.npy',"r")
        obs_dat=obs_dat_file.read()
        obs_dat=obs_dat.split("\n")
        obs_dat=np.array(obs_dat)
        obs_dat=obs_dat[0:2800]
        obs_dat=obs_dat.astype(np.float)
        obs = np.array(obs_dat).astype(np.float32).reshape(1400, 2)

        #temp = temp.reshape(len(temp) // dimension, dimension)
        obstacles[i] = obs.flatten()
        EPB.setProperty("value", i / N * 100)


    print(obstacles.shape)
    return obstacles
