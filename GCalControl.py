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
fileName="NoiseRun_5Hz.txt"
setVel=3 #Hz

# Motor connection
try:
    print("LIGO GCal Control")
    fileName=input("Enter data file name: ")
    # Data file to be appended to
    if ".txt" in fileName:
        if not os.path.exists("data/"+fileName):
            f=open("data/"+fileName,"a+")
        else:
            option=input("File already exists\nOverwrite, Append, or NewFile: ")
            if "a" in option:
                f=open("data/"+fileName,"a+")
            elif "o" in option:
                f=open("data/"+fileName,"w+")
            else:
                i=1
                newFileName=fileName.replace(".txt","")+"("+str(i)+")"+".txt"
                while(os.path.exists("data/"+newFileName)):
                    newFileName=fileName.replace(".txt","")+"("+str(i)+")"+".txt"
                    i+=1
                f=open("data/"+newFileName,"a+")
    else:
        if not os.path.exists("data/"+fileName+".txt"):
            f=open("data/"+fileName+".txt","a+")
        else:
            option=input("File already exists\nOverwrite, Append, or NewFile: ")
            if "a" in option:
                f=open("data/"+fileName+".txt","a+")
            elif "o" in option:
                f=open("data/"+fileName+".txt","w+")
            else:
                i=1
                newFileName=fileName+"("+str(i)+")"+".txt"
                while(os.path.exists("data/"+newFileName)):
                    newFileName=fileName+"("+str(i)+")"+".txt"
                    i+=1
                f=open("data/"+newFileName,"a+")
    setVel=float(input("Set rotor frequency in Hz: "))
    
    ch = BLDCMotor()
except RuntimeError as e:
    print("Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

def BLDCMotorAttached(e):
    try:
        attached = e
        print("\nMotor Attached")
        print("\n")
    except PhidgetException as e:
        print("Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def BLDCMotorDetached(e):
    detached = e
    try:
        print("\nMotor Detached")
    except PhidgetException as e:
        print("Exception %i: %s" % (e.code, e.details))
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

    print("Waiting for motor to attach")
    ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit\n")
    readin = sys.stdin.read(1)
    exit(1)
    
ch.setDataInterval(100) # Sets controller output rate. Requires an int and is in millisec
ch.setRescaleFactor(360/12); # Sets scaling of Position readout
ch.setAcceleration(0.2)

# Feedback loop
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
        ch.close()
        f.close()
    except PhidgetException as e:
        print("Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit\n")
        readin = sys.stdin.read(1)
        exit(1) 
    print("Disconnected from motor")   

                  

