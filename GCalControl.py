import sys
import time
import os

sys.path.append(os.getcwd()+"/lib")

from Phidget22.Devices.BLDCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

# Variable initialization
prevValue = 0.0
prevTime=time.perf_counter()
vel=0;
measVel=0;

# Data file to be appended to
f=open("data/NoiseRun_5Hz.txt","a+")

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
        print("\nMotor Attached")
        print("\n")
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def BLDCMotorDetached(e):
    detached = e
    try:
        print("\nMotor Detached")
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
    currentTime=time.perf_counter()
    
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

    print("Waiting for motor to attach...")
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
setVel=5 #Hz
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
    print("Disconnected from motor")
    exit(0)     

                  

