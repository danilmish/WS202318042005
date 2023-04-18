import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from sensor_msgs.msg import Range
from cv_bridge import CvBridge
from pyzbar import pyzbar
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect

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
            print("Z height = {}".format(z_dist))
            print("COORD X {}, COORD Y {}".format(telem1.x, telem1.y))

            break
        rospy.sleep(0.2)


z_dist = 0
def range_callback(msg):
    global z_dist
    z_dist = msg.range


qr= ""

def image_call(data):
    global qr
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
    barcodes = pyzbar.decode(cv_image)
    for barcode in barcodes:
        qr = barcode.data.decode("utf-8")
        print("QR = ", qr)
    
image_sub = rospy.Subscriber("main_camera/image_raw", Image, image_call, queue_size=1)

rospy.Subscriber("rangefinder/range", Range, range_callback)

def main():
    navigate_wait(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
    navigate_wait(x=0, y=3, frame_id='aruco_map')
    navigate_wait(x=3, y=0, frame_id='aruco_map')

    while qr == "" and not rospy.is_shutdown():
        rospy.sleep(0.4)
    
    QR_detected = qr.split()
    color = list(map(str.QR_detected))
    for i in range(len(color)):
        if color[i] == "red":
            set_effect(r=255, g =0, b=0)
        else:
            pass
        rospy.sleep(3)

    land()


if __name__ == "__main__":
    main()



