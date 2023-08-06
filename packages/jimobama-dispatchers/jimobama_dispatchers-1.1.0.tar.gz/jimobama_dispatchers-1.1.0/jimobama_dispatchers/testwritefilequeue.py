if(__name__ == "__main__"):
    from jimobama_dispatcher.dispatcher import Dispatcher
    import os
    import io
    import threading
    import time
    from datetime import datetime

    total_jobs = 0
    FILE_DATA = "data.txt"
    TERMINATE = False

    def read():
        try:
            last_result = 0
            if(os.path.exists(FILE_DATA) is not True):
                with open(FILE_DATA, mod='w') as file:
                    pass
            else:
                with open(FILE_DATA, mode='r') as file:
                    file.seek(0, io.SEEK_END)
                    size = file.tell()
                    if(size <= 0):
                        size = 0
                    else:
                        size = size - 1

                    file.seek(size, io.SEEK_SET)
                    last_result = file.read()
                    if(last_result == '\n'):
                        last_result = file.read()
            return last_result
        except Exception as err:
            print("Read Error : {0} ".format(err))
            raise err

    def write(result):
        size = 0
        try:
            if(os.path.exists(FILE_DATA) is True):
                with open('data.txt', mode='a') as file:
                    file.write('{0}\n'.format(str(result)))
                    file.seek(0, io.SEEK_END)
                    size = file.tell()
        except Exception as err:
            print("Write Error : {0}".format(err))
            raise err
        return size

    def Task1():
        print("Start... Task")

    def Task2(a, b):
        value = read()
        if(value == '' or value == None):
            value = '0'
        result = int(value)
        for i in range(0, 10000):
            result += (a + b)
        size = write(result)
        return [result, size]

    def ExternalRun(dispatcher):
        a = 1
        while(TERMINATE != True):
            dispatcher.Invoke(Task2, a,  10)
            a = a + 1

    dispatcher = Dispatcher.CreateInstance()

    dispatcher.Invoke(Task1)
    dispatcher.Invoke(Task2, 5, 6)
    print(dispatcher.Thread)
    for i in range(0, 2):
        t = threading.Thread(target=ExternalRun, args=(dispatcher,))
        t.daemon = True
        t.start()

    totaltime = datetime.now() - datetime.now()
    while(TERMINATE != True):
        try:
            op = dispatcher.Run()
            if(op == None):
                continue
            if(op.Result == None):
                continue
            total_jobs += 1
            totaltime = op.ElapseTime + totaltime
            print("Time Created:{0},Result= {1},Total Process time={2},Jobs ={3},file-size ={4},Queue Size ={5},Wait Time{6}".format(op.ElapseTime,
                                                                                                                                     op.Result[
                                                                                                                                         0],
                                                                                                                                     totaltime,
                                                                                                                                     total_jobs, op.Result[1], dispatcher.Count, op.WaitTime))
            pass
        except Exception as err:
            TERMINATE = True
            time.sleep(2)
            print(err)
