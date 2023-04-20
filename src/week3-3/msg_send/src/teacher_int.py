#!/usr/bin/env python
#-*- coding: utf-8-*-
# python shebang으로 스크립트 해석시 인터프린터 지시자
# script 첫줄에 사용
# https://ko.wikipedia.org/wiki/%EC%85%94%EB%B1%85

import rospy # python 을 이용하여 ROS를 사용할 수 있게 하는 library http://wiki.ros.org/rospy
# from std_msgs.msg import String
from std_msgs.msg import Int32

# 설명참고 http://wiki.ros.org/rospy_tutorials/Tutorials/WritingPublisherSubscriber
rospy.init_node('teacher')
'''
rospy에게 node의 이름을 알려주는 작업 master와 통신할 수 있게 해줌
'''
pub = rospy.Publisher('my_topic', Int32, queue_size=5) # topic 발행 my_topic, string type 

rate = rospy.Rate(2) # 2hz , 초당 2회 루프를 통과한다는 의미 (0.5초 안에 loop를 반복할 수 있도록 rate 객체를 만드는 코드! 작업시간/ 휴식시간이 0.5초라는 timeslot 내에 포함됨
cnt = 1
while not rospy.is_shutdown(): # rospy내에서  shutdown flag가 있는지 검사 
    pub.publish(cnt) # publish('원하는 메시지')를 통해 생성한 토픽과 함께 publish
    cnt += 1
    rate.sleep() # rospy.Rate() 앞서 설정한 주기만큼 반복문 돌 수 있도록 반복문내에 선언
