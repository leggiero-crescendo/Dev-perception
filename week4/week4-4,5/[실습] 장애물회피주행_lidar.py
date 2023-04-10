#!/usr/bin/env python
#-*- coding: utf-8-*-
import rospy, time
import numpy as np
import math
from sensor_msgs.msg import LaserScan
from xycar_motor.msg import xycar_motor

motor_msg = xycar_motor() # 라이다 거리정보를 담을 저장공간준비
distance = []

value = 3
lmin_check = 60  # 42 deg
lmax_check = 100 # 71 deg
rmin_check = 400 # 285 deg 
rmax_check = 440 # 313 deg
cmin_check, cmax_check = 7, 498 # 0 ~ 5 deg / 360 ~ 355 deg



def angle2ind(angle):
    return round(((angle - 0) / 360) * 505)

def ind2angle(index):
	result = (((index* 360) / 505) )
	return result


def callback(data): # 라이다 토픽이 들어오면 실행되는 콜백
	global distance, motor_msg
	distance = data.ranges
	# print len(data.ranges)

def drive_go(angle, speed):
	global motor_msg
	motor_msg.speed = int(speed)
	motor_msg.angle = int(angle)
	pub.publish(motor_msg)

def drive_back():
	global motor_msg
	motor_msg.speed = -5
	motor_msg.angle = 0 # -50 ~ 50
	pub.publish(motor_msg)


def drive_stop():
	global motor_msg
	motor_msg.speed = 0
	motor_msg.angle = 0
	pub.publish(motor_msg)

rospy.init_node('lidar_driver')
rospy.Subscriber('/scan', LaserScan, callback, queue_size = 1)
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size = 1)
time.sleep(3) # ready to connect lidar


ang = 0

# 접근 2 - 중간으로 주행하기

while not rospy.is_shutdown():
	ok = 0

	# 전방 각도 범위를 3개로 분할 후 각 범위 중 최소 값 저장
	llidar_ranges = np.array(distance[lmin_check:lmax_check]) # 421 ~ 463
	rlidar_ranges = np.array(distance[rmin_check:rmax_check]) # 421 ~ 463
	clidar_ranges = np.concatenate([np.array(distance[0 : cmin_check]), np.array(distance[cmax_check:505])], axis=0) # 421 ~ 463
	llidar_ranges = np.where(llidar_ranges == 0.0, float('inf'), llidar_ranges)
	rlidar_ranges = np.where(rlidar_ranges == 0.0, float('inf'), rlidar_ranges)
	clidar_ranges = np.where(clidar_ranges == 0.0, float('inf'), clidar_ranges)

	ldis, rdis, cdis = np.min(llidar_ranges), np.min(rlidar_ranges), np.min(clidar_ranges)

	# 전방각도 물체가 0.25m 이내 or inf 값을 받을 경우 정지
	if cdis <= 0.25 or cdis == float('inf'):
		drive_stop() 
		time.sleep(0.2)
	# 왼쪽 or 오른쪽 양쪽에 물체가 0.2m 내로 가까워졌을 경우 정지
	elif ldis <= 0.2 and rdis <= 0.2:
		drive_stop()
		time.sleep(0.2)
	# 물체가 왼쪽, 오른쪽 각에서 발견될 경우 회전하여 이동
	elif ldis <= 0.4 :
		ang = 40
		drive_go(ang, 5)
	elif rdis <= 0.4:
		ang = -40
		drive_go(ang, 5)
	else:
		ang = 0
		drive_go(ang, 5)

	time.sleep(0.3) 

