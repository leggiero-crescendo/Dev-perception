#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)

import rospy # rospy module
# from std_msgs.msg import String # msg 중 string type msg import
from std_msgs.msg import Int32

def callback(msg): # callback 함수 정의
    # print msg.data # msg.data 출력
    pass

rospy.init_node('student') # 함수 초기화

sub = rospy.Subscriber('msg_to_students', Int32, callback) # Subscriber() 토픽의 구독자 ('topic name', data type, 도착시 호출할 함수)

rospy.spin() # shutdown 되기 전 까지 반복 
