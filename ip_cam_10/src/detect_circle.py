#!/usr/bin/env python

import cv2,platform
import numpy as np
from sensor_msgs.msg import Image
import roslib
import sys
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from collections import deque
import imutils
import urllib #for reading image from URL
 
 

########################################### ADJUST HSV ########################################

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'colour':(0,210,70)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'colour':(40,255,255)}
 
# define standard colors for circle around the object
colors = {'colour':(0,0,255)}

###############################################################################################

class ipcamera(object):
    def __init__(self, url):
        try:
            self.stream=cv2.VideoCapture(url)
        except:
            rospy.logerr('Unable to open camera stream: ' + str(url))
            sys.exit() #'Unable to open camera stream')
        if not self.stream.isOpened():
            print "Error opening resource: " + str(url)
            print "Maybe opencv VideoCapture can't open it"
            sys.exit()
        #
        print "Correctly opened resource, starting to show feed."
        self.bytes=''
        self.image_pub = rospy.Publisher("ipcam10_vid", Image,queue_size=1000)
        self.bridge = CvBridge()
#	print 0

if __name__ == '__main__':
    try:
        camUrl='rtsp://192.168.0.152:5544/ch0'
        rospy.init_node('ipcam_10', anonymous=True)
        ip_camera = ipcamera(camUrl)
        while not rospy.is_shutdown():
            (rval, frame) = ip_camera.stream.read()
            if rval:
                blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
                #for each color in dictionary check object in frame
                for key, value in upper.items():
                    kernel = np.ones((9,9),np.uint8)
                    mask = cv2.inRange(hsv, lower[key], upper[key])
                    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    center = None
       
                    # only proceed if at least one contour was found
                    if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
       
                        # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                        if radius > 0.5:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                            print(x,y)
                            ''' 
                            -> Figure out a way to put code into separate files
                            -> Make a new file, detect.py 
                            -> Make a launch files for full run and stream run
                            -> Make a publisher of float array (Just search if there's float tuple type as well) type (Someting like node.publish(x,y))
                            -> Update to me
                            -> Ask me for some tutorials 
                            -> Do some corner case testing
                            --- 
                            '''
                            cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                            cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

                ip_camera.image_pub.publish(ip_camera.bridge.cv2_to_imgmsg(frame, "bgr8"))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        ip_camera.stream.release()
        cv2.destroyAllWindows()
    except rospy.ROSInterruptException:
        pass