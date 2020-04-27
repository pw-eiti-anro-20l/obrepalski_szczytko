#! /usr/bin/python

import rospy
import json
import os
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

xaxis= (1,0,0)
zaxis= (0,0,1)

def forward_kinematics(data):

#NOKDL
    result_matrix=translation_matrix((0,0,0))

    a, d, alpha, th = params['i1']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[0], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T1 = concatenate_matrices(rx, tx, rz, tz)

    a, d, alpha, th = params['i2']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, d))
    rz = rotation_matrix(data.position[1], zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T2 = concatenate_matrices(rx, tx, rz, tz)

    a, d, alpha, th = params['i3']
    alpha, a, d, th = float(alpha), float(a), float(d), float(th)
    tz = translation_matrix((0, 0, data.position[2]-d))
    rz = rotation_matrix(th, zaxis)
    tx = translation_matrix((a, 0, 0))
    rx = rotation_matrix(alpha, xaxis)
    T3 = concatenate_matrices(rx, tx, rz, tz)

    result_matrix = concatenate_matrices(T1, T2, T3)
    x, y, z = translation_from_matrix(result_matrix)
    qx, qy, qz, qw = quaternion_from_matrix(result_matrix)
    

    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw
    pub.publish(pose)

    marker = Marker()
    marker.header.frame_id = 'base_link'
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.pose.orientation.w = 1

    time = rospy.Duration()
    marker.lifetime = time
    marker.scale.x = 0.09
    marker.scale.y = 0.09
    marker.scale.z = 0.09
    marker.pose.position.x = x;
    marker.pose.position.y = y;
    marker.pose.position.z = z;
    marker.pose.orientation.x = qx;
    marker.pose.orientation.y = qy;
    marker.pose.orientation.z = qz;
    marker.pose.orientation.w = qw;
    marker.color.a = 0.7
    marker.color.r = 0.5
    marker.color.g = 0.0
    marker.color.b = 0.6
    marker_pub.publish(marker)

if __name__ == '__main__':
    rospy.init_node('NONKDL_KIN', anonymous=True)
    params = {}

    with open(os.path.dirname(os.path.realpath(__file__)) + '/../yaml/dh.json', 'r') as file:
        params = json.loads(file.read())


    pub = rospy.Publisher('nkdl_pose', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('nkdl_visual', Marker, queue_size=100)

    rospy.Subscriber('joint_states', JointState, forward_kinematics)


    rospy.spin()