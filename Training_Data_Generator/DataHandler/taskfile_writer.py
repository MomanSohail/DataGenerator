#Importing Libraries.
import os
from os import path as pa
import kautham_py.kautham_python_interface as kautham

#This Function will create a file or folder in the directory to save dataset.
def folderOrFileCreater(curr_dir,name,folder_or_file):
    
    if folder_or_file=="folder":
        folder_created=os.path.join(curr_dir,name)
        if not pa.exists(folder_created):
            os.mkdir(folder_created)
    
    elif folder_or_file=="file":
        filename=os.path.join(curr_dir,name)
        opened_file=open(filename,"w+")
        return opened_file

#This Function will Write a Seperate Data Set file as npy or txt.
def writePathMPNETFormate(kautham_path,py_taskfile,dimension):
     #Splitting the tex string into a list.
     python_kpath=kautham_path.split(" ")

     if dimension=="r2":
         #Writing only x and y for 2D.
        py_taskfile.write(f"{python_kpath[0]}\n{python_kpath[1]}\n")
     elif dimension=="r3":
         #Writting x,y and z for 3D.
        py_taskfile.write(f"{python_kpath[0]}\n{python_kpath[1]}\n{python_kpath[2]}\n")

     return True

#This Function is Used to write Conf tag in .xml file
#It is being called in writeTaskfile Function.
def writePath(taskfile,kautham_path,py_taskfile,should_save_txtfile,dimension):

    taskfile.write("\t\t<Conf> %s </Conf>\n" % kautham_path)

    #Calling Function to generate Data Set.txt file.
    if should_save_txtfile:
        writePathMPNETFormate(kautham_path,py_taskfile,dimension)

    return True

#This Function will write the taskfile in .xml
#3rd parameter is for .txt Data Set Should be saved or not.
#7th is for Folder Name in which xml should be saved.
def writeTaskfile(path,name,should_save_txtfile,dimension,kTaskfile,py_taskfile):

    global taskfile
    taskfile=kTaskfile
    if path:

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
          kpath=''
          for j in range(0,k):
              kpath=kpath + str(path[i,j]) + " "

          writePath(taskfile,kpath,py_taskfile,should_save_txtfile,dimension)

        taskfile.write("\t</Transit>\n")

        #Close and save XML document
        taskfile.write("</Task>")
        taskfile.close()
        py_taskfile.close()

        return True
    else:
        return False