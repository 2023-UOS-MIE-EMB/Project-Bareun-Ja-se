from multiprocessing import Manager
class cQueue():
    __manager = Manager()
    def __init__(self):
        self.queue = self.__manager.list([])

    def Push(self, data):
        self.queue.append(data)
        
    def Pop(self):
        object_pop = None
        if not( self.isEmpty()):
            object_pop = self.queue[0]
            self.queue = self.queue[1:]
        return object_pop
            
    def peek(self):
        object_peek = None
        if not( self.isEmpty()):
            object_peek = self.queue[0]
        return object_peek
            
    def isEmpty(self):
        return len(self.queue) == 0