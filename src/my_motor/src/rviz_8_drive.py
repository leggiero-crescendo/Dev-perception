#!/usr/bin/env python

import rospy
import time
from xycar_motor.msg import xycar_motor

motor_control = xycar_motor()

rospy.init_node('driver')

pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

def motor_pub(angle, speed):
    global pub
    global motor_control

    motor_control.angle = angle
    motor_control.speed = speed

    pub.publish(motor_control)


speed = 3
while not rospy.is_shutdown():
    angle = -50
    for i in range(40):
        motor_pub(angle, speed)
        time.sleep(0.1)

    angle = 0
    for i in range(30):
        motor_pub(angle, speed)
        time.sleep(0.1)

    angle = 50
    for i in range(40):
        motor_pub(angle, speed)
        time.sleep(0.1)

    angle = 0
    for i in range(30):
        motor_pub(angle, speed)
        time.sleep(0.1)