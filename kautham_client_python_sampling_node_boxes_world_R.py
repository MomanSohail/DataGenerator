#This is the Python Client File.
#In this File There are only Functions Calls.Implementation is in(Functions.py)
#This File will Run the 2D as Well as 3D Kautham Problem.


#!/usr/bin/env python3
import rospy
import rospkg
import sys
import os
import random

import Functions
import Art

from std_msgs.msg import String, Time
from geometry_msgs.msg import Pose
rospack =rospkg.RosPack()
import xml.etree.ElementTree as ET
from collections import defaultdict
#Import python module with functions necessary for interfacing with kautham
import kautham_py.kautham_python_interface as kautham


# Global variables
directory=''
Robot_move_control= ''
Robot_pos=[]
taskfile=''
graspedobject= False



if __name__ == '__main__':
    try:

        #Variable for While loop Condition
        run_code=True

        #While Loop for continue or exit the code.
        while run_code:

            #printing Kautham Logo.from Art.py file.
            print(Art.logo_welcome)
            print(Art.logo_kautham)
            print("\n\n")

            #Asking to Run Default or Custom.
            print("If u Type \'d\' Kautham Client Will Generate:100 Env. and 100 Paths per Env.")
            print("If u Type \'c\'. You can Select Number of Paths and Env.")
            default_or_not=input("Run Custom or Default?(c/d):")

            #Default Setting for the program.(HardCoded.).
            if default_or_not=="d":
                print("\nIf You Enter \'2\' Kautham Client will run 2D Problem and for \'3\' 3D.")
                r2_r3=int(input("Enter 2 for \'2D\' and 3 for \'3D\' problem:"))
                if r2_r3==2:

                    # 1st Parameter is for r2=2D and r3=3D
                    # 2nd is for Number of Paths to be computed.
                    # 3rd is for weather to create Dataset or not.
                    # 4th is for format of the Dataset File i.e txt or numpy etc.
                    # 5th is for Number of Enviroments

                    Functions.main("r2",100,True,".txt",100,True)
                elif r2_r3==3:
                    Functions.main("r3",100,True,".txt",100,True)
                elif r2_r3==1:
                    Functions.main("r2",100,True,".txt",100,True)
                    Functions.main("r3",100,True,".txt",100,True)


            #User Defined Settings.
            elif default_or_not=="c":
                #input from the users.
                #r2_r3 is for Either 2D or 3D file Run.
                print("\nIf You Enter \'2\' Kautham Client will run 2D Problem and for \'3\' 3D.")
                r2_r3=int(input("Enter 2 for \'2D\' and 3 for \'3D\' problem:"))

                #no_of_env is for how many Enviroments u want to Create.
                no_of_env=input("\n Enter The Number of Enviroments You Want to Generate:")
                no_of_env=int(no_of_env)

                #no_of_paths is for how many Paths You want Per Enviroment.
                no_of_paths=input("Enter The Number of Paths Per Env. You Want to Generate:")
                no_of_paths=int(no_of_paths)

                #Asking user that weather to generate taskfile and intial and Goal State or not.
                Generate_tf=input("Do you Want to Generate Taskfiles and Inital and Goal State Files.?(y/n):").lower()

                #Flag for Taskfiles Generation.
                Flag_tf=False

                if Generate_tf=="y":
                    Flag_tf=True

                #Asking user that weather to generate txt or numpy file or not.
                Generate_txt=input("Do you Want to Generate DataSet file or not?(y/n):").lower()

                #Flag should be true if we want to generate .txt or numpy file or not.
                Flag=False

                #Setting Flag true if user input y.
                if Generate_txt=="y":
                    #Asking for Format of DataSet file.
                    format=input("Enter The Format:i.e .txt or .npy:")
                    Flag=True

                #Running for 2D.
                if r2_r3==2:

                    #Main Function Imported From Functions.py
                    # 1st Parameter is for r2=2D and r3=3D
                    # 2nd is for Number of Paths to be computed.
                    # 3rd is for weather to create Dataset or not.
                    # 4th is for format of the Dataset File i.e txt or numpy etc.
                    # 5th is for Number of Enviroments

                    Functions.main("r2", no_of_paths,Flag,format,no_of_env,Flag_tf)

                #Running for 3D.
                elif r2_r3==3:
                    Functions.main("r3", no_of_paths,Flag,format,no_of_env,Flag_tf)
                #Running for both 2D and 3D.
                elif r2_r3==1:
                    Functions.main("r2", no_of_paths, Flag,format,no_of_env,Flag_tf)
                    Functions.main("r3", no_of_paths, Flag,format,no_of_env,Flag_tf)

            #Asking to run again or exit
            choice=input("\n\nDo You Want To Run Again(y/n):")
            if choice=="n":
                run_code=False



    except rospy.ROSInterruptException:
        pass
