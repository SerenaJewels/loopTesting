from socketcan import CanRawSocket, CanFrame
import controller

# setting up can link
interface = "vcan0"
s = CanRawSocket(interface = interface)
can_id = 0x141

# setting up controller link
ps4 = PS4Controller()
ps4.init()
ps4.listen()

# setting up initial vars
shoulder_yaw = 0
wrist_pitch = 0

# NOTE BUS IS BIG ENDIEN (reads left to right)
data = bytes(range(0, 0x88, 0x11))
print(range(0, 0x88, 0x11)[7])


# sending the data
frame1 = CanFrame(can_id = can_id, data = data)

s.send(frame1)