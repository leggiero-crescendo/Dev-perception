#!/usr/bin/env python
#-*- coding: utf-8-*-

import rospy 
from std_msgs.msg import Int32

rospy.init_node('send', anonymous=False)

pub = rospy.Publisher('my_topic', Int32, queue_size=0) 

rate = rospy.Rate(2)
cnt = 1
while ( pub.get_num_connections() == 0):
    cnt = 1

while not rospy.is_shutdown() and cnt <= 50: 
    pub.publish(cnt)
    print "SENT:", cnt 
    cnt += 1
    rate.sleep() 
