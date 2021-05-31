Download The 3 Files and paste in the Kautham-Client Directory.
Run kautham_Clinet file through terminal like this:

->python3 kautham_client_python_sampling_node_boxes_world_R.py config.json




->Art.py Contains the logo for the Kautham.
->config.json Contains Configuration to run the code.
    ->>>"Dimension":2,--Set this to 3 to run kautham problem for 3D.
        "Number_Of_Env":5,--Change to Number Of Enviroments to be Generated.
        "Number_of_Paths":3,--Change to  Number Of Paths per Env to be  Generated.
        "Should_Save_Taskfile":"y",--Set this to "n" if don't want to save taskfiles.
        "Should_Save_DataSet":"y",--Set this to "n" if don't want to save DataSet file.
        "Format_Dataset_File":".txt"--Change to the extention of file i.e.npy.
->Functions.py Contains Implementation of all the functions.
->kautham_Clinet file contain main funxtion and function call(You should run only this file through terminal)
