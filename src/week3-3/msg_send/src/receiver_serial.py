#!/usr/bin/env python
#-*- coding: utf-8-*-
# Sheband(#!)

import rospy # rospy module
from std_msgs.msg import Int32

class MSG():
    def __init__(self):
        self.num = 0
        self.miss = 0

    def callback(self, msg):
        if msg.data != self.num+1:
            self.miss = [msg.data - self.num - 1]
            print "Missed :", self.miss
        self.num = msg.data
        print "Received :", [msg.data] 
    
msg_c = MSG()
rospy.init_node('student') 
sub = rospy.Subscriber('my_topic', Int32, msg_c.callback) 

rospy.spin() 
