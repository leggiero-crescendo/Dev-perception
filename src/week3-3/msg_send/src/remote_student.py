#!/usr/bin/env python
#-*- coding: utf-8-*-

import rospy 
from std_msgs.msg import String
from msg_send.msg import my_msg

done = False
def callback(msg): # callback 함수 정의
    print msg.data # msg.data 출력
    done = True

rospy.init_node('remote_student', anonymous=True)
pub = rospy.Publisher('msg_to_xycar', my_msg)
rospy.Subscriber('msg_from_xycar', String, callback)
rate = rospy.Rate(2) 

msg = my_msg()
msg.first_name = "Gil-Dong"
msg.last_name = "Hong"
msg.age = 15
msg.score = 100
msg.id_number = 12345678
msg.phone_number = "010-0000-0000"


while not rospy.is_shutdown() and not done: 
    pub.publish(msg)
    print 'send...' 
    rate.sleep() 