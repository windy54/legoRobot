legoRobot
=========

I have finally managed to control a robot using RaspiConnect on my IPad and the BrickPI interface card.
The robot include a lego ultrasonic range sensor and the HT compass sensor.

The BrickPI software currently does not provide support for the compass sensor , using information gathered from the web I have managed to create a C++ file to enable calibration.

The python files are my raspiconnect interface, local.py and interface to the robot. I have not managed to calibrate the sensor using pyrhon.
