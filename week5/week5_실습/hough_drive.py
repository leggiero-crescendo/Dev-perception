#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy, rospkg
import numpy as np
import cv2, random, math
from cv_bridge import CvBridge
from xycar_motor.msg import xycar_motor
from sensor_msgs.msg import Image
from collections import deque

import sys
import os
import signal


from MovingAverage import MovingAverage
from PID import PidControl

class HoughLine(object):

    def __init__(self):

        self.image = np.empty(shape=[0])
        self.bridge = CvBridge()
        self.pub = None
        self.frame_w = 640
        self.frame_h = 480
        self.offset = 320#370
        self.gab = 50#60 #40

        rospy.init_node('auto_drive')
        self.pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

        self.image_sub = rospy.Subscriber("/usb_cam/self.image_raw", self.image, self.img_callback)
        rospy.sleep(0.05)

    def img_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    # publish xycar_motor msg
    def drive(self, Angle, Speed): 

        msg = xycar_motor()
        msg.angle = Angle
        msg.speed = Speed

        self.pub.publish(msg)

    # draw lines
    def draw_lines(self, img, lines):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            img = cv2.line(img, (x1, y1+self.offset), (x2, y2+self.offset), color, 2)
        return img

    # draw rectangle
    def draw_rectangle(self, img, lpos, rpos, offset=0):
        center = (lpos + rpos) / 2

        cv2.rectangle(img, (lpos - 5, 15 + self.offset),
                        (lpos + 5, 25 + self.offset),
                        (0, 255, 0), 2)
        cv2.rectangle(img, (rpos - 5, 15 + self.offset),
                        (rpos + 5, 25 + self.offset),
                        (0, 255, 0), 2)
        cv2.rectangle(img, (center-5, 15 + self.offset),
                        (center+5, 25 + self.offset),
                        (0, 255, 0), 2)    
        cv2.rectangle(img, (315, 15 + self.offset),
                        (325, 25 + self.offset),
                        (0, 0, 255), 2)
        return img

    # left lines, right lines
    def divide_left_right(self, lines):
        low_slope_threshold = 0
        high_slope_threshold = 10

        # calculate slope & filtering with threshold
        slopes = []
        new_lines = []

        for line in lines:
            x1, y1, x2, y2 = line[0]

            if x2 - x1 == 0:
                slope = 0
            else:
                slope = float(y2-y1) / float(x2-x1)
            
            if abs(slope) > low_slope_threshold and abs(slope) < high_slope_threshold:
                slopes.append(slope)
                new_lines.append(line[0])

        # divide lines left to right
        left_lines = []
        right_lines = []

        for j in range(len(slopes)):
            Line = new_lines[j]
            slope = slopes[j]

            x1, y1, x2, y2 = Line

            if (slope < 0) and (x2 < self.frame_w/2 - 90):
                left_lines.append([Line.tolist()])
            elif (slope > 0) and (x1 > self.frame_w/2 + 90):
                right_lines.append([Line.tolist()])
        return left_lines, right_lines

    # get average m, b of lines
    def get_line_params(self, lines):
        # sum of x, y, m
        x_sum = 0.0
        y_sum = 0.0
        m_sum = 0.0

        size = len(lines)
        if size == 0:
            return 0, 0

        for line in lines:
            x1, y1, x2, y2 = line[0]

            x_sum += x1 + x2
            y_sum += y1 + y2
            m_sum += float(y2 - y1) / float(x2 - x1)

        x_avg = x_sum / (size * 2)
        y_avg = y_sum / (size * 2)
        m = m_sum / size
        b = y_avg - m * x_avg

        return m, b

    # get lpos, rpos
    def get_line_pos(self, img, lines, left=False, right=False):

        m, b = self.get_line_params(lines)

        if m == 0 and b == 0:
            if left:
                pos = 0
            if right:
                pos = self.frame_w
        else:
            y = self.gab / 2
            pos = (y - b) / m

            b += self.offset
            x1 = (self.frame_h - b) / float(m)
            x2 = ((self.frame_h/2) - b) / float(m)

            cv2.line(img, (int(x1), self.frame_h), (int(x2), (self.frame_h/2)), (255, 0,0), 3)

        return img, int(pos)

    def process_img(self, img):
        thresh_line = 40 # small : low acc, many lines 
        min_length = 40 
        line_bool = False
        frame = img.copy()

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # blur
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)

        # canny edge
        low_threshold = 60
        high_threshold = 70
        edge_img = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold)

        # HoughLinesP
        roi = edge_img[self.offset : self.offset+self.gab, 0 : self.frame_w]
        # adjust until a line is detected 
        while not line_bool:
            all_lines = cv2.HoughLinesP(roi,1,math.pi/180, thresh_line, min_length, max_self.gab)
            if all_lines is None:
                line_bool = False
                thresh_line -= 2
            else:
                line_bool = True
            if thresh_line < 30:
                all_lines = None
                break
            # print("threshold", thresh_line)
        cv2.imshow('roi', roi)

        # print(all_lines)
        if all_lines is None:
            rospy.loginfo("Nothing")
            # None value 
            return 0, 640
        # divide left, right lines
        left_lines, right_lines = self.divide_left_right(all_lines)

        # get center of lines
        frame, lpos = self.get_line_pos(frame, left_lines, left=True)
        frame, rpos = self.get_line_pos(frame, right_lines, right=True)

        # draw lines
        frame_line = self.draw_lines(frame, left_lines)
        frame_line = self.draw_lines(frame_line, right_lines)
        # draw horizon lines
        frame_line = cv2.line(frame_line, (230, 235), (410, 235), (255,255,255), 2)
                                    
        # draw rectangle (l,r - c:G / (w/2):R)
        frame_rec = self.draw_rectangle(frame_line, lpos, rpos, offset=self.offset)
        #roi2 = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
        #roi2 = draw_rectangle(roi2, lpos, rpos)

        # show self.image
        cv2.imshow('calibration', frame_rec)

        return lpos, rpos

    def draw_steer(self, image, steer_angle):
        # read of steer_arrow
        arrow_pic = cv2.imread('steer_arrow.png', cv2.INREAD_COLOR)

        # to calcurate
        origin_frame_h = arrow_pic.shape[0]
        origin_frame_w = arrow_pic.shape[1]
        steer_wheel_center = origin_frame_h * 0.74
        arrow_frame_h = self.frame_h / 2
        arrow_frame_w = (arrow_frame_h * 462) / 728

        # rotate steer img by using steer angle
        matrix = cv2.getRotatedMatrix2D((origin_frame_w / 2, steer_wheel_center), (steer_angle) * 2.5, 0.7)

        # fit img 
        arrow_pic = cv2.warpAffine(arrow_pic, matrix, (origin_frame_w + 60, origin_frame_h))
        arrow_pic = cv2.resize(arrow_pic, dsize = (arrow_frame_w, arrow_frame_h), interpolation = cv2.INTER_AREA)

        # full self.image + steer angle
        gray_arrow = cv2.cvtColor(arrow_pic, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_arrow, 1, 255, cv2.THRESH_BINARY_INV)

        arrow_roi = self.image[arrow_frame_h : self.frame_h, 
                        (self.frame_w / 2 - arrow_frame_w / 2) : (self.frame_w / 2 + arrow_frame_w / 2)]
        arrow_roi = cv2.add(arrow_pic, arrow_roi, mask = mask)

        res = cv2.add(arrow_roi, arrow_pic)

        self.image[(self.frame_h - arrow_frame_h) : self.frame_h,
            (self.frame_w / 2 - arrow_frame_w / 2) : (self.frame_w / 2 + arrow_frame_w / 2)] = res
        
        cv2.imshow('steer', self.image)

    def draw_angle(self, draw_image, steer_angle, error, norm):

        self.image_copy = draw_image.copy()
        cv2.putText(self.image_copy, str(steer_angle), (50,50), cv2.FONT_ITALIC, 1, (255,0,0), 2)
        cv2.putText(self.image_copy, str(error), (50,100), cv2.FONT_ITALIC, 1, (0,0,255), 2)
        cv2.putText(self.image_copy, str(norm), (50,150), cv2.FONT_ITALIC, 1, (0,255,0), 2)

        cv2.imshow('angle', self.image_copy)

    def start(self):
        left_center = 160
        right_center = 480

        angle = 2.5
        angle_temp = 2.5 
        speed = 5
        angle_list = []

        # mm = MovingAverage(10)
        # ml = MovingAverage(10)
        # mr = MovingAverage(10)
        # pid = PidControl(0.56, 0.0007, 0.2)
        # pid = PidControl(0.3, 0.0007, 0.2)

        # self.images = self.image.copy()
        while True:
            while not self.image.size == (640*480*3):
                continue
            lpos, rpos = self.process_img(self.image)
            # ml.add_sample(lpos)
            # mr.add_sample(rpos)

            # lpos = ml.get_wmm()
            # rpos = mr.get_wmm()

            center = (lpos + rpos) / 2
            angle = (center - self.frame_w/2)
            angle = angle*0.4 # sol 1) 값의 급격한 변화를 줄이기 위해


            if lpos==0 and rpos==640: # can't recognize lanes
                angle_temp = angle
                rospy.loginfo("Nothing : "+str(angle_temp))
                if self.offset!=370:
                    self.offset+=10

            # sol 2) 둘 중에 선이 안 잡힐 경우 선 하나만 이용
            elif lpos == 0:
                error = right_center - rpos
                error = error*0.2 
                print("r", error)
            elif rpos == 640:
                error = left_center - lpos
                error = error*0.2
                print("l", error)

            # angle = pid.pid_control(error)
            # mm.add_sample(angle)
            # mean_angle = mm.get_wmm()
            mean_angle = angle

            rospy.sleep(0.05)

            if abs(mean_angle) >= 50:
                self.drive(50, 7)
                rospy.loginfo("over 50 : "+str(mean_angle))

                self.offset = 360
            elif 30 < abs(mean_angle) < 50:
                self.drive(mean_angle, 7 )
                rospy.loginfo("30 ~ 50 : "+ str(mean_angle))
            else:
                self.drive(mean_angle, 7 )
                # self.offset = 370
                rospy.loginfo("else : "+str(mean_angle))


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        rospy.spin()

if __name__ == '__main__':
    hough = HoughLine()
    hough.start() 