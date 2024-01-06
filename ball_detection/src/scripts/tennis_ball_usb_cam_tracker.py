#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()

def filter_color(rgb_image, lower_bound_color, upper_bound_color):
    # Convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)

    # Define a mask using the lower and upper bounds of the color
    mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)

    return mask

def getContours(binary_image):      
    # _, contours, hierarchy = cv2.findContours(binary_image.copy(), 
    #                                           cv2.RETR_EXTERNAL,
    #                                           cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    return contours

def draw_ball_contour(rgb_image, contours):
    black_image = np.zeros_like(rgb_image)

    for c in contours:
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if area > 100:
            cv2.drawContours(rgb_image, [c], -1, (150, 250, 150), 1)
            cv2.drawContours(black_image, [c], -1, (150, 250, 150), 1)
            cx, cy = get_contour_center(c)
            cv2.circle(rgb_image, (cx, cy), int(radius), (0, 0, 255), 1)
            cv2.circle(black_image, (cx, cy), int(radius), (0, 0, 255), 1)
            cv2.circle(black_image, (cx, cy), 5, (150, 150, 255), -1)
            print("Area: {}, Perimeter: {}".format(area, perimeter))
    
    print("Number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours", rgb_image)
    cv2.imshow("Black Image Contours", black_image)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    return cx, cy

def image_callback(ros_image):
    print("Got an image")
    global bridge

    try:
        cv_image = bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
        print(e)

    yellow_lower = (30, 110, 100)
    yellow_upper = (50, 255, 255)

    binary_image_mask = filter_color(cv_image, yellow_lower, yellow_upper)
    contours = getContours(binary_image_mask)
    draw_ball_contour(cv_image, contours)

    cv2.waitKey(1)

def main(args):
    rospy.init_node('tennis_ball_usb_cam_tracker', anonymous=True)

    image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)  
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
