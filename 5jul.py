import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from mavros_msgs.msg import Altitude
from sensor_msgs.msg import Range

rospy.init_node('flight')

navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
land = rospy.ServiceProxy('land', Trigger)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)




def navigate1(x=0, y=0, z=1, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    
    
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance: 
            break
        rospy.sleep(0.2)
    rospy.sleep(0.5)



def land_wait():
    hh = 1
    
    while hh>0.15:
        print("Going to ground")
        navigate (z=hh, frame_id="aruco_70", speed = 1)
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < 0.2: 
            hh = hh - 0.1
            range = Range()
            high = range.range
        else:
            pass
        rospy.sleep(1)
    land()
    


navigate1 (z=1, frame_id="body", auto_arm = True)
navigate1 (frame_id="aruco_70")

land_wait()