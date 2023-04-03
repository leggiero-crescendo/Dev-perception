#!/usr/bin/env python
#-*- coding: utf-8-*-


import rospy 
from std_msgs.msg import String
name = 'third'
class Stringbag():
    def __init__(self):
        self.pub_string = String()

    def callback(self, msg):
        self.data = msg.data

    def return_data(self):
        if self.data:
            return self.data
        else:
            return None


rospy.init_node('third')
str_bag = Stringbag()
sub = rospy.Subscriber('start_callback', String, str_bag.callback) # first, second
result = str_bag.return_data()

pub = rospy.Publisher('msg_go', String, queue_size=1)  
rate = rospy.Rate(2) 
string_data = String()

while not rospy.is_shutdown() and result == 'second':
    string_data = 'my name is '+name 
    pub.publish(string_data) 
    rate.sleep()
