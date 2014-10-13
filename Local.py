#!/usr/bin/python 
# Filename: local.py 
# MiloCreek BP MiloCreek 
# Version 3.0 6/11/2014 
# 
# Local Execute Objects for RasPiConnect  
# to add Execute objects, modify this file 
# 
# Modified by Steve Gale to control robot using dexter industries BrickPi
# robot includes ultrasonic sesnor, compass and PI camera
# update rate for camera is slow
#

# system imports
import sys
import subprocess
import os
import time
# RasPiConnectImports

import Config
import Validate
import BuildResponse 

# import robot library
sys.path.append("/home/pi/StevesPrograms/")
import legoRaspiConnect as lego
import useCamera

pictureFileStatus = 0

def ExecuteUserObjects(objectType, element):

    global pictureFileStatus
    # Example Objects

    # fetch information from XML for use in user elements

    #objectServerID is the RasPiConnect ID from the RasPiConnect App

    objectServerID = element.find("./OBJECTSERVERID").text
    objectID       = element.find("./OBJECTID").text
    objectAction   = element.find("./OBJECTACTION").text
    objectName     = element.find("./OBJECTNAME").text

    if (Config.debug()):
        print("objectServerID = %s" % objectServerID)
    # 
    # check to see if this is a Validate request
    #
    validate = Validate.checkForValidate(element)

    if (Config.debug()):
        print "VALIDATE=%s" % validate

        
    # Build the header for the response

    outgoingXMLData = BuildResponse.buildHeader(element)

    #
    #
    
    if objectAction=="SINGLEPUSH":
        
        if (objectServerID == "B-1"):
                # stop
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute
                #
                # Execute your code
                #
                #
                lego.stop()
                responseData = "OK" ## send an OK back to the App
                # Done with your code
                #
                #

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

        elif (objectServerID == "B-4"): 

                # left
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute

                lego.turnLeft()
                responseData = "OK" ## send an OK back to the App
                #
                #
                # Done with your code

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
                


        elif (objectServerID == "B-5"):
                # right
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute
                #
                # Execute your code
                #
                #
                lego.turnRight()
                responseData = "OK" ## send an OK back to the App
                # Done with your code
                #
                #

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

        elif (objectServerID == "B-6"):
                # forwards
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute

                lego.moveForwards()
                responseData = "OK" ## send an OK back to the App
                # Done with your code
                #
                #

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

                
        elif (objectServerID == "B-7"):
                # backwards
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute

                lego.moveBackwards()
                responseData = "OK" ## send an OK back to the App
                # Done with your code
                #
                #

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

                
        elif (objectServerID == "B-8"):
                # shutdown
                #check for validate request
                # validate allows RasPiConnect to verify this object is here 

                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData

                # not validate request, so execute
                #
                # Execute your code
                #
                #
                os.system("sudo shutdown -h now")
                responseData = "OK" ## send an OK back to the App
                # Done with your code
                #
                #

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData

        elif (objectServerID == "B-9"):
                #calibrate
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData
                
                responseData = "exit"
                print "exit "
                sys.exit()

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData  

        elif (objectServerID == "B-10"):
                #calibrate
                if (validate == "YES"):
                        outgoingXMLData += Validate.buildValidateResponse("YES")
                        outgoingXMLData += BuildResponse.buildFooter()
                        return outgoingXMLData
                
                responseData = "ok"
                lego.turn(90)

                outgoingXMLData += BuildResponse.buildResponse(responseData)
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
        elif (objectServerID == "FB-1"):
            #calibrate
            if (validate == "YES"):
                outgoingXMLData += Validate.buildValidateResponse("YES")
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
        
            responseData = lego.calibrate()

            outgoingXMLData += BuildResponse.buildResponse(responseData)
            outgoingXMLData += BuildResponse.buildFooter()
            return outgoingXMLData


        else:
                # returning a zero length string tells the server that you have not matched 
                # the object and server 
                print "unknown objectServerID ",objectServerID
                #lego.stop()
                                
    elif (objectServerID == "LT-1"):
        #text box range
        if (validate == "YES"):
                outgoingXMLData += Validate.buildValidateResponse("YES")
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
        range = lego.getRange()
        responseData = "%d" % (range)

        outgoingXMLData += BuildResponse.buildResponse(responseData)
        outgoingXMLData += BuildResponse.buildFooter()
        return outgoingXMLData
        
    elif (objectServerID == "LT-2"):
        #text box heading
        if (validate == "YES"):
                outgoingXMLData += Validate.buildValidateResponse("YES")
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
        heading = lego.getHeading()
        responseData = "%d" % (heading,)

        outgoingXMLData += BuildResponse.buildResponse(responseData)
        outgoingXMLData += BuildResponse.buildFooter()
        return outgoingXMLData


    elif (objectServerID == "SL-1"):
        #adjust speed
        if (validate == "YES"):
                outgoingXMLData += Validate.buildValidateResponse("YES")
                outgoingXMLData += BuildResponse.buildFooter()
                return outgoingXMLData
        
        commandResponse = objectAction
        motorSpeed = float(commandResponse) * 2.5
        if  motorSpeed > 250:
            motorSpeed = 250
        newValue =  float(lego.setSpeed( int(motorSpeed) ) ) / 2.5 # integer 0 to 100
        responseData = "%d" % (newValue)

        outgoingXMLData += BuildResponse.buildResponse(responseData)
        outgoingXMLData += BuildResponse.buildFooter()
        return outgoingXMLData
    elif (objectServerID == "W-2"):
    
        #check for validate request
        if (validate == "YES"):
            outgoingXMLData += Validate.buildValidateResponse("YES")
            outgoingXMLData += BuildResponse.buildFooter()

            return outgoingXMLData
            
        # normal response requested 

        imageName = "legoraw.jpg"
        if pictureFileStatus == 0:
            imageName = "RovioImage.jpg"
            useCamera.takePicture("legoraw1.jpg")
            pictureFileStatus = 1
        elif pictureFileStatus == 1:
            imageName = "legoraw1.jpg"
            useCamera.takePicture("legoraw2.jpg")
            pictureFileStatus = 2
        else:
            imageName = "legoraw2.jpg"
            useCamera.takePicture("legoraw1.jpg")
            pictureFileStatus = 1
        

        responseData = "<html><head>"
        responseData += "<title></title><style>body,html,iframe{margin:0;padding:0;}</style>"
        responseData += "</head>"
        
        responseData += "<body><img src=\""
        responseData += Config.localURL() 
        responseData += "static/"
        responseData += imageName
        responseData += "\" type=\"jpg\" width=\"300\" height=\"300\">"
        responseData += "<BR>Picture<BR>"

        responseData +="</body>"
        
        responseData += "</html>"
    
        
        outgoingXMLData += BuildResponse.buildResponse(responseData)
        outgoingXMLData += BuildResponse.buildFooter()
        if (Config.debug()):
            print outgoingXMLData

        return outgoingXMLData  

    else:
        # returning a zero length string tells the server that you have not matched 
        # the object and server 
        #lego.stop()
        return ""

