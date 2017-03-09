#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import Bool
import math

def talker():
    pub = rospy.Publisher('autonomous_switch', Bool)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(2) 
    i = 0
    while not rospy.is_shutdown():
        if (i%2 == 0):
            hello_str = True
        else:
            hello_str = False
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
        i += 1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass