#!/usr/bin/env python
#-*- coding: utf-8-*-

import rospy 
from std_msgs.msg import String

rospy.init_node('sender', anonymous=True)

pub = rospy.Publisher('long_string', String) 
size = rospy.get_param('~size')
hash = '#'* 1000000 * size#size_dic[size]


rate = rospy.Rate(1) #초당 1회

while not rospy.is_shutdown():
    print size 

    hash_time = hash + ":" + str(rospy.get_time())
    print hash_time
    pub.publish(hash_time) 
    rate.sleep() 
