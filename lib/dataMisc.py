from lib.hubCore import *

class dataClass(
            HubBase,
               ):

    def __init__(
        self,
        itag,
        otag,
        logPath,
        libroot,
        rawroot,
        dataroot,
        miscroot,
        ):
        self.itag       = itag
        self.otag       = otag
        self.logger     = Logger(
                                itag, 
                                logPath % (itag + '-' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")),
                                )

        self.libroot    = libroot
        self.rawroot    = rawroot
        self.dataroot   = dataroot
        self.miscroot   = miscroot

        HubBase     .__init__(self)
        self.__initParam()

    def __initParam(self):        
        self.cmddict    = {}

        self.data = None
        self.savepath   = None

        self.x          = None
        self.y          = None
        self.x_train    = None
        self.y_train    = None
        self.x_val      = None
        self.y_val      = None
        self.x_test     = None
        self.y_test     = None
        # self.dataPack   = None
        
        self.datas  = {}
        self.datas  = self.initDict(
                                self.datas,
                                self.dataroot,
                                None,
                            )
        self.raws   = {}
        self.raws   = self.initDict(
                                self.raws,
                                self.rawroot,
                                None,
                            )

    def Command(
        self,
        cmds,
        ):
        if self.data:
            self.data.Command(cmds)
    
    def Get(
        self,
        cmd,
        ):
        if   cmd.lower() == 'libname':
            return self.libname
        elif cmd.lower() == 'path':
            return self.libpath, self.savepath
        elif cmd.lower() == 'trainset':
            return self.x_train, self.y_train
        elif cmd.lower() == 'testset':
            return self.x_test, self.y_test
        elif cmd.lower() == 'shape':
            return self.x_train.shape, self.y_train.shape, self.x_test.shape, self.y_test.shape
        elif cmd.lower() == 'x_train':
            return self.x_train
        elif cmd.lower() == 'x_test':
            return self.x_test
        elif cmd.lower() == 'y_train':
            return self.y_train
        elif cmd.lower() == 'y_test':
            return self.y_test

    def Set(
        self,
        cmd,
        *arg,
        ):
        if   cmd.lower() == 'libname':
            self.libname   = arg[0]
        self.xprint(
            self.itag,
            sys._getframe().f_code.co_name,
            cmd,
        )
        
    def Raw(
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
        self.data.Raw(
                thePath,
            )

    def Save(
        self,
        *arg,
        ):
        root = self.dataroot
        name = self.data.filename.split('.')[0]

        arg     = self.rwParams(
                        self.classname,
                        sys._getframe().f_code.co_name,
                        'arg',
                        arg,
                    )

        self.savepath = os.path.join(
                        root,
                        name,
                        )

        self.x_train, self.x_val, self.x_test, self.y_train, self.y_val, self.y_test = self.data.Save(
                                                                self.savepath,
                                                                *arg,
                                                                )
        return (
            '%s: %s'%(
                sys._getframe().f_code.co_name,
                self.savepath,
                ),
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
        self.savepath = os.path.join(
                        root,
                        name,
                        )
        self.x_train, self.x_val, self.x_test, self.y_train, self.y_val, self.y_test = self.data.Load(
                                                                    self.savepath,
                                                                )

    def toFunc(
        self,
        func,
        argv,
        ):
        # self.mpQueue[func].put([
        self.thQueue[func].put([
            'dataset',
            *argv,
            ])
        # self.mpQueue[func].join()
        self.thQueue[func].join()

    def Create(
        self,
        ):
        sts = time.time()
        self.data.Create()
        self.xprint(
            self.itag,
            sys._getframe().f_code.co_name,
            'took',
            str(time.time() - sts) + 's',
        )