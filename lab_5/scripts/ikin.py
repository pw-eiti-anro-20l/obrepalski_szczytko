#!/usr/bin/env python

import json
from collections import OrderedDict
import os
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header, String
from math import atan2, sqrt, pi, acos, sin


def inverse_kinematics(data):

    global pub
    global arm1len
    global arm2len
    global base_hight
    global arm3max
    global arm3min
    global pose_old
    global pose

    msg = JointState()
    msg.name = ['joint1', 'joint2', 'joint3']
    msg.header.stamp = rospy.get_rostime()

    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z
    
    print(x)
    print(y)
    print(z)
    print (arm3min)
    print (arm3max)
    
    
    if x**2+y**2 < (arm1len+arm2len)**2 and x**2+y**2 > (arm1len-arm2len)**2 and z > arm3min and z < arm3max:
        tt = (x ** 2 + y ** 2 - arm1len ** 2 - arm2len ** 2)/(2 * arm1len * arm2len )
        print(tt)
        print("NIBBA")
        pose[1] = acos( tt )
        if abs( pose[1] - pose_old[1] ) > abs( pose[1] + pose_old[1] ):
            pose[1]*=-1
        pose[0] = atan2(-arm2len * sin(pose[1]) * x + (arm1len + arm2len*tt)*y, (arm1len+arm2len*tt)*x+arm2len*sin(pose[1])*y)
        pose[2] = - z + base_hight
    else:
        tt = (x ** 2 + y ** 2 - arm1len ** 2 - arm2len ** 2)/(2 * arm1len * arm2len )
        print(tt)
        print("AAAAAaaaaaaaaa")
    
          
    msg.position = pose
    pub.publish(msg)
    
    pose_old = pose
    
    #pub.publish(str(tt))

def ikin():
    
    #pub = rospy.Publisher('joint_states', JointStates, queue_size=10)
    rospy.init_node('ikin', anonymous=True)
    rospy.Subscriber("/oint_rviz", PoseStamped, inverse_kinematics)
    rospy.spin()

if __name__ == "__main__":

    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    #LOAD PARAMETERS
    arm1len = float(rospy.get_param("i2/l_len"))
    arm2len = float(rospy.get_param("i3/l_len"))
    base_hight = arm1len/2
    arm3max = base_hight*1.2
    arm3min = 0
    pose_old = [0.0]*3
    pose = [0.0]*3
    
    try:
        ikin()
    except rospy.ROSInterruptException:
        pass
