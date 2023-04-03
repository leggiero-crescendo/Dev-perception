#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(msg):
	rospy.loginfo("I heard %s", msg.data)

rospy.init_node('receiver')
rospy.Subscriber('msg_to_receiver',String, callback)
pub = rospy.Publisher('start_ctl',String,queue_size=1)

rate = rospy.Rate(10)
hello_str = String()

rospy.sleep(1)

sq = ['first','second','third','fourth']
pub_msg = String()

for i in sq:
	pub_msg.data = i+":go"
	pub.publish(pub_msg)
	rospy.sleep(3)

rospy.spin()