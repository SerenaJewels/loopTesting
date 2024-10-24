#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.
#
# https://gist.github.com/claymcleod/028386b860b75e4f5472

import os
import pprint
import pygame
import socketcan

class PS4ToBus(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    s = None
    interface = "vcan0"
    can_id = 0x141

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        # setting up can link
        s = CanRawSocket(interface = interface)

    def listen(self):
        """Listen for events to happen"""
        dirArr = ['n', 'n', False, False, False, False] # left joystick, right joystick, left bumper, right bumper, left trigger, right trigger
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
                # os.system('clear')
                # pprint.pprint(self.button_data)
                dirArr[2] = self.button_data[4]
                dirArr[3] = self.button_data[5]
                dirArr[4] = self.button_data[6]
                dirArr[5] = self.button_data[7]

                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)

                if(len(self.axis_data) >= 4):
                    # print(self.axis_data)
                    if(self.axis_data.get(0) < -0.85):
                        dirArr[0] = 'l'
                    elif(self.axis_data.get(0) > 0.85):
                        dirArr[0] = 'r'
                    elif(self.axis_data.get(1) < -0.85):
                        dirArr[0] = 'u'
                    elif(self.axis_data.get(1) > 0.85):
                        dirArr[0] = 'd'
                    else:
                        dirArr[0] = 'n'

                    if(self.axis_data.get(3) < -0.85):
                        dirArr[1] = 'l'
                    elif(self.axis_data.get(3) > 0.85):
                        dirArr[1] = 'r'
                    elif(self.axis_data.get(4) < -0.85):
                        dirArr[1] = 'u'
                    elif(self.axis_data.get(4) > 0.85):
                        dirArr[1] = 'd'
                    else:
                        dirArr[1] = 'n'

                    # print(dirArr)
                    print(self.axis_data)
                else:
                    print('calibrate:', self.axis_data)

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()