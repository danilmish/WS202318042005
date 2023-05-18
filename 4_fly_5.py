#импорт необходимых модулей и библиотек
import rospy
import math
import cv2 as cv
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover.srv import SetLEDEffect


#инициализация ноды (программы)
rospy.init_node('flight')

#инициализация используемых сервисов 
bridge = CvBridge()
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

#создание топика для просмотра распознанного изображения
color_debug = rospy.Publisher("/color_debug", Image)
#rosrun image_view video_recorder image:=/main_camera/image_raw
#rosbag record /main_camera/image_raw
#объявление процедуры check_temp, при вызове которой будет распознавание цветов
def check_temp():

    #создание переменной frame, где будет 
    frame = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')[80:160, 100:220]
    # vvod na ekran
    print(frame)

   #задание для каждого цвета диапазона в кодировке BGR. В результате в каждую из переменных запишется бинарное представление цвета (0 - если цвет не попадет в диапазон и 255 - если попадает). Это бинарное представление представлено в виде матрицы.
    red = cv.inRange(frame, (120, 135, 159), (126, 145, 164))
    reds = cv.inRange(frame, (20, 20, 200), (90, 90, 240))
    blue = cv.inRange(frame, (200, 70, 60), (205, 73, 64))
    green = cv.inRange(frame, (20, 108, 0), (81, 181, 40))
    yellow = cv.inRange(frame, (0, 220, 220), (20, 255, 255))
    yellows = cv.inRange(frame, (0, 240, 254), (0, 243, 255))

    #зададим словарь color, где запишем для каждого ключа 'r', 'b', 'g' значения из бинарной матрицы только не нулевые значения
    color = {'r': cv.countNonZero(red),
             'r1': cv.countNonZero(reds),
             'b': cv.countNonZero(blue),
             'g': cv.countNonZero(green),
             'y': cv.countNonZero(yellow),
             'y1': cv.countNonZero(yellows)}
    
    #публикация топика для просмотра распознанного изображения
    color_debug.publish(bridge.cv2_to_imgmsg(frame, 'bgr8')) 

    if max(color, key=color.get) == 'r':
        navigate(frame_id = 'body', x=0, y=0, z=0.5)
        rospy.sleep(5)
        print('Red_rectangle')
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(7.5, 1.5) - rectangle - red\n')
        f.close 
        set_effect(r = 255, g = 0, b = 0)
        rospy.sleep(5)


    elif max(color, key=color.get) == 'r1':
        print('Red_star')
        navigate(frame_id = 'body', x=0, y=0, z=0.5)
        rospy.sleep(5)
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(8.5, 0.5) - star - red\n')
        f.close
        set_effect(r = 255, g = 0, b = 0)
        rospy.sleep(5)
        land()
        rospy.sleep(5)
        navigate(x=0, y=0, z=1, frame_id = 'body', auto_arm = True)
        rospy.sleep(5)

    elif max(color, key=color.get) == 'b':
        print('Blue_arrow')
        navigate(frame_id = 'body', x=0, y=0, z=1)
        rospy.sleep(5)
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(6.5, 1) - arrow - blue\n')
        f.close
        set_effect(r = 0, g = 0, b = 255)
        rospy.sleep(5)
        navigate(frame_id = 'aruco_99', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_69', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_65', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_95', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_99', x=0, y=0, z=1)
        rospy.sleep(10)

    elif max(color, key=color.get) == 'y':
        print('Yellow_arrow')
        navigate(frame_id = 'body', x=0, y=0, z=1)
        rospy.sleep(5)
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(5.5, 1.5) - arrow - yellow\n')
        f.close
        set_effect(r = 255, g = 255, b = 0)
        rospy.sleep(5)
        navigate(frame_id = 'aruco_99', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_69', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_65', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_95', x=0, y=0, z=1)
        rospy.sleep(10)
        navigate(frame_id = 'aruco_99', x=0, y=0, z=1)
        rospy.sleep(10)

    elif max(color, key=color.get) == 'y1':
        print('Yellow_rectangle')
        navigate(frame_id = 'aruco_76', x=0.5, y=0.5, z=1)
        rospy.sleep(10)
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(6.5, 2.5) - rectangle - yellow\n')
        f.close
        set_effect(r = 255, g = 255, b = 0)
        rospy.sleep(5)

    elif max(color, key=color.get) == 'g':
        print('Green_square')
        navigate(frame_id = 'body', x=0, y=0, z=1)
        rospy.sleep(10)
        f = open('/home/clover/Desktop/Module_3_P_M/3_report_fly_P_M.txt', 'a')
        f.write('(8.5, 2.5) - square - green\n')
        f.close
        set_effect(r = 0, g = 128, b = 0)
        rospy.sleep(5)
        navigate(yaw=math.radians(-90), frame_id='body')
        rospy.sleep(5)
        navigate(yaw=math.radians(-90), frame_id='body')
        rospy.sleep(5)
        navigate(yaw=math.radians(-90), frame_id='body')
        rospy.sleep(5)
        navigate(yaw=math.radians(-90), frame_id='body')
        rospy.sleep(5)
        
    else:
        print('ne polychilos')
        navigate(frame_id = 'body', x=0, y=0, z=1)
        rospy.sleep(5)
        navigate(frame_id = 'aruco_90', x=0, y=0, z=1)
        rospy.sleep(5)

navigate(x=0, y=0, z=1, frame_id = 'body', auto_arm = True)
rospy.sleep(5)
navigate(frame_id = 'aruco_85', x=0.5, y=0.5, z=1)
rospy.sleep(15)
navigate(frame_id = 'aruco_85', x=0.5, y=0.5, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)

navigate(frame_id = 'aruco_86', x=0.5, y=0, z=1)
rospy.sleep(10)
navigate(frame_id = 'aruco_86', x=0.5, y=0, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)

navigate(frame_id = 'aruco_87', x=0.5, y=0.5, z=1)
rospy.sleep(10)
navigate(frame_id = 'aruco_87', x=0.5, y=0.5, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)

navigate(frame_id = 'aruco_76', x=0.5, y=0.5, z=1)
rospy.sleep(10)
navigate(frame_id = 'aruco_76', x=0.5, y=0.5, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)

navigate(frame_id = 'aruco_78', x=0.5, y=0.5, z=1)
rospy.sleep(10)
navigate(frame_id = 'aruco_78', x=0.5, y=0.5, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)

navigate(frame_id = 'aruco_98', x=0.5, y=0.5, z=1)
rospy.sleep(10)
navigate(frame_id = 'aruco_98', x=0.5, y=0.5, z=0)
rospy.sleep(5)
check_temp()
rospy.sleep(5)
navigate(frame_id = 'aruco_90', x=0, y=0, z=1)
rospy.sleep(20)
land()