from socketcan import CanRawSocket, CanFrame
import pprint
import pygame

class PS4ToBus(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    interface = None
    can_id = None
    s = None
    data = None
    activation = 0.25
    maxvel = 100 #16**8 - 1

    def init(self, bus):
        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        """Initialize socket"""
        interface = bus
        self.can_id = 0x141
        self.s = CanRawSocket(interface = interface)

    def listen(self):
        joystick_vels = [0, 0, 0, 0]

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
                    if(self.axis_data.get(0) < -self.activation):
                        joystick_vels[0] = ((self.axis_data[0] + self.activation) / (1 - self.activation)) * self.maxvel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(0) > self.activation):
                        joystick_vels[0] = ((self.axis_data[0] - self.activation) / (1 - self.activation)) * self.maxvel 
                    else:
                        joystick_vels[0] = 0

                    if(self.axis_data.get(1) < -self.activation):
                        joystick_vels[1] = ((self.axis_data[1] + self.activation) / (1 -self.activation)) *self.maxvel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(1) >self.activation):
                        joystick_vels[1] = ((self.axis_data[1] - self.activation) / (1 -self.activation)) *self.maxvel 
                    else:
                        joystick_vels[1] = 0

                    if(self.axis_data.get(3) < -self.activation):
                        joystick_vels[2] = ((self.axis_data[3] + self.activation) / (1 -self.activation)) *self.maxvel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(3) >self.activation):
                        joystick_vels[2] = ((self.axis_data[3] - self.activation) / (1 -self.activation)) *self.maxvel 
                    else:
                        joystick_vels[2] = 0

                    if(self.axis_data.get(4) < -self.activation):
                        joystick_vels[3] = ((self.axis_data[4] + self.activation) / (1 -self.activation)) *self.maxvel  # normalizes the 0.25 to 1 range to a 0 - 1 range and then mult by max vel
                    elif(self.axis_data.get(4) >self.activation):
                        joystick_vels[3] = ((self.axis_data[4] - self.activation) / (1 -self.activation)) *self.maxvel 
                    else:
                        joystick_vels[3] = 0

                    print(self.axis_data[0])
                    print(joystick_vels)

                    self.data = bytearray(b'\xA2\x00\x00\x00')
                    self.data += int(joystick_vels[0]).to_bytes(4, byteorder='big', signed=True)
                    self.data = bytes(self.data)
                    frame1 = CanFrame(can_id = self.can_id, data = self.data)
                    self.s.send(frame1)
                
                else:
                    print('calibrate:', pprint.pprint(self.axis_data))

if __name__ == "__main__":
    ps4 = PS4ToBus()
    ps4.init("vcan0")
    ps4.listen()