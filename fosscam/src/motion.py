#!/usr/bin/env python
import rospy
import urllib2
import time
from std_msgs.msg import Float64MultiArray

def cam_callback(inp):
    if(inp.data[4]==1): 
        urllib2.urlopen("http://192.168.1.183/decoder_control.cgi?command=0&user=martian_eye&pwd=rover2409")
    elif(inp.data[4]==-1):
        urllib2.urlopen("http://192.168.1.183/decoder_control.cgi?command=2&user=martian_eye&pwd=rover2409")
    elif(inp.data[6]==1):
        urllib2.urlopen("http://192.168.1.183/decoder_control.cgi?command=6&user=martian_eye&pwd=rover2409")
    elif(inp.data[6]==-1):
        urllib2.urlopen("http://192.168.1.183/decoder_control.cgi?command=4&user=martian_eye&pwd=rover2409")
    else:
        urllib2.urlopen("http://192.168.1.183/decoder_control.cgi?command=1&user=martian_eye&pwd=rover2409")
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('cam_listener', anonymous=True)
    rospy.Subscriber("/rover/control_directives", Float64MultiArray, cam_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()