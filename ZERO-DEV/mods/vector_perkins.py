import numpy as np
import math
import json
class IMU_DATA:
    def __init__(self, axis):
        self.refVectors = [axis[0], axis[1]]

    #thorugh the program we will be updating the gravity vector
    def setGravity(self, gravity):
        self.gravityVector = np.array(gravity)
    
global imu2_data, imu1_data, camera_vector, holeList
imu1_data: IMU_DATA
imu2_data: IMU_DATA

def GetTravelAngle():
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
    print(f'normal type:{type(normal_vector)}')
    dot = np.dot(other_vector, normal_vector)
    print(f'Dot type:{type(dot)}')
    projection = other_vector - (dot * normal_vector)
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

#Create IMU data objects with the reference vectors
def LoadVectorProfile():
    global imu1_data, imu2_data, camera_vector, holeList
    data=open_json_file("imu_data.json")
    imu1_ref = [np.array(data["imu1"]["refVec1"]), np.array(data["imu1"]["refVec2"])]
    imu2_ref = [np.array(data["imu2"]["refVec1"]), np.array(data["imu2"]["refVec2"])]
    #imu1_ref = [np.array([1,0,0]), np.array([0,0,1])]
    #imu2_ref = [np.array([0,0,-1]), np.array([0,1,0])]
    imu1_data = IMU_DATA(imu1_ref)
    imu2_data = IMU_DATA(imu2_ref)
    # Load camera vector
    camera_vector = np.array(data["cameraVec"])
    # Load holes
    holeList = np.deg2rad(np.array(data["holes"]))

if __name__=="__main__":
    LoadVectorProfile()
    #In actual program we will be updating the gravity vector with IMU sensor data
    gravity1 = [-1.009, 0, -1]
    gravity2 = [0, -1.9908, 0]
    imu1_data.setGravity(gravity1)
    imu2_data.setGravity(gravity2)
    #In actual program this will run periodically
    angle=GetTravelAngle()
    print(angle*180/math.pi)
