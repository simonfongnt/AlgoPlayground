# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 19:09:19 2018

@author: SF
"""
import os
import sys
import importlib
import datetime
import time
import requests
import logging
import json
import pandas as pd
import re

import threading
from threading import Thread
# from multiprocessing import Process, Manager
import ctypes

#%%
class Logger():
    def __init__(self, name, path):
        # Gets or creates a logger
#        self.logger = logging.getLogger(__name__)  
        self.logger = logging.getLogger(name)  
#        self.logger.propagate = False
        # define file handler and set formatter
        file_handler = logging.FileHandler(
                                        path,
                                        mode='w',
                                        )
        formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        # add file handler to logger
        self.logger.addHandler(file_handler)
        # set log level
#        self.logger.setLevel(logging.INFO)#logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        
    def var2str(self,   *text):
        return ' '.join(str(x) for x in [*text])    
        
    def debug(self,     *text):
        self.logger.debug       ('\n' + self.var2str(*text))
        
    def info(self,      *text):
        self.logger.info        ('\n' + self.var2str(*text))
        
    def warning(self,   *text):
        self.logger.warning     ('\n' + self.var2str(*text))
        
    def error(self,     *text):
        self.logger.error       ('\n' + self.var2str(*text))
        
    def critical(self,  *text):
        self.logger.critical    ('\n' + self.var2str(*text))
        
    def exception(self, *text):
        self.logger.exception   ('\n' + self.var2str(*text))
        
class HubBase():
    def __init__(
        self,
        ):

        self.module     = None
        self.modules    = {}
        try:
            self.modules    = self.initDict(
                                    self.modules,
                                    self.libroot,
                                    '.py',
                                )
        except Exception:
            pass
        self.libname    = None
        self.libpath    = None
        self.libloc     = None

        self.prevParams = {}

        # Help Info
        self.helpfname  = 'help.json'
        self.helpinfo   = {}
        helppath = os.path.join(
                self.libroot,
                self.helpfname,
            )
        with open(helppath) as f:
            self.helpinfo = json.load(f)

        self.ioText = ''

    # convert variable to string format
    def var2str(self, *text):
        # # print(
        # #     text[0],
        # # )
        # try:
        #     # msg = str(text[0]) + '\n'
        #     # msg = msg + ' '.join(str(x) for x in [text[1]])
        #     return ' '.join(str(x) for x in [text[1]])
        # except Exception:
        #     return ' '.join(str(x) for x in [*text])
        return ' '.join(str(x) for x in [*text])
        
    # Print to console and telegram
    def xprint(self, *text):
        # save to log
        self.logger.info(*text)
        # transmit to telegram
        self.thQueue[self.otag].put(self.var2str(*text))
        # self.mpQueue[self.otag].put(self.var2str(*text))

    # rountine to compute text to telegram
    def ResetioText(self):
        self.ioText = ''
        
    def AddioText(self, *text):
        try:
            self.ioText = self.ioText + self.var2str(*text) + '\n'
            return True
        except Exception as e:
            self.logger.exception(
                self.itag,
                sys._getframe().f_code.co_name,  
                e
                )
#            print (self.itag, 'addioText', e)
            return False
    
    def GetioText(self):
        return self.ioText

    def Help(
        self,
        topic,
        module = None,        
        ):
        msg = ''
        if topic in self.helpinfo:
            for line in self.helpinfo[topic]:
                msg = msg + line + '\n'
        if module:
            msg = msg + module.Help(topic)
        self.xprint(msg)


    def GetthID(self):  
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

    def Kill(self):
        thID = self.GetthID()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thID),
                ctypes.py_object(SystemExit)
                )
        if res == 0:
            raise ValueError("invalid thread id")
        if res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thID, 0)
            print('Exception raise failure')

    def saveParams(
        self,
        func,
        param,
        val,
        ):
        if func not in self.prevParams:
            self.prevParams[func] = {}
        self.prevParams[func][param] = val

    def loadParams(
        self,
        func,
        param,
        ):
        return self.prevParams[func][param]

    def rwParams(
        self,
        classname,
        funcname,
        paramname,
        val,
        ):
        
        if classname not in self.prevParams:
            self.prevParams[classname] = {}
        if funcname not in self.prevParams[classname]:
            self.prevParams[classname][funcname] = {}
        if paramname not in self.prevParams[classname][funcname]:
            self.prevParams[classname][funcname][paramname] = None
        if (
                (
                    isinstance(val, pd.DataFrame)
                and val is not None
                    )
            or  (
                    not isinstance(val, pd.DataFrame)
                and val
                    )
                ):
            self.prevParams[classname][funcname][paramname] = val

        return self.prevParams[classname][funcname][paramname]


    def initDict(
        self,
        theDict,
        rootdir,
        fext = None,
        ):
        # initialize dict for directory
        if rootdir not in theDict:
            theDict[rootdir] = {}
        arr = os.listdir(rootdir)
        i = 0
        for j in range(len(arr)):
            if (    # show all file extension
                    not fext
                    # show only this file extension
                or  arr[j].endswith(fext)
                    ):
                theDict[rootdir][i] = os.path.join(
                                            rootdir,
                                            arr[j],
                                            )
                i = i + 1
        return theDict
    
    def getPath(       
        self, 
        theDict,
        rootdir,
        *arg,
        ):
        # assert existance
        thePath = None
        try:
            choice = int(arg[-1])
            path = os.path.join(
                        rootdir,
                        *arg[:-1]
                        )
            thePath = theDict[path][choice]
        except Exception as e:
            # self.logger.exception(
            #     self.itag,
            #     sys._getframe().f_code.co_name,
            #     arg,
            #     e,
            # )
            try:
                thePath = os.path.join(
                            rootdir,
                            *arg
                            )
            except Exception as ee:
                pass
                # self.logger.exception(
                #     self.itag,
                #     sys._getframe().f_code.co_name,
                #     arg,
                #     ee,
                # )
        # self.logger.debug(
        #     self.itag,
        #     sys._getframe().f_code.co_name,
        #     'thePath',
        #     thePath,
        # )
        return thePath

    def List(
        self,
        theDict,
        rootdir,
        fext,
        *arg,
        ):
        rootdir = self.getPath(
                            theDict,
                            rootdir,
                            *arg,
                        )
        if not rootdir:
            return
        # refresh dict
        theDict   = self.initDict(
            theDict,
            rootdir,
            fext,
        )
        # construct msg
        msg = rootdir + ':\n'
        for i in range(len(theDict[rootdir].keys())):
            msg = msg + str(i) + ':' + theDict[rootdir][i] + '\n'
        return theDict, msg
    
    def Import(
        self,
        theDict,
        rootdir,
        *arg,
        ):
        sts = time.time()
        libpath = self.getPath(
                            theDict,
                            rootdir,
                            *arg,
                        )
        # assert
        libloc = libpath
        if (
                libloc[-3:] == '.py'
            ):
            libloc = libloc[:-3]
        libloc = libloc.replace(
            os.sep,
            '.',
        )
        libname = None
        if (
                libpath != rootdir
                ):
            libname = libloc.split('.')[-1]
        try:
            if (    # load with new file path
                    libloc
                and libname
                and libname != self.libname
                ):
                self.logger.debug(
                    self.itag,
                    sys._getframe().f_code.co_name,
                    'new lib:',
                    libname,
                )
                # assert
                importlib.invalidate_caches()
                module = importlib.import_module(libloc)
                
                # success then update the path
                self.libpath = libpath
                self.libloc  = libloc
                self.libname = libname
            else:
                self.logger.debug(
                    self.itag,
                    sys._getframe().f_code.co_name,
                    'reload lib:',
                    self.libname,
                )
                importlib.invalidate_caches()
                module = importlib.reload(self.module)
            # self.dataset = self.module.Dataset()
            self.logger.debug(
                self.itag,
                sys._getframe().f_code.co_name,
                'took',
                str(time.time() - sts) + 's',
            )
            return module
        except Exception as e:
            self.xprint(
                self.itag,
                sys._getframe().f_code.co_name,
                libdir,
                libname,
                e,
            )

