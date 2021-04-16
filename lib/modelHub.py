from lib.modelMisc import modelClass
from lib.hubCore import *

class AlgoModel(
            modelClass,
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
        modelroot,
        distroot,
        miscroot,
        ):
        self.thQueue   = thQueue
        # self.mpQueue   = mpQueue

        modelClass.__init__(
                self,
                itag,
                otag,
                logPath,
                libroot,
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
            elif    cmds[i] == '-C':
                cmds[i] = 'create' 
            elif    cmds[i] == '-c':
                cmds[i] = 'compile' 
            elif    cmds[i] == '-f':
                cmds[i] = 'fit'
            elif    cmds[i] == '-t':
                cmds[i] = 'to'
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
                    module = self.model
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
                        self.model = self.module.Model()
                    self.model.Config(
                        self.xprint,
                        self.miscroot,
                    )
                    self.xprint(
                        self.model.Module(),
                        )
                # info of module
                elif (
                        cmds[0] == 'info'
                        ):
                    self.xprint(
                        self.model.Info(),
                        )
                # Save
                elif (
                        cmds[0] == 'save'
                        ):
                    self.Save(
                            self.modelroot,
                            None if len(cmds) == 1 else cmds[1],
                        )
                # list dataset
                elif (
                        cmds[0] == 'list'
                        ):
                    self.datasets, msg = self.List(
                                            self.models,
                                            self.distroot,
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
                    self.Load(
                            self.models,
                            self.distroot,
                            *cmds[1:]
                        )
                elif (
                        cmds[0] == 'model'
                        ):
                    self.Model(
                        cmds[1] if len(cmds) >= 2 and cmds[1] else self.modelroot,
                        cmds[2] if len(cmds) == 3 and cmds[2] else self.Get('modelinfo')[1],
                    )
                # Init Params
                elif (
                        cmds[0] == 'init'
                        ):
                    self.Init(
                        self.x_train,
                        self.x_val,
                        self.y_train,
                        self.y_val,
                        self.dataPack,
                        )
                # Create Model
                elif (
                        cmds[0] == 'create'
                        ):
                    self.Create(
                        *cmds[1:],
                        )
                # Compile Model
                elif (
                        cmds[0] == 'compile'
                        ):
                    self.Compile(
                        *cmds[1:],
                        )
                # Model Fit
                elif (
                        cmds[0] == 'fit'
                        ):
                    self.Fit(
                        *cmds[1:],
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
                        cmds[0] == 'dataset'
                        ):
                    self.Dataset(
                        cmds[1],
                        cmds[2],
                        cmds[3],
                        cmds[4],
                        cmds[5],
                    )
                elif (
                        cmds[0] == 'to'
                        ):
                    if (    # to Test
                            cmds[1] == 'test'
                            ):
                        self.toFunc(
                            'test',
                            [
                                self.modelroot,
                                self.Get('libname'),
                                self.model.modelPack if self.model else None,
                                ],
                            )
                # Run
                elif (
                        cmds[0] == 'run'
                        ):
                    if len(cmds) == 2:
                        self.Module(
                            self.libroot,
                            cmds[1],
                            )
                    self.Run()
                # Pass command to model module
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