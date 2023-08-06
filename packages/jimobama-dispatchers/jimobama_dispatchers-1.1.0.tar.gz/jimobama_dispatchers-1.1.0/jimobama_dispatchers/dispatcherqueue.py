import threading
from jimobama_dispatchers.dispatcheroperation import DispatcherOperation
import queue


class DispatcherQueue(object):

    def __init__(self):
        self.__queue = queue.Queue()
        self.__queueLocker = threading.Lock()

    @property
    def IsEmpty(self):
        return self.__queue.empty()

    @property
    def Count(self):
        return self.__queue.qsize()

    def Enqueue(self, operation: DispatcherOperation):
        try:
            self.__queueLocker.acquire()
            if(isinstance(operation, DispatcherOperation) != True):
                raise TypeError(
                    "@Enqueue: expecting a DispatcherOperation but {0} was given".format(type(operation)))
            self.__queue.put(operation)
        finally:
            self.__queueLocker.release()

    def Dequeue(self):
        operation = None
        try:
            self.__queueLocker.acquire()
            if(self.Count > 0):
                operation = self.__queue.get()
        finally:
            self.__queueLocker.release()
        return operation
