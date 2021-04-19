import os, sys
clientDir = os.path.abspath(sys.argv[0] + "/..")
# print(os.getcwd())
os.chdir(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))

import time
import logging
# from queue import Queue
import queue
from threading import Thread
import subprocess
import datetime
import json
import pandas as pd
import datetime
from dateutil import tz
import signal
import multiprocessing
from multiprocessing import Process, Manager, freeze_support

#%%
class prompter(Thread):
    """Prompt user for command input.
    Runs in a separate thread so the main-thread does not block.
    """
    def __init__(
            self, 
            thQueue,
            itag, 
            otag,
            ):
        super().__init__()
        self.thQueue   = thQueue
        self.itag       = itag
        self.otag       = otag

    def run(self):
        target = None
        self.status = True
        while self.status:
            cmds = input('> ').split(' ')
            self.thQueue[self.otag].put(cmds)
            self.thQueue[self.otag].join()  # blocks until consumer calls task_done()
                
    def stop(self):
        self.status = False
        Thread.join(self, None)
    # set Params
    def set(self, name, val):
        return None

#%%
def main(
        argv
        ):
    from lib.tgApi      import tgApi
    from lib.ioHub      import ioHub
    from lib.dataHub    import AlgoData
    from lib.modelHub   import AlgoModel
    from lib.testHub    import AlgoTest

    pathJson    = json.load(
                        open(
                            os.path.join(
                                'config', 
                                'path.json',
                                ),
                            )
                        )
    loginJson = json.load(
                        open(
                            os.path.join(
                                clientDir, 
                                pathJson['login']
                                ),
                            )
                        )
    logPath = os.path.join(
                        clientDir, 
                        *pathJson['logpath'],
                        )
    
    # multiprocess
    manager = Manager()
    mpcmds = {}
    mpparams = {}
    mps = {}

    # initialize thread channels
    thcmds = {}
    thcmds['main']      = queue.Queue() 
    # prepare threadings
    ths = {}   

    # mpcmds  ['data']    = multiprocessing.JoinableQueue()
    # mps['data']         = None
    thcmds['data']   = queue.Queue()
    ths['data']      = None
    


    # mpcmds  ['model']   = multiprocessing.JoinableQueue()
    # mps['model']        = None
    thcmds['model']     = queue.Queue() 
    ths['model']        = None


                                    
    # mpcmds  ['test']    = multiprocessing.JoinableQueue()
    # mps['test']         = None
    thcmds['test']      = queue.Queue() 
    ths['test']         = None

    # # initialize thread channels
    # thcmds = {}
    # thcmds['main']      = queue.Queue() 
    # # prepare threadings
    # ths = {}   

    thcmds['cli']       = queue.Queue() 
    ths['cli']          = prompter      (
                                    thQueue    = thcmds,
                                    itag        = 'cli',  
                                    otag        = "ioHub",
                                    )
    thcmds['tgApi']     = queue.Queue() 
    mpcmds['tgApi']     = multiprocessing.JoinableQueue()
    ths['tgApi']        = tgApi(
                                    thQueue     = thcmds, 
                                    mpQueue     = mpcmds, 
                                    enable      = loginJson['telegram']['Enable'],
                                    token       = loginJson['telegram']['token'],
                                    botname     = loginJson['telegram']['botname'], 
                                    authgroup   = loginJson['telegram']['authgroup'],
                                    itag        = "tgApi",
                                    otag        = "ioHub",
                                    )
    thcmds['ioHub']     = queue.Queue() 
    ths['ioHub']        = ioHub        (
                                    itag        = 'ioHub',
                                    otag        = "tgApi",
                                    logPath     = logPath,
                                    mps         = mps,
                                    mpQueue     = mpcmds,
                                    ths         = ths,
                                    thQueue     = thcmds,
                                    libroot     = os.path.join(
                                                    *pathJson['ioHub']['libroot'],
                                                    ),
                                    scriptroot  = os.path.join(
                                                    *pathJson['ioHub']['scriptroot'],
                                                    ),
                                    )
    # # prepare processings
    # for key, mp in mps.items():
    #     mp.daemon = True
    #     mp.start()
    # initialize threadings
    for key, th in ths.items():
        try:
            th.daemon = True
            th.start()
        except Exception:
            pass

    # thcmds['tgApi'].put('client starts')

    while True: 
        # thists = datetime.datetime.now().timestamp()
        # start / restart?
        # if not mps['data']:
        #     mps['data']      = AlgoData(
        #                                     mpQueue     = mpcmds,
        if not ths['data']:
            ths['data']      = AlgoData(
                                            thQueue    = thcmds,
                                            itag        = 'data',  
                                            otag        = "tgApi",
                                            logPath     = logPath,
                                            libroot     = os.path.join(
                                                            *pathJson['data']['libroot'],
                                                            ),
                                            rawroot     = os.path.join(
                                                            *pathJson['data']['rawroot'],
                                                            ),
                                            dataroot    = os.path.join(
                                                            *pathJson['data']['dataroot'],
                                                            ),
                                            miscroot    = os.path.join(
                                                            *pathJson['data']['miscroot'],
                                                            ),
                                            )
            # mps['data'].daemon = True
            # mps['data'].start()
            ths['data'].daemon = True
            ths['data'].start()

        # if not mps['model']:
        #     mps['model']        = AlgoModel(
        #                                     mpQueue     = mpcmds,
        if not ths['model']:
            ths['model']        = AlgoModel(
                                            thQueue    = thcmds,
                                            itag        = 'model',  
                                            otag        = "tgApi",
                                            logPath     = logPath,
                                            libroot     = os.path.join(
                                                            *pathJson['model']['libroot'],
                                                            ),
                                            modelroot   = os.path.join(
                                                            *pathJson['model']['modelroot'],
                                                            ),
                                            distroot    = os.path.join(
                                                            *pathJson['model']['distroot'],
                                                            ),
                                            miscroot    = os.path.join(
                                                            *pathJson['model']['miscroot'],
                                                            ),
                                            )
            # mps['model'].daemon = True
            # mps['model'].start()
            ths['model'].daemon = True
            ths['model'].start()

        # if not mps['test']:
        #     mps['test']         = AlgoTest(
        #                                     mpQueue     = mpcmds,
        if not ths['test']:
            ths['test']         = AlgoTest(
                                            thQueue    = thcmds,

                                            itag        = 'test',  
                                            otag        = "tgApi",
                                            logPath     = logPath,
                                            libroot     = os.path.join(
                                                            *pathJson['test']['libroot'],
                                                            ),
                                            tmproot    = os.path.join(
                                                            *pathJson['test']['tmproot'],
                                                            ),
                                            modelroot   = os.path.join(
                                                            *pathJson['test']['modelroot'],
                                                            ),
                                            distroot    = os.path.join(
                                                            *pathJson['test']['distroot'],
                                                            ),
                                            miscroot    = os.path.join(
                                                            *pathJson['test']['miscroot'],
                                                            ),
                                            )
            # mps['test'].daemon = True
            # mps['test'].start()
            ths['test'].daemon = True
            ths['test'].start()
        time.sleep(0.1)

#%%
if __name__ == '__main__':
    # Pyinstaller fix
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    freeze_support()
    # print('run client.py', clientDir)
    main(sys.argv)