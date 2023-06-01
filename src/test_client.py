import NetWorkManager as NW
from PacketManager import cPacketManager
import socket
 

PacketManager = cPacketManager()
tcp_socket = socket.create_connection(('localhost', 7777))
 
try:
    sendingContent = {  "0" : "0",
                        "1" : "1", 
                        "2" : "0" ,
                        "3" : "5",
                        "4" : "1"}
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