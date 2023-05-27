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

    ServerSocket = None
    ClientSocket = None

    __host = "127.0.0.1" #loopback
    __port = 7777

    def __init__(self,Hssid = 'rpi42'):
        self.__Hssid = Hssid
        return
    def __del__(self):
        self.SocketClose()
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

        if(lines.find("error")):  #need to check log file..
           return False

        return True

    def SetTCPServerSocket(self):
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ServerSocket.bind(self.__host,self.__port)

    def SocketClose(self):
        self.ServerSocket.close()
        self.ClientSocket.close()







