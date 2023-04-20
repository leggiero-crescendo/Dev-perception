#!/usr/bin/env python

import rospy
import time
from xycar_motor.msg import xycar_motor

motor_control = xycar_motor()

# auto driver 노드 만들기
rospy.init_node("auto_driver")

# 토픽 발행 준비
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size = 1)

# angle 값과 speed 값을 인자로 받아 그걸 xycar_motor 토픽에 담아 발행
def motor(angle, speed):
    global pub
    global motor_control

    motor_control.angle = angle
    motor_control.speed = speed

    pub.publish(motor_control)

speed = 3                       # 구동속도 3으로 설정
while not rospy.is_shutdown():
    angle = -50                 # 좌회전, 조향각 최대(핸들 최대한 왼쪽) 
    for _ in range(60):
        motor(angle, speed)
        time.sleep(0.1)

    angle = 0                   # 직진(핸들 중앙)
    for _ in range(30):
        motor(angle, speed)
        time.sleep(0.1)

    angle = 50                  # 우회전, 조향각 최대(핸들 최대한 오른쪽)
    for _ in range(60):
        motor(angle, speed)
        time.sleep(0.1)

    angle = 0                   # 직진(핸들 중앙)
    for _ in range(30):
        motor(angle, speed)
        time.sleep(0.1)

