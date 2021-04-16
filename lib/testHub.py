from lib.testMisc   import testClass
from lib.hubCore import *

class AlgoTest(
            testClass,
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
        tmproot,
        modelroot,
        distroot,
        miscroot,
        ):
        self.thQueue   = thQueue
        # self.mpQueue   = mpQueue

        testClass.__init__(
                self,
                itag,
                otag,
                logPath,
                libroot,
                tmproot,
                modelroot,
                distroot,
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
            elif    cmds[i] == '-s':
                cmds[i] = 'save'
            elif    cmds[i] == '-L':
                cmds[i] = 'list'
            elif    cmds[i] == '-l':
                cmds[i] = 'load'
            elif    cmds[i] == '-I':
                cmds[i] = 'info'
            elif    cmds[i] == '-i':
                cmds[i] = 'init'
            elif    cmds[i] == '-r':
                cmds[i] = 'run'
            elif    cmds[i] == '-a':
                cmds[i] = 'anaylsis'
            elif    cmds[i] == '-e':
                cmds[i] = 'export'
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
                    module = self.test
                    self.Help(
                        topic,
                        module,
                        )
                # list modules
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
                        self.test = self.module.Test()
                    self.test.Config(
                        self.xprint,
                        self.miscroot,
                    )
                    self.xprint(
                        self.test.Module(),
                        )
                # info of module
                elif (
                        cmds[0] == 'info'
                        ):
                    self.xprint(
                        self.test.Info(),
                        )
                # Save
                elif (
                        cmds[0] == 'save'
                        ):
                    self.Save(
                            self.modelroot,
                            None if len(cmds) == 1 else cmds[1],
                        )
                # list model
                elif (
                        cmds[0] == 'list'
                        ):
                    self.models, msg = self.List(
                                            self.models,
                                            self.modelroot,
                                            '.py',
                                            *cmds[1:]
                                            )
                    self.xprint(
                        msg,
                        )
                # load model
                elif (
                        cmds[0] == 'load'
                        ):
                    self.Load(
                            self.models,
                            self.modelroot,
                            *cmds[1:]
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
                # Other
                elif (
                        cmds[0] == 'model'
                        ):
                    self.Model(
                        cmds[1] if len(cmds) >= 2 and cmds[1] else self.tmproot,
                        cmds[2] if len(cmds) >= 3 and cmds[2] else self.Get('modelinfo')[1],
                        cmds[3],
                    )
                elif (
                        cmds[0] == 'dataset'
                        ):
                    self.Dataset(
                        cmds[1],
                        cmds[2],
                        cmds[3],
                    )
                # Init Class
                elif (
                        cmds[0] == 'init'
                        ):
                    self.Init(
                        self.x_test,
                        self.y_test,
                        self.mPath,
                        self.dataPack,
                        self.modelPack,
                        *cmds[1:],
                    )
                # Init Class
                elif (
                        cmds[0] == 'run'
                        ):
                    self.Run(
                        *cmds[1:],
                    )
                # Export
                elif (
                        cmds[0] == 'export'
                        ):
                    self.Export(
                        self.distroot,
                        self.mName,
                        *cmds[1:],
                    )
                # Analysis model
                elif (
                        cmds[0] == 'analysis'
                        ):
                    self.Analysis(
                        *cmds[1:],
                    )
                # Pass command to Test module
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