from typing import TypeVar, Tuple, List
import json

'''
@기능
    TCP통신 시스템에서 패킷에 관련된 사항을 전체적으로 관리하는 클래스
    패킷을 파싱하고 형식에 따라 나누어 가지고 있으며, 다양한 편의기능을 제공한다.
@ 생성자
    기본생성자 인자없음'''
class cPacketController:
    __packetContent : dict = None

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


        
        return parsingResult
    
    '''
    @기능
        패킷에 넣을 컨텐츠를 패킷 형태로 만들어줌 
    @인자
        - dataToSend : 패킷의 body에 들어갈 내용
    @ret 
        Tuple[bool, str] : [실행 성공여부, 만들어진 패킷]'''
    def MakingPacketToSendClient(self, dataToSend : dict) -> Tuple[bool, str] :
        #todo : dict to json str
        return True , dataToSend
    
    '''
    @기능
        가장 최근에 파싱한 패킷의 contents를 dictionary 형태로 return한다.
    @ret
        dictionary : 가장 최근 패킷에 들어 있었던 데이터'''
    def GetContents(self) -> dict :
        return self.__packetContent

    '''
    @기능
    @인자'''
    def __CheckingHeader(self, buf : str) -> bool :
        # 1. 첫줄 -> H, bodySize 확인
        # 2. size이용해서 Tail Header검사
        return True
    
    '''
    @기능
        json형식의 str을 
    @인자
        -buf : json형태의 str 
    @ret
        bool : true is success '''
    def __ParsingBody(self,jsons : str) -> bool:

        #<for Test>
        jsons = "{\"1\":\"10\",\"2\":\"3\"}"        #json data to test
        #buf = "[\"1\":\"10\",\"2\":\"3\"]"         #not json

        try : 
            self.__packetContent = json.loads(jsons)
            return True

        except ValueError: #parsing fail
            return False

        



  
