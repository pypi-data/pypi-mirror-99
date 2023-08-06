import threading ;
import jimobama_events  as events
import time;



"""
  A simple utils for FPS
  
 
"""
class FPSTimer(object):

    class FPSEvent(events.Event):
        def __init__(self,**kwargs ):
            super().__init__("FPSEvent.Render");
            self.frame_counts  =  kwargs['frame_counts'] if('frame_counts' in kwargs) else 0;
            self.period        =  kwargs['period']       if('period' in kwargs)   else 0;
            
    class FPSError(events.Event):
        def __init__(self, err:Exception):
            super().__init__("FPSEvent.Error");
            self.__err =  err;

        @property
        def Error(self):
            return self.__err;
            
    class FPSLocker(object):

        def __init__(self, locker):
            self.__locker = locker;
            self.__locker.acquire();
        
        def __del__(self):
            self.__locker.release();

    def __init__(self, frequency : int = 60):
        self.ticked         = events.EventHandler();
        self.cycled         = events.EventHandler();
        self.failed         = events.EventHandler();
        self.__timerThread  =  None
        self.__started       =  False;
        self.__threadLocker  =  threading.Lock();
        self.__StartEvent    =  threading.Event();
        self.__frequence     =  frequency;
        self.__period_in_seconds  =  1/ self.__frequence;
        self.__fps_count          =  0;
        self.__elapse_seconds_fps = 0; 
        self.__perf_frequence     =  10000;
        self.__WaitForeverEvent   = threading.Event();

    @property
    def frequency(self):
        return self.__frequence;
    @property
    def elapse_seconds_fps(self):
        return self.__elapse_seconds_fps;

    @property
    def fps_count(self):
        return self.__fps_count;

    @property
    def period(self):
        """
         return : period in seconds.
        """
        return self.__period_in_seconds;

    def __create_thread(self):
        timerThread  =  threading.Thread(target=self.__run_in_background, name="FPSRenderThread");
        timerThread.daemon = True;
        return timerThread;

    def __run_in_background(self):
        __NS_IN_SECONDS  = 1000000000;
        self.__started   = True;
        self.__StartEvent.set();
        elapse_time        = 0;
        start_time         = time.perf_counter();
        frame_count        =  0;
        total_elapse_time  =  0;

        while(self.started):
            try:
                if(elapse_time < self.period):
                    now_time    =  time.perf_counter();
                    delta       =  (now_time - start_time)  ;
                    elapse_time =  elapse_time + delta
                    start_time  =  now_time;
                    continue;
                start_time              = time.perf_counter();
                frame_count             = frame_count + 1;
                total_elapse_time       = total_elapse_time + elapse_time
                
                # request render per the frame time
                event_args  =  self.FPSEvent(frame_counts=frame_count, period= elapse_time);
                self.ticked(event_args); 
               
                if(total_elapse_time >= 1):
                    #Trigger FrameCount event per the number of frames per seconds.
                    self.__fps_count          = frame_count;
                    self.__elapse_seconds_fps = total_elapse_time;
                    event_args  =  self.FPSEvent(frame_counts=frame_count, period= self.elapse_seconds_fps);
                    self.cycled(event_args);
                    frame_count = 0;   
                    total_elapse_time = 0;         
                elapse_time =  0;
            except Exception as err:
                 self.failed(self.FPSError(err));
                 self.stop();

    @property
    def started(self):
        return self.__started;

    def stop(self):
        self.FPSLocker(self.__threadLocker);
        if(self.started is True):
            self.__started = False;
            if(self.__timerThread is not None)  and (self.__timerThread.is_alive() is True):
                #wait until the thread is terminated.
                if(self.__timerThread.ident != threading.current_thread().ident):
                    self.__timerThread.join(1);
            self.__timerThread = None;
        self.__WaitForeverEvent.set();

    def start(self):
        self.FPSLocker(self.__threadLocker);
        if(self.started):
            return ;
        self.__timerThread = self.__create_thread();
        self.__timerThread.start();
        self.__StartEvent.wait();

    def wait_forever(self):
        self.__WaitForeverEvent.wait();
        



if(__name__ =="__main__"):
    data  =  0;
    arr  = list();
    locker  =  threading.Lock();
 

    def cycled(evt):
        FPSTimer.FPSLocker(locker)
        print( "Cycled  =  {0} , frequency ={1}".format(evt.period, evt.frame_counts))

    def write(evt):
        FPSTimer.FPSLocker(locker)
        global data;
        data = data + 1;
   

    fpsDSP          =  FPSTimer(frequency=2048);
    fpsDSP.ticked    +=write;
    fpsDSP.cycled    +=cycled;
    
   
    fpsDSP.start();
    
    fpsDSP.wait_forever();
     
        

   

