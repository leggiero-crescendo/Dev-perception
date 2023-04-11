#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Int32MultiArray
from xycar_msgs.msg import xycar_motor

ultra_msg = None
motor_msg = xycar_motor()

def callback(data):
    global ultra_msg
    ultra_msg = data.data

def drive_go(angle):
    global motor_msg, pub
    motor_msg.speed = -5
    motor_msg.angle = angle
    pub.publish(motor_msg)

def drive_stop():
    global motor_msg, pub
    motor_msg.speed = 0
    motor_msg.angle = 0
    pub.publish(motor_msg)

rospy.init_node("ultra_driver")
rospy.Subscriber("xycar_ultrasonic", Int32MultiArray, callback, queue_size=1)
pub = rospy.Publisher("xycar_motor", xycar_motor, queue_size=1)

time.sleep(2)

# 장애물 인식 거리
CENTER_DECTION_DISTANCE = 10
DIRECTION_DECTION_DISTANCE = 20

# 장애물 정지 거리
CENTER_STOP_DISTANCE = 2
DIRECTION_STOP_DISTANCE = 5

while not rospy.is_shutdown():
    if ultra_msg == None:
        continue

    left, center, right = ultra_msg[-1], ultra_msg[-2], ultra_msg[-3]
    reach_l_dectection, reach_c_dectection, reach_r_detection =\
        left <= DIRECTION_DECTION_DISTANCE,\
        center <= CENTER_DECTION_DISTANCE,\
        right <= DIRECTION_DECTION_DISTANCE
    reach_l_stop, reach_c_stop, reach_r_stop =\
        left <= DIRECTION_STOP_DISTANCE,\
        center <= CENTER_STOP_DISTANCE,\
        right <= DIRECTION_STOP_DISTANCE

    # 정지 거리 범위 안이면 정지
    if reach_l_stop or reach_c_stop or reach_r_stop:
        drive_stop()
    # 왼쪽 혹은 오른쪽 인식
    elif reach_l_dectection or reach_r_detection:
        # 왼쪽 인식
        if reach_l_dectection:
            drive_go(-50)
        # 오른쪽 인식
        elif reach_r_detection:
            drive_go(50)
    # 중앙 인식이 없다면 물체가 없는 것으로 간주하고 직진
    elif reach_c_dectection == False:
        drive_go(0)
    # 이외의 모든 상황은 정지
    else:
        drive_stop()
