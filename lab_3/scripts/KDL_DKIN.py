#!/usr/bin/env python

import rospy
import json
import os
import PyKDL as kdl
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
#from std_msgs.msg import String

def callback(data):
    
    kdl_chain = kdl.Chain()
    kdl_frame = kdl.Frame()

    frame0 = kdl_frame.DH(0, 0, 0, 0)
    joint0 = kdl.Joint(kdl.Joint.None)
    kdl_chain.addSegment(kdl.Segment(joint0, frame0))

    a, d, alfa, theta = dh['i2']
    frame1 = kdl_frame.DH(a, alfa, d, theta)
    joint1 = kdl.Joint(kdl.Joint.RotZ)
    kdl_chain.addSegment(kdl.Segment(joint1, frame1))

    a, d, alfa, theta = dh['i1']
    frame2 = kdl_frame.DH(a, alfa, d, theta)
    joint2 = kdl.Joint(kdl.Joint.RotZ)
    kdl_chain.addSegment(kdl.Segment(joint2, frame2))

    a, d, alfa, theta = dh['i3']
    frame3 = kdl_frame.DH(a, alfa, d, theta)
    joint3 = kdl.Joint(kdl.Joint.TransZ)
    kdl_chain.addSegment(kdl.Segment(joint3, frame3))

    joint_angles = kdl.JntArray(kdl_chain.getNrOfJoints())
    joint_angles[0] = data.position[0]
    joint_angles[1] = data.position[1]
    joint_angles[2] = -data.position[2]
    
    kdl_chain_t = kdl.ChainFkSolverPos_recursive(kdl_chain)
    frame_t = kdl.Frame()
    kdl_chain_t.JntToCart(joint_angles, frame_t)
    quat = frame_t.M.GetQuaternion()

    pose = PoseStamped()
    pose.header.frame_id = 'BASE'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = frame_t.p[0]
    pose.pose.position.y = frame_t.p[1]
    pose.pose.position.z = frame_t.p[2]+baseHeight
    pose.pose.orientation.x = quat[0]
    pose.pose.orientation.y = quat[1]
    pose.pose.orientation.z = quat[2]
    pose.pose.orientation.w = quat[3]
    pubP.publish(pose)

    marker = Marker()
    marker.header.frame_id = 'BASE'
    marker.header.stamp = rospy.Time.now()
    marker.type = marker.CUBE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    marker.pose.position.x = frame_t.p[0]
    marker.pose.position.y = frame_t.p[1]
    marker.pose.position.z = frame_t.p[2]+baseHeight
    marker.pose.orientation.x = quat[0]
    marker.pose.orientation.y = quat[1]
    marker.pose.orientation.z = quat[2]
    marker.pose.orientation.w = quat[3]
    marker.color.a = 0.5
    marker.color.r = 0.5
    marker.color.g = 0.4
    marker.color.b = 1
    pubM.publish(marker)
    
if __name__ == '__main__':

    baseHeight = rospy.get_param("i2/l_len")
    baseHeight = float(baseHeight)/2

    rospy.init_node('KDL_DKIN', anonymous=True)
    dh = {}

    
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
        dh = json.loads(file.read())


    pubP = rospy.Publisher('KDL_pose', PoseStamped, queue_size=10)
    pubM = rospy.Publisher('KDL_visual', Marker, queue_size=100)
    
    rospy.Subscriber('joint_states',  JointState, callback)
    

    rospy.spin()
