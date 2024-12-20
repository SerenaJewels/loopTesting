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

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    activation = 0.25
    maxVel = 100

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
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
                # pprint.pprint(self.axis_data)
                # pprint.pprint(self.hat_data)

                if(len(self.axis_data) >= 4):
                    if(self.axis_data.get(0) < -activation):
                        self.axis_data[0] = (self.axis_data[0] - activation) / (1 - activation) * maxVel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(0) > activation):
                        self.axis_data[0] = (self.axis_data[0] + activation) / (1 - activation) * maxVel 
                    else:
                        self.axis_data[0] = 0

                    if(self.axis_data.get(1) < -activation):
                        self.axis_data[1] = (self.axis_data[1] - activation) / (1 - activation) * maxVel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(1) > activation):
                        self.axis_data[1] = (self.axis_data[1] + activation) / (1 - activation) * maxVel 
                    else:
                        self.axis_data[1] = 0

                    if(self.axis_data.get(3) < -activation):
                        self.axis_data[3] = (self.axis_data[3] - activation) / (1 - activation) * maxVel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(3) > activation):
                        self.axis_data[3] = (self.axis_data[3] + activation) / (1 - activation) * maxVel 
                    else:
                        self.axis_data[3] = 0

                    if(self.axis_data.get(4) < -activation):
                        self.axis_data[4] = (self.axis_data[4] - activation) / (1 - activation) * maxVel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(4) > activation):
                        self.axis_data[4] = (self.axis_data[4] + activation) / (1 - activation) * maxVel 
                    else:
                        self.axis_data[4] = 0

                    print(self.axis_data)

                else:
                    print('calibrate:', pprint.pprint(self.axis_data))

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()