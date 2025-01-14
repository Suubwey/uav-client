################################################################################################
# @File DroneKitPX4.py
# Example usage of DroneKit with PX4
#
# @author Sander Smeets <sander@droneslab.com>
#
# Code partly based on DroneKit (c) Copyright 2015-2016, 3D Robotics.
################################################################################################

# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import gpiozero
from time import sleep
import time, math
import RPi.GPIO as GPIO
gpiozero.Device.pin_factory = PiGPIOFactory()
################################################################################################
# Settings
################################################################################################
    
MAV_MODE_AUTO   = 4


################################################################################################
# Init
################################################################################################

# Connect to the Vehicle
print("Connecting")
vehicle = connect("/dev/ttyACM0", wait_ready=True)
    


################################################################################################
# Listeners
################################################################################################

home_position_set = False
#Create a message listener for home position fix
@vehicle.on_message('HOME_POSITION')
def listener(self, name, home_position):
    global home_position_set
    home_position_set = True



################################################################################################
# Start mission example
################################################################################################


# wait for a home position lock
while not home_position_set:
    print("Waiting for home position...")
    time.sleep(1)

# Display basic vehicle state
print(" Type: %s" % vehicle._vehicle_type)
print(" Armed: %s" % vehicle.armed)
print(" System status: %s" % vehicle.system_status.state)
print(" GPS: %s" % vehicle.gps_0)
print(" Alt: %s" % vehicle.location.global_relative_frame)

home = vehicle.location.global_relative_frame

def mission(response):

    # Change to AUTO mode
    PX4setMode(MAV_MODE_AUTO)
    time.sleep(1)

    # Load commands
    cmds = vehicle.commands
    cmds.clear()



    # takeoff to 10 meters
    wp = get_location_offset_meters(home, 0, 0, 10);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)



    for i in response:
        wp = get_location_offset_meters_dict(i, 0, 0, 0);
        cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
        cmds.add(cmd)


    # land
    wp = get_location_offset_meters(home, 0, 0, 10);
    cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0, wp.lat, wp.lon, wp.alt)
    cmds.add(cmd)


    # Upload mission
    cmds.upload()
    time.sleep(2)

    # Arm vehicle
    vehicle.armed = True

    # monitor mission execution
    nextwaypoint = vehicle.commands.next
    while nextwaypoint < len(vehicle.commands):
        if vehicle.commands.next > nextwaypoint:
            display_seq = vehicle.commands.next+1
            print("Moving to waypoint %s" % display_seq)
            nextwaypoint = vehicle.commands.next
        time.sleep(1)

    # wait for the vehicle to land
    while vehicle.commands.next > 0:
        time.sleep(1)


    # Disarm vehicle
    vehicle.armed = False
    time.sleep(1)

    # Close vehicle object before exiting script
    vehicle.close()
    time.sleep(1)

def PX4setMode(mavMode):
    vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component,
                                            mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                                            mavMode,
                                            0, 0, 0, 0, 0, 0)

def get_location_offset_meters(original_location, dNorth, dEast, alt):


    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt+alt)

def get_location_offset_meters_dict(original_location, dNorth, dEast, alt):


    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the
    specified `original_location`. The returned Location adds the entered `alt` value to the altitude of the `original_location`.
    The function is useful when you want to move the vehicle around specifying locations relative to
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location['lat']/180))

    #New position in decimal degrees
    newlat = original_location['lat'] + (dLat * 180/math.pi)
    newlon = original_location['lng'] + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location['alt']+alt)


def servo():
    servo = Servo(15)
    servo.max()
    sleep(1)
    servo.min()
    sleep(1)
    servo.max()
    sleep(1)

def distance():
    print(123);
