#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

rospy.init_node('my_node', anonymous=True)
pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)

msg = Twist()
rate = rospy.Rate(1)

def turtlekey(msg, linear, angular):
    x, y, z = linear
    rx, ry, rz = angular
    msg.linear.x = x
    msg.linear.y = y
    msg.linear.z = z
    msg.angular.x = rx
    msg.angular.y = ry
    msg.angular.z = rz

num = rospy.get_param('~num')

while not rospy.is_shutdown():
    for i in range(0, num):
        turtlekey(msg, [3.0, 0.0, 0.0], [0.0, 0.0, -3.0])
        pub.publish(msg)
        rate.sleep()
    for j in range(0, num):
        turtlekey(msg, [3.0, 0.0, 0.0], [0.0, 0.0, 3.0])
        pub.publish(msg)
        rate.sleep()

