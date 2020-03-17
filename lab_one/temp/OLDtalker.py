#!/usr/bin/env python

import rospy

from rospy import Publisher
from rospy import ROSInterruptException
from rospy import init_node
from rospy import Rate
from rospy import is_shutdown
from geometry_msgs.msg import Twist
from std_msgs.msg import String

import sys, select, termios, tty




def get_move():
    key = screen.getch()
   # key = raw_input('')
    twist = Twist()
    if key == 'w':
        twist.linear.x = 2.0
        return twist
    if key == 's':
        twist.linear.x = -2.0
        return twist
    if key == 'a':
        twist.angular.z = 2.0
        return twist
    if key == 'd':
        twist.angular.z = -2.0
        return twist
    return None


def do_sample():
    pub = Publisher('/turtlesim/turtle1/cmd_vel', Twist, queue_size=10)
    init_node('talker', anonymous=True)
    rate = Rate(10)
    while not is_shutdown():
        move = get_move()
        if move is not None:
            pub.publish(move)
        rate.sleep()


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        do_sample()
    except ROSInterruptException:
        pass
