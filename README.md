# Contour-Detection-to-track-tennis-balls-using-ROS-nodes
A contour detection algorithm using CVBridge on ROS-Noetic 

1. Make sure that you have all the necessary libraries such as OpenCV4 etc. installed.
2. If not identify these libraries in the header of the algorithm and pip install these files.
3. Activate the roscore
4. Before running this ROS Script we need to load the ROS camera node using
   rosrun usb_cam usb_cam_node _pixel_format:=yuyv

5. Go inside the workspace, source it and run the script using
   rosrun ball_detection tennis_ball_usb_cam_tracker.py

[![Click to Watch Video](https://img.youtube.com/vi/enYqXHO7T9M/0.jpg)](https://www.youtube.com/watch?v=enYqXHO7T9M)
