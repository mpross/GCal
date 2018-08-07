import sys
import time 
from Phidget22.Devices.BLDCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

prevValue = 0.0
prevTime=time.clock()
f=open("data.txt","a+")

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
    
def VelocityUpdateHandler(e, velocity):
    global prevValue
    global prevTime
    
    currentValue=ch.getPosition()
    currentTime=time.clock()
    
##    print(str(ch.getVelocity()*4000/60) + "   " + str((currentValue-prevValue)/360/(currentTime-prevTime)))
##    f.write(str(ch.getVelocity()*4000/60) + "   " + str((currentValue-prevValue)/360/(currentTime-prevTime)) + "\r\n")
    print(ch.getPosition())
    prevValue=currentValue
    prevTime=currentTime
    
def closeOut():
    ch.setTargetVelocity(0)
    ch.close()
    print("Stopped")

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
    
ch.setDataInterval(100) #Requires an int and is in millisec
ch.setRescaleFactor(360/12);

##ch.setTargetVelocity(3.5/4000*60)

while(1):
    ch.setTargetVelocity(0)
##time.sleep(10)

f.close()

try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed BLDCMotor device")
exit(0)                     

