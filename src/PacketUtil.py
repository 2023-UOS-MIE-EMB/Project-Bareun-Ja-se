from typing import TypeVar, Tuple, List

class cPacketController:
    __body : dict = None

    def __init__(self):
        return

    def ParsingPacket(self,buf : str ) -> bool : 
        if(self.__CheckingHeader(buf) == False):
            return False

        if(self.__ParsingBody(buf) == False):
            return False

        return True


    #todo : making Packet with streaming addr
    def MakingPacketToSendClient(self, streamingAddr : str) -> Tuple[bool, str] :
        return True , streamingAddr

    def GetBody(self) -> dict :
        return self.__body

    def __CheckingHeader(self, buf : str) -> bool :
        # 1. ù�� -> H, bodySize Ȯ��
        # 2. size�̿��ؼ� Tail Header�˻�
        return True

    def __ParsingBody(self,buf : str) -> bool:
        self.__body = { "key" : 10}

        return True



  
