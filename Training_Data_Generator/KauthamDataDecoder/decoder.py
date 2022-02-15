import numpy as np
import os
from os import path as pa


#This Function Will Convert Path File Generated From MPNET into XML file to be visulazied in kautham.
def decodePath2XML(path_filename,obstacle_filename,no_of_obstacles,file_name_counter):

    #This Function will write path into the conf tag of xml file to be generated.
    def writePath(taskfile,path):

        taskfile.write("\t\t<Conf> %s </Conf>\n" % path)

        return True

    #This Function Will Read Path File Genrated by MPENT.
    def readPathFile(pathfile_name):
        path_file=open(pathfile_name,"r")
        path=path_file.read()
        path=path.split("\n")
        path=np.array(path)
        #Checking If the Lenght is odd then Reshape.
        if len(path)%2==0:
            path=path
        else:
            size=len(path)
            path=path[0:size-1]

        #Reshaping to 2-D Array.
        path=path.reshape(-1,2)
        #Final Path Array.
        mpnet_path=path.astype(np.float)

        return mpnet_path

    #This Function Will Read Obs_Cloud File from MPNET DataSet.
    def readObstacleFile(obstacle_filename,no_of_obstacles):

        #Final Path Array.
        obstacles_cloud=readPathFile(obstacle_filename)
        #Reshaping to 1400 values.
        obstacles_cloud=obstacles_cloud[0:1400]
        #Calculating Centre Points.

        total_points=0
        size=no_of_obstacles*200
        mpnet_obstacles=np.zeros((no_of_obstacles,2))

        #For Loop For Number of Obstacles
        for i in range (0,no_of_obstacles):

            no_of_points=0
            x_points=np.zeros(200)
            y_points=np.zeros(200)

            #For Loop for Number Of Points Per Obstacle
            for j in range(total_points,200+total_points):
                #For Loop For Dimension
                #for k in range(0,2):
                    #obs_cloud[j][k]=random.random()*size_of_obstacles-size_of_obstacles/2.0+Obs_Controls[i][k]

                #Sperating the X and Y values.
                x_points[no_of_points]=obstacles_cloud[j][0]
                y_points[no_of_points]=obstacles_cloud[j][1]
                no_of_points+=1

            #Sorting the List.
            x_points=np.sort(x_points)
            y_points=np.sort(y_points)
            mpnet_obstacles[i][0]=x_points[100]
            mpnet_obstacles[i][1]=y_points[100]

            if(total_points<size):
                total_points=total_points+200
            else:
                break

        return mpnet_obstacles

    #This Function will write a xmlFile from MPNET DataSet Files.
    def writeTaskfile(path,objects,prob_name,file_name_counter):
        global taskfile
        if 2==2:

            curr_dirr=os.path.dirname(os.path.abspath(__file__))

            #Creating MPNET Path Folder to save files.
            folder_name="Decoded Taskfiles"
            folder_created=os.path.join(curr_dirr,folder_name)
            if not pa.exists(folder_created):
                os.mkdir(folder_created)

            #Naming The XMLFile
            tfile =f'{folder_created}/mpnet_decoded_taskfile'+ str(file_name_counter)+'.xml'
            taskfile = open(tfile, "w+")

            #Writing the Header.
            taskfile.write("<?xml version=\"1.0\"?>\n")
            taskfile.write("<Task name= \"%s\" >\n" % prob_name)

            #Writing Initial State.
            taskfile.write("\t<Initialstate>\n")

            #Manually defining Objects Name.
            onames=["plain","plainbox_1","plainbox_2","plainbox_3","plainbox_4","plainbox_5","plainbox_6","plainbox_7","walls"]

            #Manually Defining walls and plain position.
            wall_position="-20.0 20.0 20.0 -0.9987522959709167 0.049937617033720016 0.0 2.9592790603637695"
            plain_position="0.0 0.0 0.0 0.0 0.0 1.0 0.0"

            taskfile.write("\t\t<Object object= \"" + onames[0] + "\"> " + plain_position + "</Object>\n")

            for i in range(0,len(objects)):

                posestr = str(objects[i][0])+str(objects[i][1])+"0.10000000149011612 8.659561265171044e-17 -0.7071068286895752 0.7071068286895752 3.1415927410125732"
                #Writing the Objects
                taskfile.write("\t\t<Object object= \"" + onames[i+1] + "\"> " + posestr + "</Object>\n")

            taskfile.write("\t\t<Object object= \"" + onames[8] + "\"> " + wall_position + "</Object>\n")
                #<Initialstate>
                #    <Object object= "objname"> -90.0, 80.0, 35.0, 0.0, -1.0, -1.0, 0.0 </Object>
                #</Initialstate>

            taskfile.write("\t</Initialstate>\n")

            #Writing Path
            taskfile.write("\t<Transit>\n")

            #path is a 2-d Array so.
            #For loop for number of values.
            for i in range(0,len(path)):

                tex=''

                #for loop for Dimension||X and Y Values.
                for j in range(0,2):
                    tex=tex + str(path[i,j]) + " "

                #Manually Assigning other 5 values as we need 7 for the kautham to display xml file.
                tex=tex + "0.0560000017285347" + " "+"8.659559941682064e-17" + " "+"-0.7071070075035095" + " "+"0.7071070075035095" + " "+"-4.3711398944878965e-08"

                #Calling Function to write the Path.
                writePath(taskfile,tex)

            taskfile.write("\t</Transit>\n")

            #Close and save XML document
            taskfile.write("</Task>")
            taskfile.close()

            #print("Results saved in ", tfile)
            return True

        else:
            #print("No path, so no Results saved.")
            return False

    #Calling Functions.
    mpnet_path=readPathFile(path_filename)
    mpnet_obstacles=readObstacleFile(obstacle_filename,no_of_obstacles)

    #Name of the Problem File of Kautham
    #Which will Load this TaskFile.
    name="10_OMPL_RRTconnect_boxes_world_R21.xml"

    #Function Call.
    writeTaskfile(mpnet_path,mpnet_obstacles,name,file_name_counter)




#Calling the Functions.
root_dir=os.path.dirname(os.path.abspath(__file__))

path_filename=os.path.join(root_dir,"path0.txt")
obstacle_filename=os.path.join(root_dir,"obs_cloud0.npy")

decodePath2XML(path_filename,obstacle_filename,7,1)
