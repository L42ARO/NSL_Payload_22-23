'''NOTE: Bug found, if imu2 is placed with it's Z axis facing up, the angle will be wrong
        - Findings so far: there seems to be something messing up when getting the imu2 vertical angle
        - Alternatively something is being messed up when adding the vertical deviation to the imu2 vertical angle
'''
import os
import numpy as np
import math
import json

class IMU_DATA:
    def __init__(self, axis):
        self.refVectors = [axis[0], axis[1]]

    #thorugh the program we will be updating the gravity vector
    def setGravity(self, gravity):
        self.gravityVector = np.array(gravity)

class SERVO_DATA:
    def __init__(self, axis):
        self.refVectors = [axis[0], axis[1]]

global imu2_data, imu1_data, camera_vector, servo_data,  holeList
imu1_data: IMU_DATA
imu2_data: IMU_DATA
servo_data: SERVO_DATA


#Important: Positive Angle Means counterclockwise viewed from the Front Endcap of the Stepper Motor
def GetTravelAngle():
    #Project the gravity vector into the plane made by ref_vectors[0] and ref_vectors[1]
    imu1_gravity=projection_on_plane(imu1_data.refVectors[0], imu1_data.refVectors[1], imu1_data.gravityVector)
    ref1 = projection_on_plane(imu1_data.refVectors[0], imu1_data.refVectors[1], imu1_data.refVectors[0])
    ref2 = projection_on_plane(imu1_data.refVectors[0], imu1_data.refVectors[1], imu1_data.refVectors[1])
    imu1_gravity = changeCoordSystem(imu1_gravity,ref1, ref2)
    imu1_vertical = -1 * imu1_gravity
    vertical_angle = getAngleFromCoordinate(imu1_vertical[0], imu1_vertical[1])
    #Second get the hole which is closest to the vertical angle
    imu1_hole_angle = closestAngle(holeList, vertical_angle)
    #Third get the angle between the vertical angle and the hole
    vertical_deviation = getAngleBetween(vertical_angle, imu1_hole_angle)
    #Fith invert the imu2 gravity vector
    imu2_gravity = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.gravityVector)
    ref1 = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.refVectors[0])
    ref2= projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], imu2_data.refVectors[1])
    imu2_gravity = changeCoordSystem(imu2_gravity, ref1, ref2)
    imu2_vertical = -1 * imu2_gravity
    imu2_vertical_angle = getAngleFromCoordinate(imu2_vertical[0], imu2_vertical[1])
    #Sixth add the vertical deviation to the imu2 vertical angle
    imu2_hole_angle = add2Angles(imu2_vertical_angle ,vertical_deviation)
    #Get the angle between the align vector of imu2 and the hole
    camera_2d = projection_on_plane(imu2_data.refVectors[0], imu2_data.refVectors[1], camera_vector)
    camera_2d = changeCoordSystem(camera_2d, ref1, ref2)
    camera_angle = getAngleFromCoordinate(camera_2d[0], camera_2d[1])
    travel_angle = getAngleBetween(camera_angle, imu2_hole_angle)
    #Return the angle to travel
    return travel_angle, imu1_hole_angle

def GetGimbalTravelAngle(startAngle):
    #Get vertical angle to align IMU, use servo data as reference plane
    imu2_gravity = projection_on_plane(servo_data.refVectors[0], servo_data.refVectors[1], imu2_data.gravityVector)
    ref1 = projection_on_plane(servo_data.refVectors[0], servo_data.refVectors[1], servo_data.refVectors[0])
    ref2 = projection_on_plane(servo_data.refVectors[0], servo_data.refVectors[1], servo_data.refVectors[1])
    imu2_gravity = changeCoordSystem(imu2_gravity, ref1, ref2)
    imu2_vertical = -1 * imu2_gravity
    imu2_vertical_angle = getAngleFromCoordinate(imu2_vertical[0], imu2_vertical[1])
    #Gimbal angle is the angle between the vertical angle and the start angle
    gimbal_angle = getAngleBetween(startAngle, imu2_vertical_angle)
    print(f'----- Gimbal Angle: {gimbal_angle*180/math.pi}')
    return gimbal_angle
def changeCoordSystem(vector, newX, newY):
    A = np.array([newX, newY])
    xy_vec = np.array(vector)
    uv_vec = np.dot(A, xy_vec)
    return uv_vec
def add2Angles(angle1, angle2):
    res = angle1 + angle2
    #Check if it goes above 2pi
    if(res > 2*math.pi):
        res -= 2*math.pi
    #Check if it goes below 0
    elif(res < 0):
        res += 2*math.pi #res is already negative, so it's like subtracting to 360deg
    return res
    
def projection_on_plane(x_axis_vector, y_axis_vector, other_vector):
    #Checking if vectors are perpendicular
    if abs(np.dot(x_axis_vector, y_axis_vector)) > 1e-10:
        raise ValueError("Vectors x_axis_vector and y_axis_vector are not perpendicular")
    #Calculating the normal vector of the plane
    normal_vector = np.cross(x_axis_vector, y_axis_vector)
    #IMU uses Left Hand Rule for gravity vector, so we need to invert the normal vector
    normal_vector *= -1
    #Calculating the projection
    dot = np.dot(other_vector, normal_vector)
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

def getAngleBetween(iAngle, fAngle):
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
    global imu1_data, imu2_data, camera_vector, holeList, servo_data
    file_path = "imu_data.json"
    if not (os.path.basename(os.getcwd()) == 'mods'):
        file_path = os.path.join('mods', 'imu_data.json')
    data=open_json_file(file_path)
    imu1_ref = [np.array(data["imu1"]["refVec1"]), np.array(data["imu1"]["refVec2"])]
    imu2_ref = [np.array(data["imu2"]["refVec1"]), np.array(data["imu2"]["refVec2"])]
    #imu1_ref = [np.array([1,0,0]), np.array([0,0,1])]
    #imu2_ref = [np.array([0,0,-1]), np.array([0,1,0])]
    imu1_data = IMU_DATA(imu1_ref)
    imu2_data = IMU_DATA(imu2_ref)
    # Load camera vector
    camera_vector = np.array(data["cameraVec"])

    #Load Servo data
    servo_ref = [np.array(data["servo"]["refVec1"]), np.array(data["servo"]["refVec2"])]
    servo_data = SERVO_DATA(servo_ref)
    # Load holes
    holeList = np.deg2rad(np.array(data["holes"]))

if __name__=="__main__":
    print(getAngleFromCoordinate(2.83,-8.52)*180/math.pi)
    LoadVectorProfile()
    #In actual program we will be updating the gravity vector with IMU sensor data
    #gravity1 = [3.14, 3.48, -8.540000000000001]
    #gravity2 = [-3.22, 2.83,-8.52]
    gravity1 = [2.86, 3.89, -8.48]
    gravity2 = [-3.6, 1.19, -9.07]
    imu1_data.setGravity(gravity1)
    imu2_data.setGravity(gravity2)
    #In actual program this will run periodically
    angle, hole=GetTravelAngle()
    print(f'Choseon hole: {hole*180/math.pi}')
    print(f'Angle to travel: {angle*180/math.pi}')
