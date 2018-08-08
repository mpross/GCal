import sys
import time 
from Phidget22.Devices.BLDCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

# Variable initialization
prevValue = 0.0
prevTime=time.clock()
vel=0;
measVel=0;

# Data file to be appended to
f=open("ScalingTest.txt","a+")

# Motor connection
try:
    ch = BLDCMotor()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

def BLDCMotorAttached(e):
    try:
        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def BLDCMotorDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

# This event is called at a regular cadence set by DataInterval timed by the controllers clock.    
def VelocityUpdateHandler(e, velocity):
    global prevValue
    global prevTime
    global measVel

    currentValue=ch.getPosition()
    currentTime=time.clock()
    
    # Outputs and saves set velocity and measured velocity
    print(str(ch.getVelocity()*4000/60) + "   " + str((currentValue-prevValue)/360/(currentTime-prevTime)))
    f.write(str(ch.getVelocity()*4000/60) + "   " + str((currentValue-prevValue)/360/(currentTime-prevTime)) + "\r\n")
    measVel=(currentValue-prevValue)/360/(currentTime-prevTime)
    
    prevValue=currentValue
    prevTime=currentTime

# Initial setup
try:
    ch.setOnAttachHandler(BLDCMotorAttached)
    ch.setOnDetachHandler(BLDCMotorDetached)
    ch.setOnErrorHandler(ErrorEvent)
    ch.setOnVelocityUpdateHandler(VelocityUpdateHandler)

    print("Waiting for the Phidget BLDCMotor Object to be attached...")
    ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
    
ch.setDataInterval(100) # Sets controller output rate. Requires an int and is in millisec
ch.setRescaleFactor(360/12); # Sets scaling of Position readout
ch.setAcceleration(0.2)

# Feedback loop
setVel=10 #Hz
maxVel=0.3 #Duty Cycle
try:
    while(1):    
        
##        vel=abs(0.5*(setVel-measVel)+setVel)/4000*60 
        vel=setVel/4000*60
        # Velocity limit
        if(vel <=maxVel):
            ch.setTargetVelocity(vel)
        else:
            ch.setTargetVelocity(maxVel)
            
except KeyboardInterrupt:
    # Close out
    ch.setTargetVelocity(0)

    try:
        f.close()
        ch.close()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1) 
    print("Closed BLDCMotor device")
    exit(0)     

                  

