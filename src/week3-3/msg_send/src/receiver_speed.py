#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)
import sys
import rospy # rospy module
from std_msgs.msg import String

name = 'receiver'
sub_topic = 'long_string'

def callback(data):
    msgs = data.data.split(":")
    time_data = float(rospy.get_time()) - float(msgs[1])
    str_size = sys.getsizeof(msgs[0])
    rospy.loginfo(str(str_size)+"byte :"+str(time_data)+"s")
    rospy.loginfo("speed:"+str(float(str_size)/max(time_data, 1e-9))+"Mbyte/s")
    
rospy.init_node(name, anonymous=True) 
sub = rospy.Subscriber(sub_topic, String, callback) 

rospy.spin() 
