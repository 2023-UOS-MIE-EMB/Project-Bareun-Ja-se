from typing import TypeVar, Tuple, List
import json, io
from  utils import ConcatStr

'''
@기능
    TCP통신 시스템에서 패킷에 관련된 사항을 전체적으로 관리하는 클래스
    패킷을 파싱하고 형식에 따라 나누어 가지고 있으며, 다양한 편의기능을 제공한다.
@생성자 인자 없음'''
class cPacketManager:
    def __init__(self):
        return
    '''
    @기능
        패킷을 형식에 따라 Header, Body로 나눈다. 패킷의 유효성 검사도 동시에 진행
    @ret
        -dict : 파싱이 결과가 담김. 문제가 있었다면 None '''
    def ParsingPacket(self,packet : str ) -> dict : 
        headerSize = self.__CheckingHeader(packet)
        parsingResult = None

        if (headerSize == -1): 
            return parsingResult

        packetBody = packet[ headerSize : -4 ] #\r\n\r\n =  4 bytes 

        parsingResult =  self.__JsonsToDict(packetBody)
        return parsingResult
    
    '''
    @기능
        패킷에 넣을 컨텐츠를 패킷 형태로 만들어줌 
    @인자
        - dataToSend : 패킷의 body에 들어갈 내용
    @ret 
        Tuple[bool, str] : [실행 성공여부, 만들어진 패킷]'''
    def MakingPacketToSend(self, dataToSend : dict) -> Tuple[bool, str] :
        
        packetList = []

        packetBody = json.dumps(sendingContent, indent = 0)
        packetBody = packetBody.replace(' ','') #body

        bodySize = len(packetBody)
        
        packetHeader = ConcatStr("H:",bodySize) #header

        packetList.append(packetHeader)
        packetList.append(packetBody)
        packetList.append("\r\n") #tail header

        dataToSend = ConcatStr('',packetList, "\r\n")

        return True , dataToSend
    
    '''
    @기능
        패킷의 헤더를 읽고 패킷의 유효성 검사 이후 헤더 사이즈를 반환
    @인자
        -packet : whole packet
    @ret
        int :  header size, if packet is abnormal, returns -1'''
    def __CheckingHeader(self, packet : str) -> int :
        headerSize = -1
        # 1. 첫줄 -> H, bodySize 확인
        buf = io.StringIO(packet)
        firstLine = buf.readline()

        # 2. size이용해서 Tail Header검사

        return headerSize
    
    '''
    @기능
        json형식의 str을 dict로 변환하여 리턴
    @인자
        -buf : json형태의 str 
    @ret
        dict : if None, it is failed '''
    def __JsonsToDict(self,jsons : str) -> dict:
        results  = None
        try : 
            results = json.loads(jsons)
            return results

        except ValueError: #parsing fail
            return None

        



  
'''test code '''

if __name__ == '__main__':
    packetManager = cPacketManager()

    sendingContent = { "1" : "10", "2" : "3" }
    rsult, packetBody = packetManager.MakingPacketToSend(sendingContent)
    print(packetBody)
    print("end")