
import threading
import time
from datetime                                 import datetime
from jimobama_dispatchers.dispatcherbase      import DispatcherBase
from jimobama_dispatchers.dispatcheroperation import DispatcherOperation
from jimobama_dispatchers.dispatcherqueue     import DispatcherQueue


class Dispatcher:

    __dispatchers = list()

    @staticmethod
    def CreateInstance(dispatching_thread: threading.Thread = None):
        thread = dispatching_thread if (isinstance(
            dispatching_thread, threading.Thread) is True) else threading.current_thread()
        result = None
        for dispatcher in Dispatcher.__dispatchers:
            if(dispatcher.Thread == thread):
                result = dispatcher
                break
        if(result is None):
            # create a dispatcher with the given thread.
            result = Dispatcher.__Dispatcher(thread)
            Dispatcher.__dispatchers.append(result)
        return result

        @staticmethod
        def Count():
            return len(Dispatcher.__dispatchers)

    def __init__(self):
        raise NotImplementedError("@Dispatcher does not have a constructor")

    """
    """
    class __Dispatcher(DispatcherBase):

        def __init__(self, thread):
            super().__init__()
            self.__currentThread = thread
            self.__DispatcherQueue = DispatcherQueue()
            self.__Freezed = False
            self.__WaitEvent = threading.Event()

        def Invoke(self, method, *args, **kwargs) -> DispatcherOperation:
            operation = None
            if(callable(method) is True):
                operation = DispatcherOperation(self, method, *args, **kwargs)
                operation.EnqueueTime = datetime.now()
                self.__DispatcherQueue.Enqueue(operation)
                self.__WaitEvent.set()
            return operation

        @property
        def Count(self):
            return self.__DispatcherQueue.Count

        def Wait(self):
            if(self.Count <= 0):
                self.__WaitEvent.wait()

        def Run(self):
            operation = None
            if(self.CheckAccess() != True):
                raise ValueError(
                    "@Run Method : must be called on the same thread that create the dispatcher instance")
            try:
                if(self.__DispatcherQueue.IsEmpty is not True):
                    operation = self.__DispatcherQueue.Dequeue()

                    if(operation != None):
                        currentTime = datetime.now()
                        operation.WaitTime = currentTime - operation.EnqueueTime
                        operation.Invoke()
                        operation.ElapseTime = datetime.now() - currentTime

            except Exception as err:
                raise err
            return operation

        def CheckAccess(self):
            return (threading.current_thread().ident == self.Thread.ident)

        @property
        def Thread(self):
            return self.__currentThread


if(__name__ == "__main__"):
    def TestA():

        print("Testing dispatcher")

    def OnFault(event):
        print(event.Exception)

    dispatcher = Dispatcher.CreateInstance()
    opRaw = dispatcher.Invoke(TestA)
    opRaw.Faulted += OnFault
    print(opRaw)
    dispatcher.Wait()
    op = dispatcher.Run()
    print(op.Status)
