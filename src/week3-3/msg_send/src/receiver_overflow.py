#!/usr/bin/env python
#-*- coding: utf-8-*-

import sys
import rospy # rospy module
from std_msgs.msg import Int32

name = 'receiver'
sub_topic = 'my_topic'

def callback(msg):
    rospy.loginfo('callback')
    rospy.sleep(5)
    print msg.data

rospy.init_node(name, anonymous=True) 
sub = rospy.Subscriber(sub_topic, Int32, callback, queue_size=1) 

rospy.spin()