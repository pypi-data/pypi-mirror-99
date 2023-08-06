
"""

"""
from datetime import datetime, timedelta
from jimobama_events import Event, EventHandler
from jimobama_dispatchers.dispatcherbase import DispatcherBase


class IOperationInvoker(object):

    def Invoke(self):
        raise NotImplementedError("@Invoke operation must be implemented")


class ExceptionEvent(Event):
    def __init__(self, exception: Exception):
        super().__init__("event.exception")
        self.__Exception = exception

    @property
    def Exception(self):
        return self.__Exception


class DispatcherOperationStatus(int):

    UNKNOWN = 0xFF
    SUCCESS = 0x00
    FAULT = 0x01


class DispatcherOperation(IOperationInvoker):

    def __init__(self, dispatcher: DispatcherBase, method, *args, **kwargs):
        self.__Dispatcher = None
        if(callable(method) != True):
            raise TypeError(
                "@Method: expecting a callable object but {0} given".format(type(method)))
        if(kwargs != None):
            if ((type(kwargs) != list) and
                (type(kwargs) != tuple) and
                    (type(kwargs) != dict)):
                raise TypeError(
                    "@Pareneter 2 : must be either variadic argument of list,tuple or dict")
        # check if the operation have dispatcher attached.
        self.__Dispatcher = dispatcher
        self.__method = method
        self.__kwargs = kwargs
        self.__args = args
        self.__Result = None
        self.__EnqueueTime = datetime.now()
        self.__WaitTime = None
        self.__ElapseTime = None
        self.__Completed = EventHandler()
        self.__Faulted = EventHandler()
        self.__Status = DispatcherOperationStatus.UNKNOWN

    @property
    def Status(self):
        return self.__Status

    @property
    def Dispatcher(self):
        return self.__Dispatcher

    @property
    def Completed(self) -> EventHandler:
        return self.__Completed

    @Completed.setter
    def Completed(self, handler: EventHandler):
        if(isinstance(handler, EventHandler)):
            if(handler == self.__Completed):
                self.__Completed = handler

    @property
    def Faulted(self):
        return self.__Faulted

    @Faulted.setter
    def Faulted(self, handler: EventHandler):
        if isinstance(handler, EventHandler) is True:
            if(handler == self.__Faulted):
                self.__Faulted = handler

    @property
    def EnqueueTime(self):
        return self.__EnqueueTime

    @EnqueueTime.setter
    def EnqueueTime(self, dtime: datetime):
        if(isinstance(dtime, datetime) is not True):
            raise TypeError("@EnqueueTime: expecting a datetime")
        self.__EnqueueTime = dtime

    @property
    def WaitTime(self):
        return self.__WaitTime

    @WaitTime.setter
    def WaitTime(self, value: timedelta):
        if(isinstance(value, timedelta) is not True):
            raise TypeError(
                "@WaitTime : expecting a dateime  but {0} given".format(type(value)))
        self.__WaitTime = value

    @property
    def ElapseTime(self):
        return self.__ElapseTime

    @ElapseTime.setter
    def ElapseTime(self, value: timedelta):
        if(isinstance(value, timedelta) is not True):
            raise TypeError(
                "@ElapseTime : Expecting a timedelta but {0} was given".format(type(value)))
        self.__ElapseTime = value

    @property
    def Result(self):
        return self.__Result

    def Invoke(self):
        try:
            if(callable(self.__method)):
                self.__Result = self.__method(*self.__args, **self.__kwargs)
                self.__Status = DispatcherOperationStatus.SUCCESS
                if(self.Completed != None):
                    self.Completed(Event("event.operation.completed"))
        except Exception as err:
            self._RaiseFault(err)

    def _RaiseFault(self, exception: Exception):
        self.__Status = DispatcherOperationStatus.FAULT
        if(isinstance(exception, Exception)):
            if(self.Faulted != None):
                self.Faulted(ExceptionEvent(exception))


if __name__ == "__main__":
    def TestFunction(args):
        print(args)
        return 10 * args

    def OnCompleted(evt):
        print(evt)

    def OnFail(evt):
        print(evt)
    op = DispatcherOperation(None, TestFunction, 90)
    op.Completed += OnCompleted
    op.Invoke()
    print(op.Result)
    print(op.Dispatcher)
