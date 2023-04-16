#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PidControl(object):
   
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.p_error = 0
        self.i_error = 0
        self.d_error = 0

    def pid_control(self, cte):
        self.d_error = cte-self.p_error
        self.p_error = cte
        if cte:
            self.i_error+=cte
        else:
            self.i_error = 0
        return self.kp*self.p_error+self.ki*self.i_error+self.kd*self.d_error

