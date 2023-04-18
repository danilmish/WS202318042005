import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from sensor_msgs.msg import Range
from cv_bridge import CvBridge
import numpy as np #
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect
import cv2 #pip install opencv-contrib-python --upgrade 


bridge = CvBridge()

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)  # define proxy to ROS-service


def navigate_wait(x=0, y=0, z=1.5, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        telem1 = get_telemetry()
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            rospy.sleep(3)
            print("COORD X {}, COORD Y {}".format(telem1.x, telem1.y))
            print("DETECTED COLOR: ", color)
            break
        rospy.sleep(0.2)


color="error"
def color_call(data):
    global color
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    img_hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)[119:120, 159:160]
    #print(img_hsv[119][159])

    red_low_value = (0, 150, 200)
    red_high_value = (10, 255, 255)

    red_final = cv2.inRange(img_hsv, red_low_value, red_high_value)

    if red_final[0][0] == 255:
        color = "red"
    else:
        color = "error"


image_sub = rospy.Subscriber("main_camera/image_raw", Image, color_call)

def main():
    navigate_wait(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
    navigate_wait(x=0, y=3, frame_id='aruco_map')
    navigate_wait(x=3, y=0, frame_id='aruco_map')



    land()


if __name__ == "__main__":
    main()



