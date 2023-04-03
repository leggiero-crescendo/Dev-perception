#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)

import rospy # rospy module
from std_msgs.msg import String
from msg_send.msg import my_msg
import time


def callback(msg):
    st_name = msg.last_name + '' + msg.first_name
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    st_name2 = 'Good morning'+ st_name + ' ' + curr_time
    pub.publish(st_name2)
    
rospy.init_node('remote_teacher', anonymous=True)
pub = rospy.Publisher('msg_from_xycar',String,queue_size=1)
sub = rospy.Subscriber('msg_to_xycar', my_msg, callback) 


rospy.spin()