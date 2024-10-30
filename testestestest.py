from socketcan import CanRawSocket, CanFrame
import controller

# setting up can link
interface = "vcan0"
s = CanRawSocket(interface = interface)
can_id = 0x141

#input data
vel = -100

# NOTE BUS IS BIG ENDIEN (reads left to right)
data = bytearray(b'\xA2\x00\x00\x00')
data2 = vel.to_bytes(4, byteorder='big',  signed=True)
# data.append()
print(bytes(data))
print(data2)

data = bytes(data + data2)

print(bytes(data + data2))

# sending the data
frame1 = CanFrame(can_id = can_id, data = data)
print()
s.send(frame1)

print(16**8 - 1)