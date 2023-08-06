from jimobama_dispatchers import Dispatcher


class DispatcherObject(object):

    def __init__(self, dispatcher: Dispatcher = None):
        if(dispatcher != None):
            if(isinstance(dispatcher, Dispatcher) is not True):
                raise TypeError("Expecting a dispatcher object type")
        else:
            dispatcher = Dispatcher.CreateInstance()
        self.__Dispatcher = dispatcher

    @property
    def Dispatcher(self):
        return self.__Dispatcher

    def CheckAccess(self):
        status = False
        if(self.Dispatcher != None):
            status = sellf.Dispatcher.CheckAccess()
        return status


if(__name__ == "__main__"):
    import threading as ts

    def Create():
        obj3 = DispatcherObject()
        print(obj3.Dispatcher)
        print("{0} , ".format(ts.current_thread().ident))

    obj = DispatcherObject()
    obj2 = DispatcherObject()
    print(ts.current_thread().ident)
    print(obj.Dispatcher)
    print(obj2.Dispatcher)
    print("Threading ")
    for i in range(0, 4):
        th1 = ts.Thread(target=Create)
        th1.start()
