import os
import time

def kauthamRosNode(task):
    if task=="roscore":
         os.system('gnome-terminal -- bash -c roscore')
    elif task=="start":
        os.system("gnome-terminal -- bash -c 'rosrun kautham kautham-rosnode'")
    elif task=="kill":
        os.system("rosnode kill kautham_node")
