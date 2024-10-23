from socketcan import CanRawSocket, CanFrame
interface = "vcan0"
s = CanRawSocket(interface = interface)

can_id = 0x141
data = bytes(range(0, 0x88, 0x11))

frame1 = CanFrame(can_id = can_id, data = data)

s.send(frame1)