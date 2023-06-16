import os
import time 
import socket

'''
@기능
    Wifi 네트워크 접속을 총괄하는 클래스
    추가로 1:1 TCP/IP 통신을 위한 소켓의 준비 또한 진행한다.
@생성자 
    -Hssid : hotspot ssid '''
class cNetWorkManager():

    #hotspot wifi
    __Hssid = 'rpi42'
    __Hpasswd = ''
    #general wifi
    __ssid = ''
    __passwd = ''

    __ServerSocket : socket.socket  = socket.socket()
    __ServerAddr = None

    __ClientSocket  : socket.socket = socket.socket()
    __ClientAddr = None

    __host = "192.168.0.67" #loopback
    # __host = "127.0.0.1" #loopback

    __port = 7777

    __maxBuf = 512

    def __init__(self,Hssid = 'rpi42', maxBuf = 512):
        self.__Hssid = Hssid
        self.__maxBuf = maxBuf
        self.__ServerAddr = (self.__host,self.__port)
        return
    def __del__(self):
        self.Close()
        return

    def TurnOnHotSpot(self):
        os.system("sudo nmcli con down id '" + self.__Hssid + "'")  
        time.sleep(2)

    def SetGeneralWiFi(self,ssid : str, passwd : str) -> bool :
        self.__ssid = ssid
        self.__passwd = passwd

        os.system("sudo nmcli dev wifi con '" + self.__ssid + "' password '" + self.__passwd + "' > ./log.txt" )
        time.sleep(2)

        logFile =  open('./log.txt',"r")
        lines =  logFile.readlines()

        if(lines.find("successfully")):  #need to check log file..
           return True

        return False

    def SetTCPServerSocket(self):
        self.__ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__ServerSocket.bind(self.__ServerAddr)

    def GetCurrentClient(self) -> str:
        return self.__ClientAddr

    def Listen(self):
        self.__ServerSocket.listen()

    def Accept(self): 
        self.__ClientSocket, self.__ClientAddr = self.__ServerSocket.accept()

    def Recv(self) -> bytes :
        buf =  self.__ClientSocket.recv(self.__maxBuf)
        return buf
    
    def SendAll(self, buf : str):
        self.__ClientSocket.sendall(buf)

    def GethostIP(self) -> str:
        #s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #s.connect(("8.8.8.8",80))
        #hostip = s.getsockname()[0]
        #s.close()
        return self.__host

    def Close(self):
        self.__ServerSocket.close()
        self.__ClientSocket.close()



if __name__ == '__main__':
        network =  cNetWorkManager()

        network.SetTCPServerSocket()
        network.Listen()
        network.Accept()
        buf = network.Recv()

        print(buf)

        network.Close()



