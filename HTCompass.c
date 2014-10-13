/*
*  Jaikrishna
*  t.s.jaikrishna<at>gmail.com
*  Initial date:  	June 21, 2013
*  Updated : 		May 30, 2014
*  Modified by Steve Gale Sept 2012 to connect to hitechnic NXT magnetic compass sensor
*  also based on Xander Soldaat's driver for this device
*  Based on Matthew Richardson's example on testing BrickPi drivers and Xander Soldaat's 
*  Example on NXT for RobotC
*  You may use this code as you wish, provided you give credit where it's due.
*  
*  This is a program for testing the RPi BrickPi drivers and I2C communication on 
*  the BrickPi  
*
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with the Magnnetic Compass from Hitechnic 
# Product webpage: http://www.hitechnic.com
*/

#include <stdio.h>
#include <math.h>
#include <time.h>
#include <math.h>
#include "tick.h"

#include <wiringPi.h>

#include "BrickPi.h"


#include <linux/i2c-dev.h>   
#include <fcntl.h>

// gcc -o program "Test BrickPi lib.c" -lrt -lm -L/usr/local/lib -lwiringPi
// gcc -o program "Test BrickPi lib.c" -lrt
// ./program

int result;



float angle;

#define PI 3.14159265359
#define I2C_PORT  PORT_2                             // I2C port for the dCompass CHANGE TO SUIT
#define I2C_SPEED 0                                  // delay for as little time as possible. Usually about 100k baud

#define I2C_DEVICE_DCOM 0                        // DComm is device 0 on this I2C bus
#define COMPASS_MODE 0x41
#define COMPASS_HEADING_UPPER 0x42
#define COMPASS_HEADING_LOWER 0x43

int initialiseCompass(){
  /* initialise sensor to measure mode */
  int result;
  BrickPi.Address[0] = 1;
  BrickPi.Address[1] = 2;
  BrickPi.SensorType       [I2C_PORT]    = TYPE_SENSOR_I2C;
  BrickPi.SensorI2CSpeed   [I2C_PORT]    = I2C_SPEED;
  BrickPi.SensorI2CDevices [I2C_PORT]    = 1; // 1 device on bus?
  BrickPi.SensorSettings   [I2C_PORT][I2C_DEVICE_DCOM] = 0;  
  BrickPi.SensorI2CAddr    [I2C_PORT][I2C_DEVICE_DCOM] = 0x02;	//device address
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 2;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 0;	//number of bytes to read
  
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41;	//mode command
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0x00;	//measure command
  
  result = BrickPiSetupSensors();
  return result;
}

int getHeading(){
  /* reads heading from compass */
  int heading;
  char byte1,byte2;
  
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 1;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 2;	//number of bytes to read
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x44;	//heading upper
  
  result = BrickPiUpdateValues();
  if(!result){  
          
    byte1  = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][0];
    byte2  = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][1];
    heading = byte2*256 + byte1;
  }
  else heading = -180;

  return heading;
}

char* getVersionNumber() {
  char high,low;
  int result;
  
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 1;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 8;	//number of bytes to read
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0;	//version
  result = BrickPiUpdateValues();
  if(!result){  
    high = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][2]-48;//convert from ascii to integer
    low  = BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][4]-48;
    /*return high * 16 + low;*/
    return &BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][1];
  }
  else printf("error\n");

  return "error "; /*result;*/
}

char* getManufacturer() {
  char high,low;
  int result;
  
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 1;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 8;	//number of bytes to read
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 8;	//manufacturer
  result = BrickPiUpdateValues();
  if(!result){  
    return &BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][0];
  }
  else printf("error\n");

  return "error "; /*result;*/
}

char* getSensor() {
  char high,low;
  int result;
  
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 1;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 8;	//number of bytes to read
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 16;	//sensor
  result = BrickPiUpdateValues();
  if(!result){  
    return &BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][0];
  }
  else printf("error\n");

  return "error "; /*result;*/
}


int startCalibration(){
  int result;
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 2;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 0;	//number of bytes to read
  
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41;	//mode command
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0x43;	//calibrate command
  result = BrickPiUpdateValues();
  
  return result;
}

int stopCalibration(){
  int result;
  BrickPi.SensorI2CWrite [I2C_PORT][I2C_DEVICE_DCOM]    = 2;	//number of bytes to write
  BrickPi.SensorI2CRead  [I2C_PORT][I2C_DEVICE_DCOM]    = 1;	//number of bytes to read
  
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][0] = 0x41;	//mode command
  BrickPi.SensorI2COut   [I2C_PORT][I2C_DEVICE_DCOM][1] = 0x0;	//calibrate command
  result = BrickPiUpdateValues();
  printf("Calibration result = %d\n",BrickPi.SensorI2CIn[I2C_PORT][I2C_DEVICE_DCOM][0]);
  return result;
}


   
   
int main() {
  int angleLow;
  int angleHigh;
  int angle;
  int calDelay = 0;
  
  char* version;
  int nbytes = 1;
  ClearTick();

  result = BrickPiSetup();
  printf("BrickPiSetup: %d\n", result);
  if(result)
    return 0;
  
  result = initialiseCompass(); // set up BrickPi and measure mode
  printf("BrickPiSetupSensors: %d\n", result);
  if(result)
    return 0;
  usleep(500000);
  
  version = getVersionNumber();
  printf("Version Number %s\n",version);

  usleep(500000);
  printf("Manufacturer %s\n",getManufacturer());

  usleep(500000);
  printf("Sensor %s\n",getSensor());

  usleep(500000);
  /* ***********************************************************************************
  *
  * I calibrated sensor by placing on a turntable and manually rotating one and a
  * half turns in 20 seconds to prove the software
  * I intended to use my robot to calibrate ny powering the motors.
  * Currently (oct 2014) I cant calibrate the sensor in Python. I think is due to
  * how I am using a class to call BrickPI.updatevalues()
  * The software below puts the compass into calibrate mode, performs no further actions
  * for 20 seconds until it selects measurement mode and reads the result.
  ***************************************************************************************/
  printf("start calibration result = %d\n",startCalibration());
  printf(" Calibration started\n");
  //usleep(20000000);
  while (calDelay<20){
     usleep(1000000);
     calDelay++;
     printf("%d\n",calDelay);
  }
  printf("stop calibration result = %d\n",stopCalibration());
  printf("calibration stopped\n");
  usleep(500000);
  
  printf("start of while loop\n");
  while(1){
      angle = getHeading();
      printf("heading = %d \n",angle);
      usleep(500000);
    }
  return 0;

}
