#This File is imported in kautham Client File and contains all the functions.
#main Function,write Path etc.

#!/usr/bin/env python3
import rospy
import rospkg
import sys
import os
from os import path as pa
import random

from matplotlib import pyplot as plt
import Functions
import numpy as np

from std_msgs.msg import String, Time
from geometry_msgs.msg import Pose
rospack =rospkg.RosPack()
import xml.etree.ElementTree as ET
import random
from collections import defaultdict
#Import python module with functions necessary for interfacing with kautham
import kautham_py.kautham_python_interface as kautham


# Global variables
directory=''
Robot_move_control= ''
Robot_pos=[]
taskfile=''
graspedobject= False



#This Function is Used to write Conf tag in .xml file
#It is being called in writeTaskfile Function.
def writePath(taskfile,tex,py_taskfile,should_save_txtfile,r2_r3):

    taskfile.write("\t\t<Conf> %s </Conf>\n" % tex)

    #Calling Function to generate Data Set.txt file.
    if should_save_txtfile:
        writePathMPNETFormate(tex,py_taskfile,r2_r3)

    return True




#This Function will Write a Seperate Data Set file as npy or txt.
#It is being called in writePath Function.
def writePathMPNETFormate(tex_python,py_taskfile,r2_r3):
     #Splitting the tex string into a list.
     new_tex=tex_python.split(" ")

     if r2_r3=="r2":
         #Writing only x and y for 2D.
        py_taskfile.write(f"{new_tex[0]}\n{new_tex[1]}\n")
     elif r2_r3=="r3":
         #Writting x,y and z for 3D.
        py_taskfile.write(f"{new_tex[0]}\n{new_tex[1]}\n{new_tex[2]}\n")

     return True



#This Function will write the taskfile in .xml
#3rd parameter is for .txt Data Set Should be saved or not.
#7th is for Folder Name in which xml should be saved.
def writeTaskfile(path, name, should_save_txtfile,r2_r3,file_name_counter,format_file,folder_number):

    global taskfile
    if path:

       #Naming the dataset file.
        curr_dirr=os.getcwd()
        if r2_r3=="r2" and should_save_txtfile==True:
            file_name='path' +str(file_name_counter-1)+format_file
            pytaskfile = os.path.join(curr_dirr+"/DataSet/e"+str(folder_number-1),file_name)

        elif r2_r3=="r3" and should_save_txtfile==True:
            file_name='path' +str(file_name_counter-1)+format_file
            pytaskfile = os.path.join(curr_dirr+"/DataSet/e"+str(folder_number-1),file_name)

        if should_save_txtfile:
            py_taskfile = open(pytaskfile, "w+")
        else:
            py_taskfile='.txt'

        Name_2="2D_"
        if r2_r3=="r3":
            Name_2="3D_"

        tfile ='z_taskfiles/task_file'+name[0]+'/taskfile_' +Name_2+ str(file_name_counter)+'.xml'
        taskfile = open(tfile, "w+")

        #header
        taskfile.write("<?xml version=\"1.0\"?>\n")
        taskfile.write("<Task name= \"%s\" >\n" % name)

        #objects
        onames = kautham.kGetObstaclesNames()
        #print(onames)
        taskfile.write("\t<Initialstate>\n")
        for i in range(len(onames)):
            posestr = str(kautham.kGetObstaclePos(onames[i]))
            for char in posestr:
                if char in " ,()":
                    posestr=posestr.replace(char,' ')
            taskfile.write("\t\t<Object object= \"" + onames[i] + "\"> " + posestr + "</Object>\n")
            #<Initialstate>
            #    <Object object= "objname"> -90.0, 80.0, 35.0, 0.0, -1.0, -1.0, 0.0 </Object>
            # </Initialstate>
        taskfile.write("\t</Initialstate>\n")
        #path
        taskfile.write("\t<Transit>\n")
        k = sorted(list(path.keys()))[-1][1]+1
        for i in range(int(len(path.keys())/k)-1):
          tex=''
          for j in range(0,k):
              tex=tex + str(path[i,j]) + " "


          writePath(taskfile,tex,py_taskfile,should_save_txtfile,r2_r3)


        taskfile.write("\t</Transit>\n")

        #Close and save XML document
        taskfile.write("</Task>")
        taskfile.close()


        #Closing the data set file.
        if should_save_txtfile:
            py_taskfile.close()
            print("Results saved in ", pytaskfile)

        print("Results saved in ", tfile)
        return True
    else:
        print("No path, so no Results saved in ", taskfile)
        return False




#Function To normalize Obstacle Controls Loaded from Obs.dat and perm
def Normalize(value,min_value,max_value):
    return (value-min_value)/(max_value-min_value)






#Function to Generate Obs_Point_CloudFile.
#This code will generate point clouds 2800 points and store in file with new line
#Value1X
#value2X
#Then we will reshape the 2800 to 1400 by 2
def pointCloudGenerator(Number_Of_file,Obs_Controls,no_of_obstacles,size_of_obstacles,rn):
    
    #Variable For Number of Points.
    #We will Create 100 Points Per Object
    s=0
    size=no_of_obstacles*200

    obs_cloud=np.zeros((size,2))
    #For Loop For Number of Obstacles
    for i in range (0,no_of_obstacles):
        #For Loop for Number Of Points Per Obstacle
        for j in range(s,200+s):
            #For Loop For Dimension
            for k in range(0,rn):
                obs_cloud[j][k]=random.random()*size_of_obstacles-size_of_obstacles/2.0+Obs_Controls[i][k]
        if(s<size):
            s=s+200
        else:
            break

        file_name='obs_cloud' +str(Number_Of_file)+".npy"
        curr_dirr=os.getcwd()
        pytaskfile = os.path.join(curr_dirr+"/DataSet/obs_cloud",file_name)
        obs_dat_file=open(pytaskfile,"w")
        obs_cloud1=obs_cloud.flatten()
        for i in obs_cloud1:
            obs_dat_file.write(str(i)+"\n")
        obs_dat_file.close()





#This is The Main Function.
def main(r2_r3,no_of_paths,Flag,format,no_of_env,Flag_tf,no_of_obstacles,size_of_obstacles,rn):

    #Setting problem files
    ROSpackage_path = rospack.get_path("kautham")
    modelFolder = ROSpackage_path + "/demos/models/"

    #check for arguments
    if len(sys.argv)<4:
        print("Using default boxes_world demo")

        if r2_r3=="r2":
            kauthamProblemFile = ROSpackage_path + "/demos/OMPL_geo_demos/boxes_world_R2/OMPL_RRTconnect_boxes_world_R21.xml"
        elif r2_r3=="r3":
            kauthamProblemFile= ROSpackage_path + "/demos/OMPL_geo_demos/boxes_world_R3/OMPL_RRTconnect_boxes_world_R3.xml"


        kauthamproblem = os.path.basename(kauthamProblemFile)
    else:
        kauthamProblemFile= ROSpackage_path + "/" + sys.argv[1]
        kauthamproblem = os.path.basename(sys.argv[1])

    print("Using kautham problem",kauthamProblemFile)
    rospy.loginfo ("Starting Kautham Python Client")
    rospy.init_node("kautham_python_client")

    rospy.loginfo_once(kauthamProblemFile)

    ##Solving the motion planning problem
    #Open kautham problem
    print("***************************************")
    print("   Opening problem                     ")
    print("***************************************")
    kautham.kOpenProblem(modelFolder,kauthamProblemFile)


    #Variable used to name the Data set File.
    file_name_counter= 1

    if Flag_tf:
        #To get Current Working Directory.
        curr_dirr=os.getcwd()

        #Creating TaskFiles Folder To Save TaskFiles Per Env.
        folder_name="z_taskfiles"
        folder_created=os.path.join(curr_dirr,folder_name)

        if not pa.exists(folder_created):
            os.mkdir(folder_created)

        #Creating inital and goal state Folder To save Init and goal States.
        folder_name="z_initialANDgoal_states"
        folder_created=os.path.join(curr_dirr,folder_name)

        if not pa.exists(folder_created):
            os.mkdir(folder_created)

    if Flag:
        #Creating Data Set Folder to Save DataSet.
        curr_dirr=os.getcwd()
        folder_name="DataSet"
        folder_created=os.path.join(curr_dirr,folder_name)

        if not pa.exists(folder_created):
            os.mkdir(folder_created)




    #Loading Obstacle.dat File
    #obs_dat=np.fromfile("obs.dat")
    #obs_dat=obs_dat[0:40]
    #obs_dat=np.reshape(obs_dat,(20,2))
    obs_dat_file=open("obs.npy","r")
    obs_dat=obs_dat_file.read()
    obs_dat=obs_dat.split("\n")
    obs_dat=np.array(obs_dat)
    obs_dat=obs_dat[0:40]
    obs_dat=obs_dat.astype(np.float)
    obs_dat=np.reshape(obs_dat,(20,2))
    print("###Obstacles.Dat File###")
    print(obs_dat)



    #Loading Obstacle.PermFile
    obs_perm= np.fromfile('obs_perm2.dat', np.int32)
    size=no_of_obstacles*no_of_obstacles
    obs_perm=obs_perm[0:size]
    obs_perm=np.reshape(obs_perm,(no_of_obstacles,no_of_obstacles))
    
    #Min and Max Value Used to Normalize the Obstacle Control
    min=-30
    max=30




    #For loop for No. of Env.
    for x in range(1,no_of_env+1):

        print("***************************************")
        print("   Changing the environment            ")
        print("***************************************")

        #Variable To Count Init and Goal FileNumber z_initialANDgoal_states/initial_goal_states/init_goal(c).txt.
        c=1
        


        
        #Code To Generate Obs_datFile.

        #This Code will Store the values by a new line
        #Value1
        #Value2
        #obs_dat=np.random.uniform(-20,20,40)
        ##print(obs_dat)
        #obs_dat_file=open("obs.npy","w")
        #for i in obs_dat:
            #obs_dat_file.write(str(i)+"\n")
        #obs_dat_file.close()
        #obs_dat_file=open("obs.npy","r")
        #obs_dat1=obs_dat_file.read()
        #obs_dat1=obs_dat1.split("\n")
        #obs_dat1=np.array(obs_dat1)
        #obs_dat1=obs_dat1[0:40]
        #obs_dat1=obs_dat1.astype(np.float)
        #obs_dat1=np.reshape(obs_dat1,(20,2))
        #print(type(obs_dat1[0][0]))


        #Calculating Obstacle Controls Using Perm and obs.dat file
        print(no_of_obstacles)
        unormalized_obstacle_control=np.zeros((no_of_obstacles,2))
        print(unormalized_obstacle_control.shape)
        obstacle_control=np.zeros((no_of_obstacles,2))
        for l in range(0,no_of_obstacles):
            for m in range(0,2):
                unormalized_obstacle_control[l][m]=obs_dat[obs_perm[x][l]][m]
                obstacle_control[l][m]=Normalize(unormalized_obstacle_control[l][m],min,max)
        print("###Unormalized Obs_Controls###")
        print(unormalized_obstacle_control)
        #unormalized_obstacle_control=unormalized_obstacle_control.flatten()
        obstacle_control=obstacle_control.flatten()
        #Change a=2 if u want to obtacles clouds to be random values.
        a=1

        #Creating the Directory To save files
        #Creating Obs_Points-Cloud Folder.
        folder_name="obs_cloud"
        folder_created=os.path.join(curr_dirr+"/DataSet",folder_name)

        if not pa.exists(folder_created):
            os.mkdir(folder_created)
        
        
        #Calling Obs_Point_Cloud Function.
        pointCloudGenerator(x-1,unormalized_obstacle_control,no_of_obstacles,size_of_obstacles,rn)

        #Setting 30 Obstacle Controls for 3D and 20 For 2D
        if r2_r3=="r3":
            obstaclescontrols = [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()]
        elif r2_r3=="r2":

            if a==1:
                obstaclescontrols=obstacle_control
            
            else:
                obstaclescontrols = [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()]
        print("###Normalized Obs_Controls###")
        print(obstaclescontrols)
        #Setting randomly
        kautham.kSetObstaclesConfig(obstaclescontrols)

        if Flag:
            #Creating SubFolders in DataSet Folder to save DataSet .npy Format.
            folder_name="e"+str(x-1)
            folder_created= os.path.join(curr_dirr+"/DataSet",folder_name)

            if not pa.exists(folder_created):
                os.mkdir(folder_created)
        if Flag_tf:
            #Creating SubFolders in TaksFiles Folder to save TaskFiles .xml.
            folder_name="task_file"+str(x)
            folder_created= os.path.join(curr_dirr+"/z_taskfiles",folder_name)
            if not pa.exists(folder_created):
                os.mkdir(folder_created)

            #Creating SubFolders in z_initialANDgoal_states Folder to save initial and Goal states .txt.
            folder_name="initial_goal_states"+str(x)
            folder_created= os.path.join(curr_dirr+"/z_initialANDgoal_states",folder_name)
            if not pa.exists(folder_created):
                os.mkdir(folder_created)

        #Variable To Count FileNumber of DataSet .npy DataSet/e1/2D_dataSet(file_name_counter).txt.
        file_name_counter=1

        # For Loop to Generate Number of Paths Per Env.
        for z in range(no_of_paths):
            #For loop for Number of Times Init and Goal are initiled False Randomly.
            for y in range(10):

                #For 2D Prob 2D Init and goal i.e x and y.
                if r2_r3=="r2":
                    init = [random.random(), random.random()]
                    goal = [random.random(), random.random()]
                #For 3D Prob 3D Init and goal i.e x and y,z.
                elif r2_r3=="r3":
                    init = [random.random(),random.random(),random.random()]
                    goal = [random.random(),random.random(),random.random()]


                if kautham.kSetQuery(init,goal):
                    print("Query valid (init=", init, " goal = ", goal, "). Calling getPath")
                    path = kautham.kGetPath(0)  #do not print the path

                    if path:
                        if Flag_tf:

                            Name_2="2D_"
                            if r2_r3=="r3":
                                Name_2="3D_"
                            if not Flag:
                                format=".txt"
                            #Writing Initial and Goal State of Every Path Computed in init_goal.txt.
                            tfile_init ='z_initialANDgoal_states/initial_goal_states'+str(x)+"/init_goal_"+Name_2+str(c)+format
                            taskfileinit = open(tfile_init, "w+")

                            if r2_r3=="r2":
                                taskfileinit.write(str(init[0])+" "+str(init[1])+"\n")
                                taskfileinit.write(str(goal[0])+" "+str(goal[1])+"\n")
                            if r2_r3=="r3":
                                taskfileinit.write(str(init[0])+" "+str(init[1])+" "+str(init[2])+"\n")
                                taskfileinit.write(str(goal[0])+" "+str(goal[1])+" "+str(goal[2])+"\n")

                            #Variable To Count Init and Goal FileNumber z_initialANDgoal_states/initial_goal_states/init_goal(c).txt.
                            c+=1

                            taskfileinit.close()

                        #Variable To count Folder Number of .xml Files.
                        folder_number=x

                        if Flag_tf:
                            Functions.writeTaskfile(path, str(x)+"_"+kauthamproblem,Flag,r2_r3,file_name_counter,format,folder_number)
                        if Flag:
                            if not Flag_tf:

                                #Naming the dataset file.
                                 if r2_r3=="r2":
                                     file_name='2D_DataSet' +str(file_name_counter)+format
                                     pytaskfile = os.path.join(curr_dirr+"/DataSet/e"+str(folder_number),file_name)
                                 elif r2_r3=="r3":
                                     file_name='3D_DataSet' +str(file_name_counter)+format
                                     pytaskfile = os.path.join(curr_dirr+"/DataSet/e"+str(folder_number),file_name)

                                 if Flag:
                                     py_taskfile = open(pytaskfile, "w+")
                                 else:
                                     py_taskfile='.txt'

                                 k = sorted(list(path.keys()))[-1][1]+1
                                 for i in range(int(len(path.keys())/k)-1):
                                     tex=''
                                     for j in range(0,k):
                                         tex=tex + str(path[i,j]) + " "

                                     #Calling DataSet Writing Function.
                                     writePathMPNETFormate(tex,py_taskfile,r2_r3)
                                 py_taskfile.close()


                        #Variable To Count FileNumber of DataSet .npy DataSet/e1/2D_dataSet(file_name_counter).txt.
                        file_name_counter+=1

                        break
                else:
                    print("Query not valid (init=", init, " goal = ", goal, "). Skipping getPath call")

    #Close kautham problem
    kautham.kCloseProblem()
