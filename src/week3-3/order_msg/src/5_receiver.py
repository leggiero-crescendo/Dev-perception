#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)

import rospy # rospy module
from std_msgs.msg import String 


class Multi():
    def __init__(self):
        self.pub_string = String()

    def callback(self, msg):
        data = msg.data.split()
        self.pub_string = data[-1]
        return self.pub_string

    def return_data(self):
        return self.pub_string

multi_data = Multi()
rospy.init_node('receiver')
sub = rospy.Subscriber('msg_go', String, multi_data.callback) # first, second
result = multi_data.return_data()
print "result",sub.callback

pub = rospy.Publisher('start_callback', String, queue_size=1) # msg.data
rate = rospy.Rate(2) 
while not rospy.is_shutdown():
    pub.publish(result) 
    rate.sleep()

rospy.spin()
