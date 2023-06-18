import NetWorkManager as NW
from PacketManager import cPacketManager
import socket
 

PacketManager = cPacketManager()

tcp_socket = socket.create_connection(('192.168.0.3', 7777))
 
try:
    sendingContent = {  "0" : "1",
                        "1" : "0", 
                        "2" : "0",
                        "3" : "0",
                        "4" : "0"}
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