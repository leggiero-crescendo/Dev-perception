#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, rospkg
import numpy as np
import cv2, random, math
from cv_bridge import CvBridge
from xycar_motor.msg import xycar_motor
from sensor_msgs.msg import Image

import sys
import os
import signal


class Sliding(object):
    
    def __init__(self):

        self.WIN_TITLE = 'camera'


        self.FRAME_W = 640
        self.FRAME_H = 480

        self.WARP_IMG_W = 320
        self.WARP_IMG_H = 240

        self.WARP_X_MARGIN = 30
        self.WARP_Y_MARGIN = 3

        # sliding windows value
        self.WIN_N = 9 # window num
        self.WIN_WIDTH = 12 # self.FRAME_W
        self.WIN_MIN_POINT = 5 # minimum point

        self.THR_VALUE = 100 # thresh 임계값
        self.THR_CONVERT = 255 # thresh 적용 했을 때 바뀌는 값

        # self.num_list = [220, 330, 80, 420, 570, 420, 400, 330]
        self.num_list = [145, 330, 30, 420, 480, 420, 370, 330] #B, G, R, Black

        self.warp_src = np.array([[self.num_list[0] - self.WARP_X_MARGIN, self.num_list[1] - self.WARP_Y_MARGIN],
        [self.num_list[2] - self.WARP_X_MARGIN, self.num_list[3] + self.WARP_Y_MARGIN],
        [self.num_list[6] + self.WARP_X_MARGIN, self.num_list[7]- self.WARP_Y_MARGIN],
        [self.num_list[4] + self.WARP_X_MARGIN, self.num_list[5] - self.WARP_Y_MARGIN]],
        dtype=np.float32)

        self.warp_dist = np.array([
                                    [0,0],
                                    [0,self.WARP_IMG_H],
                                    [self.WARP_IMG_W,0],
                                    [self.WARP_IMG_W, self.WARP_IMG_H]
                                ], dtype=np.float32)

        self.cv_image = np.empty(shape=[0])
        self.bridge = CvBridge()



        calibrated = True
        if calibrated:
            self.mtx = np.array([
                [422.037858, 0.0, 245.895397], 
                [0.0, 435.589734, 163.625535], 
                [0.0, 0.0, 1.0]
            ])
            self.dist = np.array([-0.289296, 0.061035, 0.001786, 0.015238, 0.0])
            self.cal_mtx, self.cal_roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.FRAME_W, self.FRAME_H), 1, (self.FRAME_W, self.FRAME_H))
        
        rospy.init_node('auto_drive')
        # self.pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.img_callback)
        rospy.sleep(2)
    
    
    def img_callback(self, data):

        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

    def drive(self, Angle, Speed): 

        msg = xycar_motor()
        msg.angle = Angle
        msg.speed = Speed

        self.pub.publish(msg)

    def calibrate_image(self, frame):
        
        tf_image = cv2.undistort(frame, self.mtx, self.dist, None, self.cal_mtx)
        x, y, w, h = self.cal_roi
        tf_image = tf_image[y:y+h, x:x+w]
        cv2.imwrite("./img/tf.png", tf_image)

        return cv2.resize(tf_image, (self.FRAME_W, self.FRAME_H))

    def warp_image(self, img, src, dst, size):
        M = cv2.getPerspectiveTransform(src, dst)
        Minv = cv2.getPerspectiveTransform(dst, src)
        wide_img = img[200:400,:]
        # M_trans = np.float32([[1,0,100],[0,1,-500]])
        # M_wide = M -np.float32([[0,0,-100],[0,0,500],[0,0,0]])
        warp_img_wide = cv2.warpPerspective(wide_img, M, (1000, 1000), flags=cv2.INTER_NEAREST)#)cv2.INTER_LINEAR)
        warp_img = cv2.warpPerspective(img, M, size, flags=cv2.INTER_LINEAR)

        cv2.imshow("wide_img", warp_img_wide)
        cv2.imshow("warp", warp_img)
        return warp_img, M, Minv


    def warp_process_image(self, img):

        blur = cv2.GaussianBlur(img,(5, 5), 0)

        _, L, _ = cv2.split(cv2.cvtColor(blur, cv2.COLOR_BGR2HLS))
        # cv2.imshow("L",L)
        _, lane = cv2.threshold(L, self.THR_VALUE, self.THR_CONVERT, cv2.THRESH_BINARY_INV)
        cv2.imshow("thresh",lane)

        histogram = np.sum(lane[lane.shape[0]//2:,:], axis=0)      
        midpoint = np.int(histogram.shape[0]/2)
        leftx_current = np.argmax(histogram[:midpoint])
        rightx_current = np.argmax(histogram[midpoint:]) + midpoint

        window_height = np.int(lane.shape[0]/self.WIN_N)
        nz = lane.nonzero()

        left_lane_inds = []
        right_lane_inds = []
        
        lx, ly, rx, ry = [], [], [], []

        out_img = np.dstack((lane, lane, lane))*255

        for window in range(self.WIN_N):

            win_yl = lane.shape[0] - (window+1)*window_height
            win_yh = lane.shape[0] - window*window_height

            win_xll = leftx_current - self.WIN_WIDTH
            win_xlh = leftx_current + self.WIN_WIDTH
            win_xrl = rightx_current - self.WIN_WIDTH
            win_xrh = rightx_current + self.WIN_WIDTH

            cv2.rectangle(out_img,(win_xll,win_yl),(win_xlh,win_yh),(0,255,0), 2) 
            cv2.rectangle(out_img,(win_xrl,win_yl),(win_xrh,win_yh),(0,255,0), 2) 

            good_left_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xll)&(nz[1] < win_xlh)).nonzero()[0]
            good_right_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xrl)&(nz[1] < win_xrh)).nonzero()[0]

            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)

            if len(good_left_inds) > self.WIN_MIN_POINT:
                leftx_current = np.int(np.mean(nz[1][good_left_inds]))
            if len(good_right_inds) > self.WIN_MIN_POINT:        
                rightx_current = np.int(np.mean(nz[1][good_right_inds]))

            lx.append(leftx_current)
            ly.append((win_yl + win_yh)/2)

            rx.append(rightx_current)
            ry.append((win_yl + win_yh)/2)

        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        #left_fit = np.polyfit(nz[0][left_lane_inds], nz[1][left_lane_inds], 2)
        #right_fit = np.polyfit(nz[0][right_lane_inds] , nz[1][right_lane_inds], 2)
        
        lfit = np.polyfit(np.array(ly),np.array(lx),2)
        rfit = np.polyfit(np.array(ry),np.array(rx),2)

        out_img[nz[0][left_lane_inds], nz[1][left_lane_inds]] = [255, 0, 0]
        out_img[nz[0][right_lane_inds] , nz[1][right_lane_inds]] = [0, 0, 255]


        cv2.imshow("viewer", out_img)
        
        #return left_fit, right_fit
        return lfit, rfit

    def draw_lane(self, image, warp_img, Minv, left_fit, right_fit):
        yMax = warp_img.shape[0]
        ploty = np.linspace(0, yMax - 1, yMax)
        color_warp = np.zeros_like(warp_img).astype(np.uint8)
        
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))]) 
        pts = np.hstack((pts_left, pts_right))
        
        color_warp = cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
        newwarp = cv2.warpPerspective(color_warp, Minv, (self.FRAME_W, self.FRAME_H))

        return cv2.addWeighted(image, 1, newwarp, 0.3, 0)

    def draw_angle(self, image, steer_angle):
        cv2.putText(image, str(steer_angle), (50,50), cv2.FONT_ITALIC, 1, (255,0,0), 2)
        cv2.imshow('steer', image)

    def start(self):

        while True:
            while not self.cv_image.size == (640*480*3):
                continue

            image = self.calibrate_image(self.cv_image)
            warp_img, M, Minv = self.warp_image(image, self.warp_src, self.warp_dist, (self.WARP_IMG_W, self.WARP_IMG_H))
            left_fit, right_fit = self.warp_process_image(warp_img)
            lane_img = self.draw_lane(image, warp_img, Minv, left_fit, right_fit)

            cv2.circle(lane_img, (self.num_list[0], self.num_list[1]), 5, (255,0,0),-1)
            cv2.circle(lane_img, (self.num_list[2], self.num_list[3]), 5, (0,255,0),-1)
            cv2.circle(lane_img, (self.num_list[6], self.num_list[7]), 5, (0,0,0),-1)
            cv2.circle(lane_img, (self.num_list[4], self.num_list[5]), 5, (0,0,255),-1)
            # draw_angle(lane_img, )
            cv2.imshow(self.WIN_TITLE, lane_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':

    lane_sliding = Sliding()
    lane_sliding.start()