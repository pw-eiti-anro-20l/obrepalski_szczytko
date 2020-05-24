#!/usr/bin/env python


from lab_4.srv import jint_control
from sensor_msgs.msg import JointState

from time import sleep
from sys import stderr
import rospy

#2 MODES of interpolation

def linear_interpolation(t, x0, x1, time_period):
    return x0 + (x1-x0)*t/time_period

def polynomial_interpolation(t, x0, x1, time_period):
    a = -2*(x1-x0)/(time_period**3)
    b = 3*(x1-x0)/(time_period**2)
    return x0 + b*(t**2) + a*(t**3)

#LIMITS

def limit(joint):
    out = [0.0]*3
    
    if joint[0] > 3.14:
        out[0] = 3.14
        print >> stderr, "Joint1: Theta = 3.14"
    elif joint[0] < -3.14:
        out[0] = -3.14
        print >> stderr, "Joint1: Theta = -3.14"
    else:
        out[0] = joint[0]

    if joint[1] > 3.14:
        out[1] = 3.14
        print >> stderr, "Joint2: Theta = 3.14"
    elif joint[1] < -3.14:
        out[1] = -3.14
        print >> stderr, "Joint2: Theta = -3.14"
    else:
        out[1] = joint[1]

    if joint[2] > 1:
        out[2] = 1
        print >> stderr, "Joint1: d = 1"
    elif joint[2] < -1:
        out[2] = -1
        print >> stderr, "Joint1: d = -1"
    else:
        out[2] = joint[2]

    return out



#HANDLE REQUEST

def handle(req):
    global start
    global pub

    if req.mode == 'poly':
        fun = polynomial_interpolation
    else:
        fun = linear_interpolation

    target = limit([req.joint1, req.joint2, req.joint3])

    if not req.t > 0.0:
        print >> stderr, "Received invalid time value: %s" % req.t
        return "Passed invalid time value: %s. Expected positive float64. Service interrupted!" % req.t

    msg = JointState()

    msg.name = ['joint1', 'joint2', 'joint3']

    t = 0
    rate = rospy.Rate(20)
    while t < req.t:

        msg.header.stamp = rospy.get_rostime()
        joint = [0.0]*3

        joint[0] = fun(t, start[0], target[0], req.t)
        joint[1] = fun(t, start[1], target[1], req.t)
        joint[2] = fun(t, start[2], target[2], req.t)

        msg.position = joint

        pub.publish(msg)

        if req.t - t < 0.05:
            t = req.t
        else:
            t += 0.05
        rate.sleep()

    msg.header.stamp = rospy.get_rostime()
    joint = [0.0]*3

    joint[0] = fun(t, start[0], target[0], req.t)
    joint[1] = fun(t, start[1], target[1], req.t)
    joint[2] = fun(t, start[2], target[2], req.t)

    msg.position = joint

    pub.publish(msg)

    start = joint

    return "%s interpolation completed" % req.mode.capitalize()

def jint():
    global start
    global pub

    start = [0.0]*3
    pub = rospy.Publisher('/joint_states', JointState, queue_size = 1)
    rospy.init_node('jint')
    s = rospy.Service('jint_control_srv', jint_control, handle)
    print "Ready to interpolate."

    rospy.spin()

if __name__ == "__main__":
    jint()
