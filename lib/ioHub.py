from lib.hubCore import *

# import datetime
# import sys
# import os
# import time

# from threading import Thread
# from datetime import datetime

# import pandas as pd
# import requests
        
class ioHub(
            HubBase,
            Thread,
               ):
    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name
    def __init__(
                self,
                itag,
                otag,
                mps,
                mpQueue,
                ths,
                thQueue,
                logPath,
                libroot,
                scriptroot,
                ):
        self.itag       = itag
        self.otag       = otag
        self.logPath    = logPath
        self.logger     = Logger(
                                itag, 
                                logPath % (itag + '-' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
                                )

        self.mps        = mps
        self.mpQueue    = mpQueue
        self.ths        = ths
        self.thQueue    = thQueue

        self.libroot    = libroot
        HubBase     .__init__(self)
        Thread      .__init__(self)
        self.thQueue   = thQueue        
        self.scriptroot = scriptroot
        self.__ioHubInitParam()
                
    def __ioHubInitParam(self):
        self.cmddict    = {}

        self.scripts    = {}
        self.scripts     = self.initDict(
                                self.scripts,
                                self.scriptroot,
                                '.txt',
                            )
                
    # Print to console and telegram
    def xprint(self, *text):
        now = datetime.datetime.now()
        # save to log
        self.logger.info(*text)
        # transmit to telegram
        self.thQueue[self.otag].put(
            self.var2str(*text)
            )

    def stepcmds(
            self,
            target,
            *cmds,
            ):
        # self.mpQueue[target].put(
        self.thQueue[target].put(
            cmds
        )
        self.thQueue[target].join()
        # self.mpQueue[target].join()
        if 'to' in cmds:
            time.sleep(1)
        
    def Run(
            self,
            theDict = None,
            rootdir = None,
            *arg,
            ):
        theDict = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'theDict',
                        theDict,
                    )
        rootdir = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'rootdir',
                        rootdir,
                    )
        arg     = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'arg',
                        arg,
                    )
        # choice instead of path
        thePath = self.getPath(
                            theDict,
                            rootdir,
                            *arg,
                        )
        if not thePath:
            return
        # run script step by step
        # Using readlines() 
        script = open(thePath, 'r') 
        lines = script.readlines() 
        
        count = 0
        # Strips the newline character 
        for line in lines:
            # if not line.startswith('#'):
            if bool(re.match('[a-zA-Z]', line[0])):
                while not bool(re.match('[0-9a-zA-Z]', line[-1])):
                    line = line[:-1]
                cmds = line.split(' ')
                self.stepcmds(
                    *cmds
                )
    # parse the incoming commands
    def parse(
            self,
            cmds,
            ):
        for i in range(len(cmds)):
            if      cmds[i] == '-h':
                cmds[i] = 'help'
            elif    cmds[i] == '-L':
                cmds[i] = 'list'
        return cmds

    def cycle(self):
        
        try:
            if len(self.cmddict.keys()):
                cKey = sorted(self.cmddict.keys())[0]
                cmds = self.cmddict[cKey]
                self.cmddict.pop(cKey, None)
                cmds = self.parse(cmds)
                if (0):
                    pass
                # Help
                elif (
                        cmds[0] == 'help'
                        ):
                    topic = cmds[0]
                    self.Help(topic)
                # Kill
                elif (
                        cmds[0] == 'kill'
                        ):
                    if (0):
                        pass
                    # Help
                    elif (
                            cmds[-1] == 'help'
                            ):
                        topic = cmds[-1]
                        if len(cmds) > 1:
                            topic = cmds[-2]
                        self.Help(topic)
                    elif (
                            # cmds[1] in self.mps
                            cmds[1] in self.ths
                            ):
                        # self.mps[cmds[1]].terminate()
                        # self.mps[cmds[1]] = None
                        self.ths[cmds[1]].Kill()
                        self.ths[cmds[1]] = None
                elif (
                        cmds[0] == 'script'
                        ):
                    if (0):
                        pass
                    # Help
                    elif (
                            cmds[-1] == 'help'
                            ):
                        topic = cmds[-1]
                        if len(cmds) > 1:
                            topic = cmds[-2]
                        self.Help(topic)
                    elif (
                            cmds[1] == 'list'
                            ):
                        self.scripts, msg = self.List(
                                                self.scripts,
                                                self.scriptroot,
                                                # '.cmd',
                                                '.txt',
                                                # None,
                                                *cmds[2:]
                                                )
                        self.xprint(
                            msg,
                            )
                    elif (
                            cmds[1] == 'run'
                            ):
                        self.Run(
                            self.scripts,
                            self.scriptroot,
                            *cmds[2:]
                            )
                # transfer cmds
                else:
                    # self.mpQueue[cmds[0]].put(
                    self.thQueue[cmds[0]].put(
                        cmds[1:]
                        )

#         except KeyError:
        except Exception as e:
            self.logger.exception(
                'Command `{cmds}` is unknown: ', 
                e
                )        

    # overrided threading run()                       
    def run(self):
        
        """
        Run is the main-function in the new thread. Here we overwrite run
        inherited from threading.Thread.
        """
        self.status = True
        self.pause = False
        self.Help('help')
        while self.status:        
            try:
                if self.thQueue[self.itag].empty():
                    self.cycle()
                    time.sleep(0.05)                # optional heartbeat
                else:
                    self.prompt()
                    self.thQueue[self.itag].task_done()    # unblocks prompter
            except Exception as e:
                self.logger.exception(
                        self.itag, 
                        sys._getframe().f_code.co_name,
                        e,
                        )
        raise SystemExit
            
#         Telegram Command List:
    def prompt(self):
        raws = self.thQueue[self.itag].get()
        cmds = [x.lower() for x in raws]
        # self.cmddict[time.time()] = cmds
        self.cmddict[time.time()] = raws
    
    def stop(self):
        # do clean up
        self.pause = True
        self.status = False
        Thread.join(self, None)
        
    def get(self, name):        
        return None    
    
    # set Params
    def set(self, name, val):
        return None