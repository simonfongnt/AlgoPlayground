from lib.hubCore import *

class modelClass(
            HubBase,
               ):

    def __init__(
        self,
        itag,
        otag,
        logPath,
        libroot,
        modelroot,
        distroot,
        miscroot,
        ):
        self.itag       = itag
        self.otag       = otag
        self.logger     = Logger(
                                itag, 
                                logPath % (itag + '-' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
                                )

        self.libroot    = libroot
        self.modelroot  = modelroot
        self.distroot   = distroot
        self.miscroot   = miscroot

        HubBase     .__init__(self)
        self.__initParam()

    def __initParam(self):
        self.cmddict    = {}

        self.savepath   = None

        self.x_train    = None
        self.y_train    = None
        self.x_val      = None
        self.y_val      = None
        self.dataPack   = None

        self.models     = {}
        self.models     = self.initDict(
                                self.models,
                                self.modelroot
                            )
        self.models     = self.initDict(
                                self.models,
                                self.distroot
                            )

        self.mPath      = None
        self.mName      = None
        self.model      = None
        self.history    = None
    
    def Command(
        self,
        cmds,
        ):
        if self.model:
            self.model.Command(cmds)

    def Save(
        self,
        root = None,
        name = None,
        ):
        if not root:
            root = self.modelroot
        if not name:
            name = self.libname
        self.savepath = os.path.join(
                        root,
                        name,
                        )
        self.model.Save(
            self.savepath,
        )

    def Load(
        self,
        theDict,
        rootdir,
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
        path = thePath.split(
                    os.sep,
                )
        root = os.sep.join(path[:-1])
        name = path[-1]
        self.Model(
                root,
                name,
            )
    
    def Model(
        self,
        root,
        name,
        ):
        root = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'root',
                        root,
                    )
        name = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'name',
                        name,
                    )
        try:
            path = os.path.join(
                        root,
                        name,
                        )
            self.model.Load(
                path,
            )
            self.mPath      = path
            self.mName      = name
        except Exception as e:
            self.logger.exception(
                self.itag,
                sys._getframe().f_code.co_name,
                root,
                name,
                e,
            )

    def Dataset(
        self,
        x_train,
        x_val,
        y_train,
        y_val,
        dataPack,
        ):
        self.x_train    = x_train
        self.x_val      = x_val
        self.y_train    = y_train
        self.y_val      = y_val
        self.dataPack   = dataPack
        self.model.Dataset(
            self.x_train,
            self.x_val,
            self.y_train,
            self.y_val,
            self.dataPack,
        )

    def Get(
        self,
        cmd,
        ):
        if   cmd.lower() == 'libname':
            return self.libname
        elif cmd.lower() == 'path':
            return self.libpath, self.savepath
        elif cmd.lower() == 'model':
            return self.model

    def Set(
        self,
        cmd,
        *arg,
        ):
        if   cmd.lower() == 'libname':
            self.libname   = arg[0]
        # elif cmd.lower() == 'dataset':
        #     self.Dataset(
        #         arg[0],
        #         arg[1],
        #         arg[2],
        #         arg[3],
        #         arg[4],
        #     )
        self.xprint(
            self.itag,
            sys._getframe().f_code.co_name,
            cmd,
        )

    def toFunc(
        self,
        func,
        argv,
        ):
        # self.mpQueue[func].put([
        self.thQueue[func].put([
            'model',
            *argv,
            ])
        # self.mpQueue[func].join()
        self.thQueue[func].join()

    def Init(
        self,
        x_train,
        x_val,
        y_train,
        y_val,
        dataPack,
        ):
        self.model.Init(
            x_train,
            x_val,
            y_train,
            y_val,
            dataPack,
        )

    def Create(
        self, 
        *arg,       
        ):
        self.model.Create(
            *arg,
            )

    def Compile(
        self, 
        *arg,       
        ):
        self.model.Compile(
            *arg,
            )

    def Fit(
        self,
        *arg,
        ):
        sts = time.time()
        self.msg = self.model.Fit(
            *arg,
        )
        self.Save(
            self.modelroot,
        )
        self.xprint(
            self.itag,
            sys._getframe().f_code.co_name,
            'took',
            str(time.time() - sts) + 's',
        )

    # def Run(
    #     self,
    #     ):
    #     sts = time.time()
    #     self.Init(
    #         self.x_train,
    #         self.x_val,
    #         self.y_train,
    #         self.y_val,
    #         self.dataPack,
    #     )
    #     self.Create()
    #     self.Compile()
    #     self.Fit()
    #     self.toFunc(
    #         'test',
    #         [
    #             self.modelroot,
    #             self.Get('libname'),
    #             self.model.modelPack if self.model else None,
    #             ],
    #         )
    #     self.xprint(
    #         self.itag,
    #         sys._getframe().f_code.co_name,
    #         'took',
    #         str(time.time() - sts) + 's',
    #     )