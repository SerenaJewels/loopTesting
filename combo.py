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

    def init(self, bus):
        """Initialize the joystick components"""
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        """Initialize socket"""
        interface = bus
        can_id = 0x141
        s = CanRawSocket(interface = interface)

    def listen(self):
        """Listen for events to happen"""
        dirArr = ['n', 'n']
        
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

                if(len(self.axis_data) == 4):
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

                    if(self.axis_data.get(2) < -0.85):
                        dirArr[1] = 'l'
                    elif(self.axis_data.get(2) > 0.85):
                        dirArr[1] = 'r'
                    elif(self.axis_data.get(3) < -0.85):
                        dirArr[1] = 'u'
                    elif(self.axis_data.get(3) > 0.85):
                        dirArr[1] = 'd'
                    else:
                        dirArr[1] = 'n'

                    print(dirArr)

                    
                    data = bytes(range(0, 0x88, 0x11))

                    frame1 = CanFrame(can_id = self.can_id, data = self.data)

                    self.s.send(frame1)
                
                else:
                    print('calibrate:', pprint.pprint(self.axis_data))

if __name__ == "__main__":
    ps4 = PS4ToBus()
    ps4.init("vcan0")
    ps4.listen()