import numpy as np
import math
import json
from mr_blue_sky import getAcceleration

class IMU_DATA:
    def __init__(self, gravity, axis):
        self.gravityVector = gravity
        self.refVectors = [axis[0], axis[1]]

imu1_data = imu2_data = holeList = camera_vector = None

def begin(filename):
    global imu1_data, imu2_data, holeList, camera_vector
    data = open_json_file(filename)
    # Initialize holes
    holeList = data["holes"]
    # Intialize camera vector
    camera_vector = data["cameraVec"]
    # Initilize IMUs
    imu1_ref = [np.array(data["imu1"]["refVec1"]), np.array(data["imu1"]["refVec2"])]
    imu2_ref = [np.array(data["imu2"]["refVec1"]), np.array(data["imu2"]["refVec2"])]
    accel = getAcceleration()
    imu1_data = IMU_DATA(np.array(accel[0]),imu1_ref)
    imu2_data = IMU_DATA(np.array(accel[1]),imu2_ref)

def getMainStepperAngle():
    # Project the gravity vector into the plane made by ref_vectors[0] and ref_vectors[1]
    imu1_gravity=projection_on_plane(imu1_data.refVectors[0], imu1_data.refVectors[1], imu1_data.gravityVector)
    imu1_vertical = -1 * imu1_gravity
    vertical_angle = getAngleFromCoordinate(imu1_vertical[0], imu1_vertical[1])
    # Get the hole which is closest to the vertical angle
    imu1_hole_angle = closestAngle(holeList, vertical_angle)
    # Get the angle between the vertical angle and the hole
    return getAngleBetween(imu1_hole_angle, vertical_angle)

def getMicroStepperAngle(traveledAngle):
    # Update imu2's gravity vector
    imu2_data.gravityVector = np.array(getAcceleration()[1])
    # Invert the imu2 gravity vector
    imu2_gravity = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.gravityVector)
    imu2_vertical = -1 * imu2_gravity
    imu2_vertical_angle = getAngleFromCoordinate(imu2_vertical[0], imu2_vertical[1])
    # Add the vertical deviation to the imu2 vertical angle
    imu2_hole_angle = imu2_vertical_angle + traveledAngle
    # The angle between the align vector of imu2 and the hole
    camera_2d = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], camera_vector)
    camera_angle = getAngleFromCoordinate(camera_2d[0], camera_2d[1])
    travel_angle = getAngleBetween(imu2_hole_angle, camera_angle)
    # Return the angle to travel
    return travel_angle

# Checks if the main stepper rotated by correct amount.  Returns how much to correct by in degrees 
def checkMainStepperRotation(traveledAngle):
    beforeRot = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.gravityVector)
    afterRot = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], np.array(getAcceleration()[1]))
    errAmnt = abs(getAngleBetween(afterRot, beforeRot)) - abs(traveledAngle)
    if (abs(errAmnt) <= math.pi/30):
        return 0
    else:
        return errAmnt
    
    
def GetTravelAngle(imu1_data, imu2_data, holeList, camera_vector):
    #Project the gravity vector into the plane made by ref_vectors[0] and ref_vectors[1]
    imu1_gravity=projection_on_plane(imu1_data.refVectors[0], imu1_data.refVectors[1], imu1_data.gravityVector)
    imu1_vertical = -1 * imu1_gravity
    vertical_angle = getAngleFromCoordinate(imu1_vertical[0], imu1_vertical[1])
    #Second get the hole which is closest to the vertical angle
    imu1_hole_angle = closestAngle(holeList, vertical_angle)
    #Third get the angle between the vertical angle and the hole
    vertical_deviation = getAngleBetween(imu1_hole_angle, vertical_angle)
    #Fith invert the imu2 gravity vector
    imu2_gravity = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.gravityVector)
    imu2_vertical = -1 * imu2_gravity
    imu2_vertical_angle = getAngleFromCoordinate(imu2_vertical[0], imu2_vertical[1])
    #Sixth add the vertical deviation to the imu2 vertical angle
    imu2_hole_angle = imu2_vertical_angle + vertical_deviation
    #Get the angle between the align vector of imu2 and the hole
    camera_2d = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], camera_vector)
    camera_angle = getAngleFromCoordinate(camera_2d[0], camera_2d[1])
    travel_angle = getAngleBetween(imu2_hole_angle, camera_angle)
    #Return the angle to travel
    return travel_angle
    
def projection_on_plane(x_axis_vector, y_axis_vector, other_vector):
    #Checking if vectors are perpendicular
    if abs(np.dot(x_axis_vector, y_axis_vector)) > 1e-10:
        raise ValueError("Vectors x_axis_vector and y_axis_vector are not perpendicular")
    #Calculating the normal vector of the plane
    normal_vector = np.cross(x_axis_vector, y_axis_vector)
    #Calculating the projection
    projection = other_vector - (np.dot(other_vector, normal_vector) * normal_vector)
    zero_index = np.where(projection==0)[0]
    #If size is greater than 1, then it's [0,0,0] keep into account for later implementation of Try catches
    projection_2d = np.delete(projection, zero_index[0])
    return projection_2d

def getAngleFromCoordinate(x, y):
    if (x == 0 and y == 0):
        raise Exception("Cannot assign angle to the origin.")
    elif (y == 0):
        return 0 if x > 0 else math.pi
    elif (x == 0):
        return math.pi/2 if y > 0 else 3*math.pi/2

    return math.atan(y/x) % (2*math.pi) if x > 0 else math.atan(y/x) + math.pi

def getAngleBetween(fAngle, iAngle):
    angle = fAngle - iAngle
    if (angle > math.pi):
        angle -= 2*math.pi
    elif (angle < -math.pi):
        angle += 2*math.pi
    
    return angle

def closestAngle(angList, Angle):
    return min(angList, key=lambda x:abs(getAngleBetween(x, Angle)))

def open_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

if __name__=="__main__":
    data=open_json_file("imu_data.json")
    imu1_ref = [np.array([1,0,0]), np.array([0,0,1])]
    imu2_ref = [np.array([0,0,-1]), np.array([0,1,0])]
    imu1_data = IMU_DATA(np.array([-1,0,-1]),imu1_ref)
    imu2_data = IMU_DATA(np.array([0,-1,0]),imu2_ref)
    angle=GetTravelAngle(imu1_data, imu2_data, [math.pi/4,3*math.pi/4, 5*math.pi/4, 7*math.pi/4], np.array([0,-1,0]))
    print(angle*180/math.pi)
