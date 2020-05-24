#!/usr/bin/env python

from lab_5.srv import ocmd_control, oint_control
from sensor_msgs.msg import JointState

from time import sleep
from sys import stderr
import rospy

#HANDLE REQUEST
def handle(req):
    if req.mode == 'square':
        A=[req.x-req.a/2,req.y-req.b/2,req.z]
        B=[req.x+req.a/2,req.y-req.b/2,req.z]
        C=[req.x+req.a/2,req.y+req.b/2,req.z]
        D=[req.x-req.a/2,req.y+req.b/2,req.z]
        T=2
        try:
            rospy.wait_for_service('oint_control_srv')
            make_square = rospy.ServiceProxy('oint_control_srv', oint_control)
            task=make_square('poly',A[0],A[1],A[2],0,0,0,T)
            n=0
            while n < req.t:  
                task=make_square('lin',B[0],B[1],B[2],0,0,0,T)
                task=make_square('lin',C[0],C[1],C[2],0,0,0,T)
                task=make_square('lin',D[0],D[1],D[2],0,0,0,T)
                task=make_square('lin',A[0],A[1],A[2],0,0,0,T)
                n+=1
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            
            
            
            
    elif req.mode == 'elipse':
        print('Elipse')
    else:
        print('Type \'square\' or \'elipse\'')
        return "Type \'square\' or \'elipse\' \'a\' \'b\' \'x\' \'y\' \'z\' \'t\'"
        
    return "%s test completed" % req.mode.capitalize()

def jint():
    rospy.init_node('ocmd')
    s = rospy.Service('ocmd_control_srv', ocmd_control, handle)

    rospy.spin()

if __name__ == "__main__":
    jint()
