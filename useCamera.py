# usecamera.py
# based on Project Curaco idea
# displays picture on lego robot
# sept 30th 2014
# version 1.0

import sys
import subprocess


def takePicture(filename):

    try:
        f = open("/home/pi/StevesPrograms/exposure.txt","r")
        tempString = f.read()
        f.close()
        lowerName = tempString
        
    except IOError as e:
        lowerName = "auto"
    
    exposureMode = lowerName
    cameraCommand = "raspistill -o /home/pi/RasPiConnectServer/static/"+filename\
                          + " -t 100 -n  -q 75 -ex "\
                          + exposureMode
    #+ " -t 100 -n -p 10,10,320,240 -q 75 -ex "\  for preview window
    output = subprocess.check_output(cameraCommand,shell=True,stderr=subprocess.STDOUT)
    
    return

if __name__=="__main__":
    print "test"
    takePicture("legoraw0.jpg")