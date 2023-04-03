#!/usr/bin/env python
#-*- coding: utf-8-*-

import rospy
from timeit import default_timer as dtime
from std_msgs.msg import Int32, String

rate_num = input('input rate_num : ')
rospy.init_node('teacher')
pub = rospy.Publisher('msg_to_students', Int32, queue_size=0)
rate = rospy.Rate(rate_num)
num = input('input time : ')

def do_job(time):
	for i in range(0,time):
		i=i+1
		pub.publish(i)
def list_time():
    start.append(do_start)
    end.append(do_end)
    sleep.append(sleep_time)

while not rospy.is_shutdown():
    start = []
    end = []
    sleep = []
    rate.sleep()
    start_time = dtime()
    for i in range(0,rate_num):
        do_start = dtime()
        do_job(num)
        do_end = dtime()

        rate.sleep()
        sleep_time = dtime()
        list_time()
    end_time = dtime()

    for t in range(0,rate_num):
        sleep[t] = sleep[t] - end[t]
        end[t] = end[t] - start[t]
    for result in range(0,rate_num):
        print'do job time :%.4f sec'%(end[result])
        print'sleep time:%.4f sec'%(sleep[result])
    total = end_time - start_time
    print'----------------------------'
    print'total time : %.4f sec'%total
    print'----------------------------\n'
    