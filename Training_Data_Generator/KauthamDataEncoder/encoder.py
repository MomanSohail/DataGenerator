#Importing The Libraries.
import random
import numpy as np
import os
from os import path as pa


#This Function will Encode the obstacles of the environment into point cloud representation.
#The Point Clouds will be saved in obs_point_cloudFileX.
#This code will generate point clouds using 2800 points for 2D 7 obstacles case per file and store in file with new line.
#Value1X
#value2X
#Then we will reshape the 2800 points to an array of 1400*2 (2D-array) in case of 2D.
#We will Create 200 Points Per Axis i.e X-axis.

def pointCloudEncoder(obs_dat_file,obstacle_controls,no_of_obstacles,size_of_obstacles,dimension):
    no_of_points=0
    total_no_of_points=no_of_obstacles*200
    obs_cloud=np.zeros((total_no_of_points,dimension))

    #For Loop For Number of Obstacles.
    for i in range (0,no_of_obstacles):
        #For Loop for Number Of Points Per Obstacle.
        for j in range(no_of_points,200+no_of_points):
            #For Loop For Dimension/Axis.
            for k in range(0,dimension):

                obs_cloud[j][k]=random.random()*size_of_obstacles-size_of_obstacles/2.0+obstacle_controls[i][k]
                
        if(no_of_points<total_no_of_points):
            no_of_points=no_of_points+200
        else:
            break
                
    flattened_obs_cloud=obs_cloud.flatten()
    for i in flattened_obs_cloud:
        obs_dat_file.write(str(i)+"\n")
            


        