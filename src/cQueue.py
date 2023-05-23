from multiprocessing import Process, Manager
import time

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