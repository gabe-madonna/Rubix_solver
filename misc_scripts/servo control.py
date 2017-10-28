# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 09:58:46 2017

@author: Gabe Madonna
"""
import serial, time

arduino = serial.Serial('COM12', 9600, timeout=.5)
time.sleep(1)
#arduino.write("2058.3\n".encode()) # about one revolution

def motor_helper(motor, steps):
    # eventually a string from motor will have be parsed
    cmd = str(steps) + "\n"
    arduino.write(cmd.encode()) # about one revolution

def motor_rotate(motor, steps, reps):
    #one rev is 12 seconds
    #one rev is 2048 steps
    cycle_steps = 2048
    cycle_time = 12
    rev_time = 1 + reps / cycle_steps * cycle_time
    for i in range(reps):
        motor_helper(motor, steps)
        time.sleep(rev_time)
    arduino.close()

motor_rotate(1, 2048, 5)
