#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|W|i|n|d|y| |S|o|f|t|w|a|r|e| | | | | | | |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# this program is based on lots of sources, apologies for not including all references
# wifi car from brickpi python
#
# oct 10th corrected turn logic for large errors to move shortest distance

from BrickPi import *   #import BrickPi.py file to use BrickPi operations

import time
import sys
import threading
import os



#########################################################
  
I2C_PORT  = PORT_2  # I2C port for the dCompass
I2C_SPEED = 0       # delay for as little time as possible. Usually about 100k baud

I2C_DEVICE_DCOM = 0
###########################################################

def moveForwards():
    global sensorRange
    global stopDistance
    global motorSpeed
    global travelling
    
    travelling ="F"
    
    BrickPi.MotorSpeed[PORT_A] = -motorSpeed * direction  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = -motorSpeed * direction  #Set the speed of MotorD (-255 to 255)

 
   
def moveBackwards():
    global motorSpeed
    global travelling
    
    travelling ="B"
    BrickPi.MotorSpeed[PORT_A] = motorSpeed * direction  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = motorSpeed * direction  #Set the speed of MotorD (-255 to 255)
    
def turnLeft():
    global motorSpeed
    global travelling
    
    travelling = "L"
    BrickPi.MotorSpeed[PORT_A] = +motorSpeed  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = -motorSpeed  #Set the speed of MotorD (-255 to 255)
    
def turnRight():
    global motorSpeed
    global travelling
    
    travelling = "R"
    BrickPi.MotorSpeed[PORT_A] = -motorSpeed   #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = +motorSpeed   #Set the speed of MotorD (-255 to 255)
    
def stop():
    global motorSpeed
    global autoTurn
    global travelling
    
    travelling = "S"
    
    autoTurn = False #clear flag so that auto turn can be stopped if it fails
    BrickPi.MotorSpeed[PORT_A] = -0   #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[PORT_D] = +0   #Set the speed of MotorD (-255 to 255)

def turn(angle):
    global demandedHeading
    global sensorHeading
    global autoTurn
    
    demandedHeading = sensorHeading + angle
    if demandedHeading > 359:
          demandedHeading = demandedHeading - 360
    autoTurn = True

# currently not working, need to stop all sesnor reads in calibrate mode
# and read status on completion
    
def calibrate():
    global calibrating
    
    if(not calibrating):
        calMode = 0x43
        BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 2	#number of bytes to write
        BrickPi.SensorI2CAddr  [I2C_PORT][I2C_DEVICE_DCOM]    = 0x02	#device address
        BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 0
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41	#mode command
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0x43	#cal mode
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][2] = 0x44
        calibrating = True
        response = "Calibrating "
        turnLeft()
    else:
        BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 3	#number of bytes to write
        BrickPi.SensorI2CAddr  [I2C_PORT][I2C_DEVICE_DCOM]    = 0x02	#device address
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41	#mode command
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0	#measure mode
        BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][2] = 0x44

        calibrating = False
        response = "Measuring   "
        stop()
    
    return response

def getRange():
    global sensorRange
    return sensorRange
    
def getHeading():
    global sensorHeading
    return sensorHeading

def shutdown():
    os.system("sudo shutdown -h now")

def setSpeed(newValue):
    global motorSpeed
    global travelling
    
    motorSpeed = newValue
   
    return motorSpeed
    
###########################################################


class myThread (threading.Thread):		#This thread is used for keeping the motor running while the main thread waits for user input
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        global sensorRange
        global sensorHeading
        global stopDistance
        
        while running:

            if  not calibrating :
                if autoTurn:
                    error = demandedHeading - sensorHeading
                    # limit so that move in shorted direction
                    if abs(error) > 180:
                        if error < 0:
                            turnRight()
                        else:
                            turnLeft()
                    elif error > 5:
                        turnRight()
                    elif error < -5:
                        turnLeft()
                    else:
                        stop()
                
                if travelling =="F" and sensorRange<stopDistance:
                    BrickPi.MotorSpeed[0] =0
                    BrickPi.MotorSpeed[3] =0
                    
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            byte1  = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][0]
            byte2  = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][1]
            # use globals !
            sensorHeading = byte2*256 + byte1
            sensorRange = BrickPi.Sensor[PORT_1]

            time.sleep(.1)              # sleep for 100 ms
#########################################################################################
# Initialisation
def robotInitialisation():
    global running
    global calibrating
    global direction
    global sensorRange
    global sensorHeading
    global stopDistance
    global command
    global motorSpeed
    global autoTurn
    global demandedHeading
    global travelling
    
    
    running = True  # used in thread to stop
    autoTurn = False
    direction     = -1 # quick method of changing polarity according to how motors \
                   # are connected
    sensorRange   = 0
    sensorHeading = 720 # normal range is 0 - 360 so initialise to invalid angle

    stopDistance = 20
    calibrating = False
    command = 0
    motorSpeed = 100
    demandedHeading = 0
    travelling ="S"

    BrickPiSetup()  # setup the serial port for communication

    BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
    BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D
    BrickPi.SensorType [PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT   #Set the type of sensor
                                                           # at PORT_1
    BrickPi.SensorType       [I2C_PORT]    = TYPE_SENSOR_I2C
    BrickPi.SensorI2CSpeed   [I2C_PORT]    = I2C_SPEED
    BrickPi.SensorI2CDevices [I2C_PORT]    = 1; # 1 device on bus
    BrickPi.SensorSettings   [I2C_PORT][I2C_DEVICE_DCOM] = 0  
    BrickPi.SensorI2CAddr    [I2C_PORT][I2C_DEVICE_DCOM] = 0x02	#device address
    BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41	#mode command
    BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0x00	#measure command
  
    BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
    BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 1	#number of bytes to write
    BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 2	#number of bytes to read
    BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x44	#heading 

    stop()   # get first range value
    #rickPi.Timeout=3
    #print "BrickPiSetTimeout Status :",BrickPiSetTimeout()    
    print 'here we go'
    thread1 = myThread(1, "Thread-1", 1)		#Setup and start the thread
    thread1.setDaemon(True)
    thread1.start() 


if __name__=="__main__":
   robotInitialisation()
   # running as main so test calibrate - delete until fixed as it screws up sensor
   # calibrate using the c++ program
   #print "lets calibrate"
   #print calibrate()
   #secsStart = time.time()
   #cal = True
   #while(cal):
   #    secsNow = time.time() - secsStart
   #    if secsNow > 20:
   #        cal = False
   #    print secsNow
   #    time.sleep(1)
   #print calibrate()
else:
   robotInitialisation()
       

