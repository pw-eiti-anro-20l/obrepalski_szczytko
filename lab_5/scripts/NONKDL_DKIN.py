#!/usr/bin/env python

import rospy
import json
import os
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
from nav_msgs.msg import Path
import copy
#from std_msgs.msg import String

path = Path()

def callback(data):
    
    
    xaxis = (1,0,0)
#  yaxis = (0,1,0)
    zaxis = (0,0,1)
    
    
    #ARM 1    
    a, d, al, th = dh['i1']
    a, d, al, th = float(a), float(d), float(al), float(th)
    
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[0], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(al, xaxis)
    T1 = concatenate_matrices(rx, tx, rz, tz)

    #ARM 2
    a, d, al, th = dh['i2']
    a, d, al, th = float(a), float(d), float(al), float(th)
    
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[1], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(al, xaxis)
    T2 = concatenate_matrices(rx, tx, rz, tz)
    
    #ARM 3
    a, d, al, th = dh['i3']
    a, d, al, th = float(a), float(d), float(al), float(th)
    
    tz = translation_matrix((0, 0, data.position[2]-d))
    rz = rotation_matrix(th, zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(al, xaxis)
    T3 = concatenate_matrices(rx, tx, rz, tz)
    
    #FINAL
    final_matrix = concatenate_matrices(T1, T2, T3)
    x, y, z = translation_from_matrix(final_matrix)
    qx, qy, qz, qw = quaternion_from_matrix(final_matrix)
    
    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z+baseHeight
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw
    pubP.publish(pose)


    #path.header.stamp = rospy.Time.now()
    #path.header.frame_id = 'base_link'  
    				#msg.poses.append(data.pose)
    



    
    marker = Marker()
    marker.header.frame_id = 'base_link'
    path.header.frame_id = 'base_link'
    marker.header.stamp = rospy.Time.now()
    path.header.stamp = rospy.Time.now()
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z+baseHeight
    marker.pose.orientation.x = qx
    marker.pose.orientation.y = qy
    marker.pose.orientation.z = qz
    marker.pose.orientation.w = qw
    marker.color.a = 0.5
    marker.color.r = 0.5
    marker.color.g = 0.5
    marker.color.b = 0
    path.poses.append(pose)
    pubM.publish(marker)
    pubH.publish(path)
    
    #SHOW MATRIX
    print("T1:")
    print(T1)
    print("T2:")
    print(T2)
    print("T3:")
    print(T3)
    print("FINAL:")
    print(final_matrix)
    
if __name__ == '__main__':

    baseHeight = rospy.get_param("i2/l_len")
    baseHeight = float(baseHeight)/2

    rospy.init_node('NONKDL_DKIN', anonymous=True)
    dh = {}

    
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
        dh = json.loads(file.read())


    pubP = rospy.Publisher('NONKDL_pose', PoseStamped, queue_size=10)
    pubM = rospy.Publisher('NONKDL_visual', Marker, queue_size=10)
    pubH = rospy.Publisher('path', Path, queue_size=10)
    
    rospy.Subscriber('joint_states',  JointState, callback)
    

    rospy.spin()
