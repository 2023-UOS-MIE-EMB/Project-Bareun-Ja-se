import NetWorkManager as NW
from PacketManager import cPacketManager
import socket
 

PacketManager = cPacketManager()
tcp_socket = socket.create_connection(('192.168.0.67', 7777))

#0:angle
#1:strmrq
#2:power
#3:altm time
#4:arlm mode
try:
    sendingContent = {  "0" : "1",
                        "1" : "0", 
                        "2" : "0",
                        "3" : "1",
                        "4" : "2"}
    result, packet = PacketManager.MakingPacketToSend(sendingContent)
    print(packet)
    parsingresult = PacketManager.ParsingPacket(packet)
    print(parsingresult)

    
    tcp_socket.sendall(packet)
    print("---------")

    
    buf = tcp_socket.recv(512)
    print("recv:",buf)
 
finally:
    print("Closing socket")
    tcp_socket.close()