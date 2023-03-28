#!/usr/bin/env python
#-*- coding: utf-8-*-
import rospy
from turtlesim.msg import Pose

def callback(data):
	s = "Location: %.2f, %.2f" % (data.x, data.y)
	rospy.loginfo(rospy.get_caller_id())# + s)

rospy.init_node("listener", anonymous=True) # node 생성
rospy.Subscriber("/turtle1/pose", Pose, callback) # subscriber 객체 생성 (메세지를 수신하면 callback이라는 함수가 호출)
rospy.spin() #