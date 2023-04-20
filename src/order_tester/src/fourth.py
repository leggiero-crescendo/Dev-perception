#!/usr/bin/env python

import rospy
from std_msgs.msg import String

name = 'fourth'

OK = None

def ctl_callback(data):
    global OK
    OK = str(data.data)

rospy.init_node(name)
rospy.Subscriber("start_ctl", String, ctl_callback)

while True:
    if not OK: continue
    d = OK.split(":")
    if (len(d) == 2) and (d[0] == name) and (d[1] == "go"):
        break

pub = rospy.Publisher("msg_to_receiver", String, queue_size=1)

rate = rospy.Rate(2)
hello_str = String()

while not rospy.is_shutdown():
    hello_str.data = "my name is " + name
    pub.publish(hello_str)
    rate.sleep()