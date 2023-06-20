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

    __host = "192.168.0.4" #host_ip

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
    '''
    @기능 
        사전에 미리 지정해 놓은 RPI hotspot을 켠다.'''
    def TurnOnHotSpot(self):
        os.system("sudo nmcli con down id '" + self.__Hssid + "'")  
        time.sleep(2)

    '''
    @기능 
        와이파이 이름과 비밀번호를 통해 와이파이에 접속한다..'''
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
    '''
    @기능 
        TCP서버의 리스팅 소켓을 생성 하고 바인드 한다.'''
    def SetTCPServerSocket(self):
        self.__ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__ServerSocket.bind(self.__ServerAddr)

    '''
    @기능 
       현재 서버와 연결한 클라이언트의 주소를 얻는다'''
    def GetCurrentClient(self) -> str:
        return self.__ClientAddr

    def Listen(self):
        self.__ServerSocket.listen()

    def Accept(self) -> bool: 
        try :
            self.__ServerSocket.settimeout(1)
            self.__ClientSocket, self.__ClientAddr = self.__ServerSocket.accept()
            return True
        except socket.error :
            return False
    def Recv(self) -> bytes :
        buf =  self.__ClientSocket.recv(self.__maxBuf)
        return buf
    
    def SendAll(self, buf : str):
        self.__ClientSocket.sendall(buf)
    '''
    @기능 
       현재 서버의 주소를 얻는다. 주석을 해제하면 인터넷 연결이 되는 네트워크라면 자동으로 주소를 받아올 수 있다.'''
    def GethostIP(self) -> str:
        #s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #s.connect(("8.8.8.8",80))
        #hostip = s.getsockname()[0]
        #s.close()
        return self.__host

    def Close(self):
        self.__ServerSocket.close()
        self.__ClientSocket.close()


#테스트 코드#
if __name__ == '__main__':
        network =  cNetWorkManager()

        network.SetTCPServerSocket()
        network.Listen()
        network.Accept()
        buf = network.Recv()

        print(buf)

        network.Close()



