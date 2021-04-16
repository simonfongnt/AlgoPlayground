from lib.dataMisc import dataClass
from lib.hubCore import *

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class AlgoData(
            dataClass,
            Thread,
            # Process,
               ):

    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name
    def __init__(
        self,
        itag,
        otag,
        thQueue,
        # mpQueue,
        logPath,
        libroot,
        rawroot,
        dataroot,
        miscroot,
        ):
        self.thQueue   = thQueue
        # self.mpQueue   = mpQueue

        dataClass.__init__(
                self,
                itag,
                otag,
                logPath,
                libroot,
                rawroot,
                dataroot,
                miscroot,
                )
        Thread      .__init__(self)
        # Process      .__init__(self)
    # parse the incoming commands
    def parse(
            self,
            cmds,
            ):
        for i in range(len(cmds)):
            if not isinstance(cmds[i], str):
                continue
            if      cmds[i] == '-h':
                cmds[i] = 'help'
            elif    cmds[i] == '-M':
                cmds[i] = 'modules'
            elif    cmds[i] == '-m':
                cmds[i] = 'module'
            elif    cmds[i] == '-R':
                cmds[i] = 'raws'
            elif    cmds[i] == '-r':
                cmds[i] = 'raw'
            elif    cmds[i] == '-I':
                cmds[i] = 'info'
            elif    cmds[i] == '-s':
                cmds[i] = 'save'
            elif    cmds[i] == '-L':
                cmds[i] = 'list'
            elif    cmds[i] == '-l':
                cmds[i] = 'load'
            elif    cmds[i] == '-t':
                cmds[i] = 'to'
            elif    cmds[i] == '-c':
                cmds[i] = 'create'
        return cmds

    def cycle(self):
        try:
            # route messages
            if len(self.cmddict.keys()):
                cKey = sorted(self.cmddict.keys())[0]
                cmds = self.cmddict[cKey]
                self.cmddict.pop(cKey, None)
                cmds = self.parse(cmds)
                if (0):
                    pass
                # Help
                elif (
                        isinstance(cmds[-1], str)
                    and (
                            cmds[-1] == 'help'
                            )
                        ):
                    topic = cmds[-1]
                    if len(cmds) > 1:
                        topic = cmds[-2]
                    module = self.data
                    self.Help(
                        topic,
                        module,
                        )
                # list modules/packages
                elif (
                        cmds[0] == 'modules'
                        ):
                    self.modules, msg = self.List(
                                            self.modules,
                                            self.libroot,
                                            '.py',
                                            *cmds[1:]
                                            )
                    self.xprint(
                        msg,
                        )
                # import module
                elif (
                        cmds[0] == 'module'
                        ):
                    module = self.Import(
                                self.modules,
                                self.libroot,
                                *cmds[1:]
                                )
                    if module:
                        self.module = module
                        self.data = self.module.Data()
                    self.data.Config(
                        self.xprint,
                        self.miscroot,
                    )
                    self.xprint(
                        self.data.Module(),
                        )
                # info of module
                elif (
                        cmds[0] == 'info'
                        ):
                    self.xprint(
                        self.data.Info(),
                        )
                # list raw data in rawroot
                elif (
                        cmds[0] == 'raws'
                        ):
                    self.raws, msg  = self.List(
                                            self.raws,
                                            self.rawroot,
                                            None,
                                            *cmds[1:]
                                            )
                    self.xprint(
                        msg,
                        )                        
                # load data from rawroot
                elif (
                        cmds[0] == 'raw'
                        ):
                    self.Raw(
                            self.raws,
                            self.rawroot,
                            *cmds[1:]
                        ) 
                # Save
                elif (
                        cmds[0] == 'save'
                        ):
                    msg = self.Save(
                            *cmds[1:]
                            # self.dataroot,
                            # None if len(cmds) >= 1 else cmds[1],
                            # *cmds[2:]
                        )
                    self.xprint(
                        msg,
                        )
                # list data
                elif (
                        cmds[0] == 'list'
                        ):
                    self.datas, msg = self.List(
                                            self.datas,
                                            self.dataroot,
                                            None,
                                            *cmds[1:]
                                            )
                    self.xprint(
                        msg,
                        )
                # load model
                elif (
                        cmds[0] == 'load'
                        ):
                    self.datas, __ = self.List(
                                            self.datas,
                                            self.dataroot,
                                            None,
                                            *cmds[1:]
                                            )
                    self.Load(
                            self.datas,
                            self.dataroot,
                            *cmds[1:]
                        )
                # to
                elif (
                        cmds[0] == 'to'
                        ):
                    if (    # to Model
                            cmds[1] == 'model'
                            ):
                        self.toFunc(
                            'model',
                            [
                                self.x_train,
                                self.x_val,
                                self.y_train,
                                self.y_val,
                                self.data.dataPack if self.data else None,
                                ],
                        )
                    elif (  # to Test
                            cmds[1] == 'test'
                            ):
                        self.toFunc(
                            'test',
                            [
                                self.x_test,
                                self.y_test,
                                self.data.dataPack if self.data else None,
                                ],
                        )
                # Get Params
                elif (
                        cmds[0] == 'get'
                        ):
                    self.xprint(
                        self.Get(
                            cmds[1],
                            )
                        )
                # Create
                elif (
                        cmds[0] == 'create'
                        ):
                    self.Create()
                # Run
                elif (
                        cmds[0] == 'run'
                        ):
                    if len(cmds) == 2:
                        self.Import(
                            self.libdir,
                            cmds[1],
                            )
                    self.Run()
                # Pass command to data module
                else:
                    self.Command(cmds)

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

        self.xprint('%s starts'%self.filename.split('.')[0])
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

    def prompt(self):

        cmds = self.thQueue[self.itag].get()
        self.cmddict[time.time()] = cmds
        # print(cmds)
    
    def stop(self):
        # do clean up
        self.pause = True
        self.status = False
        Thread.join(self, None)