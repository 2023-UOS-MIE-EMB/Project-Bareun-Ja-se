from multiprocessing import Process, Manager
import time

'''
@기능
    Python의 List를 이용하여 C 형식의 Queue를 구현한 클래스
@ 생성자
    기본생성자 인자없음
@ 주의사항
    저장 메모리인 Q에 직접 접근 불가
'''
class cQueue:
    __queue = None

    def __init__(self):
        self.__queue = []

    def Push(self, data):
        self.__queue.append(data)
        
    def Pop(self):
        object_pop = None
        if not( self.IsEmpty()):
            object_pop = self.__queue[0]
            self.__queue = self.__queue[1:]
        return object_pop
            
    def peek(self):
        object_peek = None
        if not( self.IsEmpty()):
            object_peek = self.__queue[0]
        return object_peek

    def Size(self) -> int : 
        return len(self.__queue)
            
    def IsEmpty(self):
        return self.Size() == 0

    def PrintAll(self):
        for i in self.__queue:
            print(i)
            
    def Clean(self):
        __queue = []