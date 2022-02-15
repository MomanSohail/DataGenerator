#Importing Libraries.
import random
import numpy as np
import os


#This Function will Read Obs_Dat and Perm File.
def readPathObstacleFile(no_of_obstacles,current_dirr):

    #Loading Obstacle.dat File
    #obs_dat=np.fromfile("obs.dat")
    #obs_dat=obs_dat[0:40]
    #obs_dat=np.reshape(obs_dat,(20,2))
    obs_filename=os.path.join(current_dirr+"/Configuration/","obs.npy")
    obs_dat_file=open(obs_filename,"r")
    obs_dat=obs_dat_file.read()
    obs_dat=obs_dat.split("\n")
    obs_dat=np.array(obs_dat)
    obs_dat=obs_dat[0:40]
    obs_dat=obs_dat.astype(np.float)
    obs_dat=np.reshape(obs_dat,(20,2))

    #Loading Obstacle.PermFile
    perm_filename=os.path.join(current_dirr+"/Configuration/","obs_perm2.dat")
    obs_perm= np.fromfile(perm_filename, np.int32)
    size=1000*no_of_obstacles
    obs_perm=obs_perm[0:size]
    obs_perm=np.reshape(obs_perm,(1000,no_of_obstacles))
    return obs_dat,obs_perm


#This function will generate obstacle control for kautham.
def createObstacleControls(no_of_obstacles,obs_dat,obs_perm,dimension):

    #Function To normalize Obstacle Controls Loaded from Obs.dat and perm
    def normalizeObs(value,min_value,max_value):

        return (value-min_value)/(max_value-min_value)

    #Min and Max Value Used to Normalize the Obstacle Control
    min=-30
    max=30

    unormalized_obstacle_control=np.zeros((no_of_obstacles,dimension))
    obstacle_control=np.zeros((no_of_obstacles,dimension))
    for l in range(0,no_of_obstacles):
        for m in range(0,dimension):

            unormalized_obstacle_control[l][m]=obs_dat[obs_perm[random.randint(1,800)][l]][m]
            obstacle_control[l][m]=normalizeObs(unormalized_obstacle_control[l][m],min,max)

    #Normalized_obstacle_control=Normalized_obstacle_control.flatten()
    obstacle_control=obstacle_control.flatten()

    return unormalized_obstacle_control,obstacle_control


#This Function will use random function to create the obstacle controls.
#This Function will be used in Random Scene Generation.
def randomObstacleControls(no_of_obstacles,dimension):

     def normalizeObs(value,min_value,max_value):

         return (value-min_value)/(max_value-min_value)

     min=-30
     max=30

     obstacle_control=np.zeros((no_of_obstacles,dimension))
     unormalized_obstacle_controls=np.zeros((no_of_obstacles,dimension))

     for l in range(0,no_of_obstacles):
         for m in range(0,dimension):

             unormalized_obstacle_controls[l][m]=random.randint(-30,30)
             #obstacle_control[l][m]=normalizeObs(unormalized_obstacle_controls[l][m],min,max)
             obstacle_control[l][m]=random.random()
             
     return unormalized_obstacle_controls,obstacle_control


#Code to create obs_dat File
#This Code will Store the values by a new line
#Value1
#Value2

#obs_dat=np.random.uniform(-20,20,40)
##print(obs_dat)
#obs_dat_file=open("obs.npy","w")
#for i in obs_dat:
    #obs_dat_file.write(str(i)+"\n")
#obs_dat_file.close()
# #obs_dat_file=open("obs.npy","r")
#obs_dat1=obs_dat_file.read()
#obs_dat1=obs_dat1.split("\n")
#obs_dat1=np.array(obs_dat1)
#obs_dat1=obs_dat1[0:40]
#obs_dat1=obs_dat1.astype(np.float)
#obs_dat1=np.reshape(obs_dat1,(20,2))
#print(type(obs_dat1[0][0]))
