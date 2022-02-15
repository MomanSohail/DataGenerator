#Importing required libraries.
if 1==1:
    import rospy
    import rospkg
    import sys
    import time
    import os
    import json
    from os import curdir, path as pa
    import random
    from matplotlib import pyplot as plt
    import numpy as np
    from std_msgs.msg import String, Time
    from geometry_msgs.msg import Pose
    rospack =rospkg.RosPack()
    import xml.etree.ElementTree as ET
    import random
    from collections import defaultdict
    #Import python module with functions necessary for interfacing with kautham
    import kautham_py.kautham_python_interface as kautham

    #Importing files(Modules.)
    from DataHandler import nodes_handler
    from DataHandler import taskfile_writer
    from SceneGenerator import scene_generator
    from KauthamDataEncoder import encoder

    #Global variables
    directory=''
    Robot_move_control= ''
    Robot_pos=[]
    taskfile=''
    graspedobject= False


#This Function will open the kautham Problem.
def openKauthamProblem(dimension):
    #Setting problem files
    ROSpackage_path = rospack.get_path("kautham")
    modelFolder = ROSpackage_path + "/demos/models/"
    #check for arguments
    if len(sys.argv)<4:
        print("Hello")
        if dimension==2:
            kauthamProblemFile = ROSpackage_path + "/demos/OMPL_geo_demos/boxes_world_R2/OMPL_RRTconnect_boxes_world_R2.xml"
        elif dimension==3:
            kauthamProblemFile= ROSpackage_path + "/demos/OMPL_geo_demos/boxes_world_R3/OMPL_RRTconnect_boxes_world_R3.xml"
        elif dimension==4:
            #kauthamProblemFile= ROSpackage_path + "/demos/OMPL_geo_demos/Synergies/artificialVFRRT.xml"
            kauthamProblemFile="/home/momun/catkin_ws/kautham/demos/OMPL_geo_demos/Synergies/artificialVFRRT.xml"
        kauthamproblem = os.path.basename(kauthamProblemFile)
    else:
        kauthamProblemFile= ROSpackage_path + "/" + sys.argv[1]
        kauthamproblem = os.path.basename(sys.argv[1])

    rospy.loginfo ("Starting Kautham Python Client")
    rospy.init_node("kautham_python_client")
    rospy.loginfo_once(kauthamProblemFile)
    ##Solving the motion planning problem
    #Open kautham problem
    kautham.kOpenProblem(modelFolder,kauthamProblemFile)
    return kauthamproblem


#This is The Kautham Client which will generate the data for dateset.
def kauthamClient(dimension,no_of_paths,flag_path,format,no_of_env,flag_taskfile,no_of_obstacles,size_of_obstacles,rn):

    #For Loop for Number Of Environments To Be Created.
    for x in range(1,no_of_env+1):

        #Opening Kautham Problem by calling the function.
        kauthamproblem=openKauthamProblem(4)

        #Variable used to name the Data set File.
        file_name_counter= 1
        folder_or_file="folder"
        current_dirr=os.getcwd()
        #Creating the required Folders To Save the Datasets.
        if flag_taskfile:

            taskfile_writer.folderOrFileCreater(current_dirr,"TaskFiles",folder_or_file)
            #Creating inital and goal state Folder To save Init and goal States.
            taskfile_writer.folderOrFileCreater(current_dirr+"/TaskFiles","Initial_Goal_States",folder_or_file)

        if flag_path:
            #Creating Data Set Folder to Save DataSet.
            taskfile_writer.folderOrFileCreater(current_dirr,"DataSet",folder_or_file)
            #Creating Folder To save cloud Files.
            taskfile_writer.folderOrFileCreater(current_dirr,"DataSet/obs_cloud",folder_or_file)
        
        #Folder For Saving the centre points of the obstacles.
        taskfile_writer.folderOrFileCreater(current_dirr,"DataSet/obstacle_controls",folder_or_file)

        #Loading Obstacle.dat File
        #Loading Obstacle.Perm File
        obs_dat,obs_perm=scene_generator.readPathObstacleFile(no_of_obstacles,current_dirr)

        #Variable To Count Init and Goal FileNumber initial_goal_states/init_goal(c).txt.
        initial_goal_file_counter=1
        #Calculating Obstacle Controls Using Perm and obs.dat file
        

        #Obstacles Controls Using Obs_Dat and Perm File.
        #unormalized_obstacle_control,obstacle_control=scene_generator.createObstacleControls(no_of_obstacles,obs_dat,obs_perm,rn)
        #Obstacles Controls using random.random()
        unormalized_obstacle_control,obstacle_control=scene_generator.randomObstacleControls(no_of_obstacles,rn)
        obstacle_controls=obstacle_control.flatten()
        print(obstacle_control)


        #Calling Obs_Point_Cloud Function.
        name='obs_cloud' +str(x-1)+".npy"
        obs_dat_file=taskfile_writer.folderOrFileCreater(current_dirr+"/DataSet/obs_cloud",name,"file")
        #Calling Point Cloud Encoder Function.
        encoder.pointCloudEncoder(obs_dat_file,obstacle_control,no_of_obstacles,size_of_obstacles,rn)
        
        #Saving the Centre Locatations of the obstacles
        name='obstacle_control' +str(x-1)+".npy"
        obstacle_control_file=taskfile_writer.folderOrFileCreater(current_dirr+"/DataSet/obstacle_controls",name,"file")
        for control in obstacle_controls:
            obstacle_control_file.write(f"{control}\n")
        obstacle_control_file.close()
        print(obstacle_controls)

        #Setting Obstacles Configuration.
        kautham.kSetObstaclesConfig(obstacle_controls)

        if flag_path:
            #Creating SubFolders in DataSet Folder to save DataSet .npy Format.
            folder_name="e"+str(x-1)
            taskfile_writer.folderOrFileCreater(current_dirr+"/DataSet",folder_name,folder_or_file)

        if flag_taskfile:
            #Creating SubFolders in TaksFiles Folder to save TaskFiles .xml.
            folder_name="Taskfiles"+str(x)
            taskfile_writer.folderOrFileCreater(current_dirr+"/TaskFiles",folder_name,folder_or_file)

            #Creating SubFolders in z_initialANDgoal_states Folder to save initial and Goal states .txt.
            folder_name="initial_goal_states"+str(x)
            taskfile_writer.folderOrFileCreater(current_dirr+"/TaskFiles/Initial_Goal_States",folder_name,folder_or_file)

        #Variable To Count FileNumber of DataSet .npy DataSet/e1/2D_dataSet(file_name_counter).txt.
        file_name_counter=1

        # For Loop to Generate Number of Paths Per Env.
        for z in range(no_of_paths):
            #For loop for Number of Times Init and Goal are initiled False Randomly.
            for y in range(10):

                #For 2D Prob 2D Init and goal i.e x and y.
                if dimension=="r2":
                    init = [random.random(), random.random()]
                    goal = [random.random(), random.random()]
                #For 3D Prob 3D Init and goal i.e x and y,z.
                elif dimension=="r3":
                    init = [random.random(),random.random(),random.random()]
                    goal = [random.random(),random.random(),random.random()]

                if kautham.kSetQuery(init,goal):
                    print("Query valid (init=", init, " goal = ", goal, "). Calling getPath")
                    path = kautham.kGetPath(0)  #do not print the path

                    if path:
                        #Printing Computational Time Of the Planner.
                        print("ComputationTime:",kautham.kGetPlannerComputationTime())

                        if flag_taskfile:

                            if not flag_path:
                                format=".txt"
                            #Writing Initial and Goal State of Every Path Computed in init_goal.txt.
                            taskfileinit = taskfile_writer.folderOrFileCreater(current_dirr+'/TaskFiles/Initial_Goal_States/initial_goal_states'+str(x),"initial_goal"+str(initial_goal_file_counter)+format,"file")

                            if dimension=="r2":
                                taskfileinit.write(str(init[0])+" "+str(init[1])+"\n")
                                taskfileinit.write(str(goal[0])+" "+str(goal[1])+"\n")
                            if dimension=="r3":
                                taskfileinit.write(str(init[0])+" "+str(init[1])+" "+str(init[2])+"\n")
                                taskfileinit.write(str(goal[0])+" "+str(goal[1])+" "+str(goal[2])+"\n")

                            #Variable To Count Init and Goal FileNumber z_initialANDgoal_states/initial_goal_states/init_goal(c).txt.
                            initial_goal_file_counter+=1

                            taskfileinit.close()

                        #Variable To count Folder Number of .xml Files.
                        folder_number=x

                        if flag_taskfile:
                            taskfile =taskfile_writer.folderOrFileCreater(current_dirr+"/TaskFiles/Taskfiles"+str(x)+"/",'taskfile'+ str(file_name_counter)+'.xml',"file")

                            file_name='path' +str(file_name_counter-1)+format
                            py_taskfile =taskfile_writer.folderOrFileCreater(current_dirr+"/DataSet/e"+str(folder_number-1),file_name,"file")
                            taskfile_writer.writeTaskfile(path, str(x)+"_"+kauthamproblem,flag_path,dimension,taskfile,py_taskfile)

                        if flag_path:
                            if not flag_taskfile:

                                #Naming the dataset file.
                                file_name='path' +str(file_name_counter)+format
                                py_taskfile =taskfile_writer.folderOrFileCreater(current_dirr+"/DataSet/e"+str(folder_number-1),file_name,"file")

                                k = sorted(list(path.keys()))[-1][1]+1
                                for i in range(int(len(path.keys())/k)-1):
                                    tex=''
                                    for j in range(0,k):
                                         tex=tex + str(path[i,j]) + " "

                                    #Calling DataSet Writing Function.
                                    taskfile_writer.writePathMPNETFormate(tex,py_taskfile,dimension)

                                py_taskfile.close()

                        #Variable To Count FileNumber of DataSet .npy DataSet/e1/2D_dataSet(file_name_counter).txt.
                        file_name_counter+=1

                        break
                    else:
                        #Restarting Kautham.

                        #nodes_handler.kauthamRosNode("start")
                        #openKauthamProblem(4)
                        print("You Should Restart Kautham-Rosnode if it is crashed.")
                else:
                    print("Query not valid (init=", init, " goal = ", goal, "). Skipping getPath call")

        kautham.kCloseProblem()
        # Kautham Node To Free up Storage.
        print("Restarting Kautham-Node.")
        nodes_handler.kauthamRosNode("kill")
        print("Kautham Node Killed Succefully.")
        time.sleep(2)
        nodes_handler.kauthamRosNode("start")
        print("Kautham Node Restarted Succesfully.")
        time.sleep(3)

    #Close kautham problem
    #kautham.kCloseProblem()


if __name__ == '__main__':
    try:
        nodes_handler.kauthamRosNode("roscore")
        nodes_handler.kauthamRosNode("start")

        #Variable for While loop Condition
        run_code=True

        #While Loop for continue or exit the code.
        while run_code:

            #Loading Configurations From Json File
            config= dict()
            path=sys.argv
            if len(path)<2:
                print("Please Pass Config File Path:")
                exit()
            else:
                filepath=path[1]
                if os.path.isfile(filepath):

                    with open(filepath) as filename:

                        #dictionary with configurations from json file.
                        config=json.load(filename)
                else:
                    print("Please Enter a valid Config File Path:")
                    exit()


            default_or_not="c"
            #User Defined Settings.
            if default_or_not=="c":

                Generate_tf=config["Should_Save_Taskfile"]
                #Flag for Taskfiles Generation.
                Flag_tf=False

                if Generate_tf=="y":
                    Flag_tf=True

                #Asking user that weather to generate txt or numpy file or not.
                #Generate_txt=input("Do you Want to Generate DataSet file or not?(y/n):").lower()
                Generate_txt=config["Should_Save_DataSet"]
                #Flag should be true if we want to generate .txt or numpy file or not.
                Flag=False

                #Setting Flag true if user input y.
                if Generate_txt=="y":
                    #Asking for Format of DataSet file.
                    #format=input("Enter The Format:i.e .txt or .npy:")
                    format=config["Format_Dataset_File"]
                    Flag=True

                #Running for 2D.

                #Assigning Values From The JSON File
                rn=config["Dimension"]
                no_of_env=config["Number_Of_Env"]
                no_of_paths=config["Number_of_Paths"]
                no_of_obstacles=config["Number_of_Obstacles"]
                should_visualize_path_and_PointCloud=config["Should_Visualize_Path_and_ObstacleCloud"]
                size_of_obstacles=config["Size_of_Obstacles"]

                if rn==2:

                    #Main Function Imported From Functions.py
                    # 1st Parameter is for r2=2D and r3=3D
                    # 2nd is for Number of Paths to be computed.
                    # 3rd is for weather to create Dataset or not.
                    # 4th is for format of the Dataset File i.e txt or numpy etc.
                    # 5th is for Number of Enviroments

                    kauthamClient("r2", no_of_paths,Flag,format,no_of_env,Flag_tf,no_of_obstacles,size_of_obstacles,rn)

                #Running for 3D.
                elif rn==3:
                    kauthamClient("r3", no_of_paths,Flag,format,no_of_env,Flag_tf,no_of_obstacles,size_of_obstacles,rn)
                #Running for both 2D and 3D.
                elif rn==1:
                    kauthamClient("r2", no_of_paths, Flag,format,no_of_env,Flag_tf,no_of_obstacles,size_of_obstacles,rn)
                    kauthamClient("r3", no_of_paths, Flag,format,no_of_env,Flag_tf,no_of_obstacles,size_of_obstacles,rn)

            #Asking to run again or exit
            choice=input("\n\nDo You Want To Run Again(y/n):")
            if choice=="n":
                run_code=False

    except rospy.ROSInterruptException:
        pass
