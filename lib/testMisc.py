from lib.hubCore import *

class testClass(
            HubBase,
               ):

    def __init__(
        self,
        itag,
        otag,
        logPath,
        libroot,
        tmproot,
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
        self.tmproot    = tmproot
        self.modelroot  = modelroot
        self.distroot   = distroot
        self.miscroot   = miscroot

        HubBase     .__init__(self)
        self.__initParam()

    def __initParam(self):
        self.cmddict    = {}

        self.test       = None
        self.savepath   = None

        self.x_test     = None
        self.y_test     = None
        self.dataPack   = None
        self.modelPack  = None

        self.models     = {}
        self.models     = self.initDict(
                                self.models,
                                self.tmproot,
                                None,
                            )
        self.models     = self.initDict(
                                self.models,
                                self.modelroot,
                                None,
                            )
        self.mPath      = None
        self.mName      = None
        self.model      = None

        self.algoModels = {}
        self.algoModels = self.initDict(
                                self.algoModels,
                                self.distroot,
                                None,
                            )
        self.aPath      = None
        self.aName      = None
        self.distpath   = None
        self.algoModel  = None

        self.history    = None

    def Command(
        self,
        cmds,
        ):
        if self.test:
            self.test.Command(cmds)
    
    def Export(
        self,
        root = None,
        name = None,
        *arg,
        ):
        if not root:
            root = self.distroot,
        if not name:
            name = self.mName,
        self.distpath = os.path.join(
                        root,
                        name,
                        )
        try:
            os.makedirs(self.distpath)
        except FileExistsError:
            # directory already exists
            pass
        self.test.Export(
            self.distpath,
            *arg,
        )

    # def Import(
    #     self,
    #     theDict,
    #     rootdir,
    #     *arg,
    #     ):
    #     theDict = self.rwParams(
    #                     self.classname,
    #                     sys._getframe().f_code.co_name,
    #                     'theDict',
    #                     theDict,
    #                 )
    #     rootdir = self.rwParams(
    #                     self.classname,
    #                     sys._getframe().f_code.co_name,
    #                     'rootdir',
    #                     rootdir,
    #                 )
    #     arg     = self.rwParams(
    #                     self.classname,
    #                     sys._getframe().f_code.co_name,
    #                     'arg',
    #                     arg,
    #                 )
    #     # choice instead of path
    #     thePath = self.getPath(
    #                         theDict,
    #                         rootdir,
    #                         *arg,
    #                     )
    #     if not thePath:
    #         return
    #     path = thePath.split(
    #                 os.sep,
    #             )
    #     root = os.sep.join(path[:-1])
    #     name = path[-1]
    #     self.AlgoModel(
    #             root,
    #             name,
    #         )

    # def AlgoModel(
    #     self,
    #     root,
    #     name,
    #     ):
    #     try:
    #         path = os.path.join(
    #                     root,
    #                     name,
    #                     )
    #         self.test.Import(
    #             path,
    #         )
    #         self.aPath      = path
    #         self.aName      = name
    #     except Exception as e:
    #         self.logger.exception(
    #             self.itag,
    #             sys._getframe().f_code.co_name,
    #             root,
    #             name,
    #             e,
    #         )

    def Save(
        self,
        root = None,
        name = None,
        ):
        if not root:
            root = self.modelroot
        if not name:
            name = self.mName
        self.savepath = os.path.join(
                        root,
                        name,
                        )
        self.test.Save(
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
                None,
            )
    
    def Model(
        self,
        root,
        name,
        modelPack,
        ):
        self.modelPack = modelPack
        try:
            path = os.path.join(
                        root,
                        name,
                        )
            self.test.Load(
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
        x_test,
        y_test,
        dataPack,
        ):
        self.x_test     = x_test
        self.y_test     = y_test
        self.dataPack   = dataPack
        self.test.Dataset(
            self.x_test,
            self.y_test,
            self.dataPack,
        )

    def Get(
        self,
        cmd,
        ):
        result = None
        if   cmd.lower() == 'libname':
            result = self.libname
        elif cmd.lower() == 'path':
            result = (self.libpath, self.savepath)
        elif cmd.lower() == 'dataset':
            result = (self.x_test, self.y_test)
        elif cmd.lower() == 'modelinfo':
            result = (self.mPath, self.mName)
        elif cmd.lower() == 'algoModelinfo':
            result = (self.aPath, self.aName)

        self.xprint(result)
        return result

    def Set(
        self,
        cmd,
        *arg,
        ):
        self.xprint(
            cmd,
            arg,
        )
        if   cmd.lower() == 'libname':
            self.libname   = arg[0]
        elif cmd.lower() == 'dataset':
            self.Dataset(
                arg[0],
                arg[1],
            )
        elif cmd.lower() == 'model':
            self.Model(
                arg[0],
                arg[1],
            )

    def Init(
        self,
        *arg,
        ):
        self.test.Init(
            self.x_test,
            self.y_test,
            self.mPath,
            self.dataPack,
            self.modelPack,
            *arg,
        )
            
    def Run(
        self,
        *arg,
        ):
        sts = time.time()
        self.test.Run(
            *arg,
        )    
        self.xprint(
            self.itag,
            sys._getframe().f_code.co_name,
            'took',
            str(time.time() - sts) + 's',
        )

    def Analysis(
        self,
        *arg,
        ):
        self.test.Analysis(
            *arg,
        )