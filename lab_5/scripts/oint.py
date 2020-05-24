#!/usr/bin/env python


from lab_5.srv import oint_control
from geometry_msgs.msg import PoseStamped

from time import sleep
from sys import stderr
from PyKDL import Rotation
import rospy

#2 MODES of interpolation

def linear_interpolation(t, x0, x1, time_period):
    return x0 + (x1-x0)*t/time_period

def polynomial_interpolation(t, x0, x1, time_period):
    a = -2*(x1-x0)/(time_period**3)
    b = 3*(x1-x0)/(time_period**2)
    return x0 + b*(t**2) + a*(t**3)

#HANDLE REQUEST

def handle(req):
    global pose_now
    global pub

    if req.mode == 'poly':
        fun = polynomial_interpolation
    else:
        fun = linear_interpolation

    if not req.t > 0.0:
        print >> stderr, "Received invalid time value: %s" % req.t
        return "time is not correct"

    msg = PoseStamped()
    msg.header.frame_id = 'base_link'

    t = 0
    rate = rospy.Rate(20)
    while t < req.t:

        msg.header.stamp = rospy.get_rostime()
        
        msg.pose.position.x = fun( t, pose_now[0], req.x, req.t )
        msg.pose.position.y = fun( t, pose_now[1], req.y, req.t )
        msg.pose.position.z = fun( t, pose_now[2], req.z, req.t )

        roll  = fun( t, pose_now[3], req.roll , req.t )
        pitch = fun( t, pose_now[4], req.pitch, req.t )
        yaw   = fun( t, pose_now[5], req.yaw  , req.t )

        rot = Rotation.RPY(roll,pitch,yaw)
        quat = rot.GetQuaternion()

        msg.pose.orientation.x = quat[0]
        msg.pose.orientation.y = quat[1]
        msg.pose.orientation.z = quat[2]
        msg.pose.orientation.w = quat[3]

        pub.publish(msg)

        if req.t - t < 0.05:
            t = req.t
        else:
            t += 0.05
        rate.sleep()

    msg.header.stamp = rospy.get_rostime()
        
    msg.pose.position.x = fun( t, pose_now[0], req.x, req.t )
    msg.pose.position.y = fun( t, pose_now[1], req.y, req.t )
    msg.pose.position.z = fun( t, pose_now[2], req.z, req.t )

    roll  = fun( t, pose_now[3], req.roll , req.t )
    pitch  = fun( t, pose_now[4], req.pitch , req.t )
    yaw  = fun( t, pose_now[5], req.yaw , req.t )

    rot = Rotation.RPY(roll,pitch,yaw)
    quat = rot.GetQuaternion()

    msg.pose.orientation.x = quat[0]
    msg.pose.orientation.y = quat[1]
    msg.pose.orientation.z = quat[2]
    msg.pose.orientation.w = quat[3]

    pub.publish(msg)

    pose_now[0] = msg.pose.position.x
    pose_now[1] = msg.pose.position.y
    pose_now[2] = msg.pose.position.z
    pose_now[3] = roll
    pose_now[4] = pitch
    pose_now[5] = yaw

    return "Done"

def oint():
    global pose_now
    global pub

    pose_now = [3.0, 0.0, 0.5, 0.0, 0.0, 0.0]
    pub = rospy.Publisher('/oint_rviz', PoseStamped, queue_size = 1)
    rospy.init_node('oint')
    s = rospy.Service('oint_control_srv', oint_control, handle)
    print "Ready"

    rospy.spin()

if __name__ == "__main__":
    oint()
