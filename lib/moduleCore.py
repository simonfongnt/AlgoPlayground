import sys
import os
import time
import glob

import pandas as pd
import pickle

from tensorflow import keras
from sklearn.model_selection import train_test_split


class ModuleBase():
    def __init__(
        self,
        ):
        # required params
        self.filePrefix = (
            self.filename.split('.')[0] + '-' + 
            self.classname + '-' + 
            str(int(time.time())) + '-'
        )
        self.ioText     = ''
        self.xprint     = None
        self.miscroot   = None

    # convert any fucking variable to string format
    def var2str(self, *text):
        return ' '.join(str(x) for x in [*text])

    def Config(
        self,
        xprint,
        miscroot,
        ):
        self.xprint     = xprint
        self.miscroot   = os.path.join(
                                miscroot,
                                self.filename.split('.')[0],
                                )
        # create directory if not exist
        try:
            os.makedirs(self.miscroot)
        except OSError as e:            
            pass
            # if e.errno != errno.EEXIST:
            #     raise

    def parse(
            self,
            topic,
            ):
        if      topic == '-h':
            topic = 'help'
        elif    topic == '-b':
            topic = 'backtest'
        return topic

    def Help(
        self,
        topic,
        ):
        topic = self.parse(topic)
        msg = ''
        if topic in self.helpinfo:
            for line in self.helpinfo[topic]:
                msg = msg + line + '\n'
        return msg

    def datasetInfo(
            self,
            x_train = None,
            x_val   = None,
            x_test  = None,
            y_train = None,
            y_val   = None,
            y_test  = None,
            ):
        
        if x_train is not None:
            self.AddioText(
                'x_train',
                x_train.shape,
                type(x_train),
            )
        if x_val is not None:
            self.AddioText(
                'x_val',
                x_val.shape,
                type(x_val),
            )
        if x_test is not None:
            self.AddioText(
                'x_test',
                x_test.shape,
                type(x_test),
            )
        if y_train is not None:
            self.AddioText(
                'y_train',
                y_train.shape,
                type(y_train),
            )
        if y_val is not None:
            self.AddioText(
                'y_val',
                y_val.shape,
                type(y_val),
            )
        if y_test is not None:
            self.AddioText(
                'y_test',
                y_test.shape,
                type(y_test),
            )

    def Module(
        self,
        ):
        return self.filename, self.classname

    def Info(
        self,
        ):
        msg = ''
        for line in self.info:
            msg = msg + line + '\n'
        return msg
        
    # convert any fucking variable to string format
    def var2str(self, *text):
        return ' '.join(str(x) for x in [*text])
            
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
            return False
    
    def GetioText(self):
        return self.ioText

class DataBase(
    ModuleBase,
    ):
    def __init__(
        self,
        ):
        ModuleBase.__init__(self)
        self.dataPack   = {}
        self.dir        = None
        self.output     = None
        self.raw        = {}

        # self.savepath   = None

        self.yCol       = 'TARGET'
        self.x          = None
        self.y          = None
        
        # output
        self.__resetOutput()

    def __resetOutput(
            self,
            ):
        self.output     = {
            'x_train':  None,
            'y_train':  None,
            'x_val':    None,
            'y_val':    None,
            'x_test':   None,
            'y_test':   None,
        }
        
    def __fromFile(
            self,
            root,
            filename,
            ):
        fPath = os.path.join(
                        root,
                        filename,
                        )
        fType = filename.split('.')[-1] # file extension

        if fType == 'csv':
            return pd.read_csv(
                        fPath,
                        sep=',',
                        )
        elif    fType == 'feather':
            return pd.read_feather(fPath)
        return None

    def Load(
        self,
        root,
        ):
        # Reset Output Variables
        self.__resetOutput()
        # Search for files
        path = os.path.join(
                    root,
                    )
        _, _, filenames = next(os.walk(path))

        for filename in filenames:
            # filename without extension matches dict key
            self.output[filename.split('.')[0]] = self.__fromFile(
                root,
                filename,
                )
        
        # Report Dataset Info
        self.ResetioText()
        self.datasetInfo(
            self.output['x_train'], 
            self.output['x_val'], 
            self.output['x_test'], 
            self.output['y_train'], 
            self.output['y_val'], 
            self.output['y_test'],
        )
        self.AddioText(
            self.classname,
            'Loaded from:\n',
            root,
        )
        self.xprint(
            self.GetioText()
        )

        return self.output['x_train'], self.output['x_val'], self.output['x_test'], self.output['y_train'], self.output['y_val'], self.output['y_test']

    def __toFile(
            self,
            data,
            root,
            filename,
            ):
        fPath = os.path.join(
                        root,
                        filename,
                        )
        fType = filename.split('.')[-1] # file extension
        if fType == 'csv':
            data.to_csv(
                            fPath, 
                            sep=',',
                            index=False,
                            # header=False,
                            # index=True,
                            # header=True,
                            )
        else:
            # default to feather
            data.to_feather(fPath)

    def Save(
        self, 
        root,
        traintestpc = 0.25,
        trainvalpc  = 0.25,
        ):

        # Reset Output Variables
        self.__resetOutput()
        # create folder if not exist
        try:
            os.makedirs(root)
        except OSError as e:
            pass

        files = glob.glob(root + '/*')
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                pass


        # divide dataset
        traintestpc = float(traintestpc)
        self.output['x_train'], self.output['x_test'], self.output['y_train'], self.output['y_test'] = train_test_split(
            self.x, 
            self.y, 
            test_size = traintestpc,
            )

        # divide dataset if necessary
        if trainvalpc and float(trainvalpc):
            trainvalpc = float(trainvalpc)
            self.output['x_train'], self.output['x_val'], self.output['y_train'], self.output['y_val'] = train_test_split(
                self.output['x_train'], 
                self.output['y_train'], 
                test_size = trainvalpc,
                )
            self.output['x_val'] = self.output['x_val'].reset_index(drop=True)
            self.output['y_val'] = self.output['y_val'].reset_index(drop=True)
            self.__toFile(
                self.output['x_val'],
                root,
                'x_val.feather',
            )
            self.__toFile(
                self.output['y_val'],
                root,
                'y_val.csv',
            )

        self.output['x_train']  = self.output['x_train'].reset_index(drop=True)
        self.output['x_test']   = self.output['x_test'] .reset_index(drop=True)
        self.output['y_train']  = self.output['y_train'].reset_index(drop=True)
        self.output['y_test']   = self.output['y_test'] .reset_index(drop=True)
        # save dataset to specific format
        self.__toFile(
            self.output['x_train'], 
            root,
            'x_train.feather',
        )
        self.__toFile(
            self.output['x_test'], 
            root,
            'x_test.feather',
        )
        self.__toFile(
            self.output['y_train'], 
            root,
            'y_train.csv',
        )
        self.__toFile(
            self.output['y_test'], 
            root,
            'y_test.csv',
        )
        
        # Report Dataset Info
        self.ResetioText()
        self.datasetInfo(
            self.output['x_train'], 
            self.output['x_val'], 
            self.output['x_test'], 
            self.output['y_train'], 
            self.output['y_val'], 
            self.output['y_test'],
        )
        self.AddioText(
            self.classname,
            'Saved to:\n',
            root,
        )
        self.xprint(
            self.GetioText()
        )

        return self.output['x_train'], self.output['x_val'], self.output['x_test'], self.output['y_train'], self.output['y_val'], self.output['y_test']


class ModelBase(
    ModuleBase,
    ):
    def __init__(
        self,
        ):
        ModuleBase.__init__(self)
        # required params
        self.modelPack  = {}
        self.x          = None
        self.y          = None
        self.x_train    = None
        self.y_train    = None
        self.x_val      = None
        self.y_val      = None
        self.trainset   = None
        self.valset     = None
        self.dataPack   = {}

        self.modelPath  = None
        self.model      = None
        self.history    = None

    def Init(
        self,
        x_train,
        x_val,
        y_train,
        y_val,
        dataPack = {},
        ):
        self.Dataset(
            x_train,
            x_val,
            y_train,
            y_val,
            dataPack,
        )

    def Dataset(
        self, 
        x_train,
        x_val,
        y_train,
        y_val,
        dataPack = {},
        ):
        self.x_train    = x_train
        self.x_val      = x_val
        self.y_train    = y_train
        self.y_val      = y_val
        self.dataPack   = dataPack
                
        # Report Dataset Info
        self.ResetioText()
        self.AddioText(
            'Train set:'
        )
        self.datasetInfo(
            x_train = self.x_train,
            y_train = self.y_train,
        )
        self.AddioText(
            'Validate set:'
        )
        self.datasetInfo(
            x_val   = self.x_val,
            y_val   = self.y_val,
        )
        self.AddioText(
            'dataPack keys:'
        )
        self.AddioText(
            self.dataPack.keys(),
        )
        self.xprint(
            self.GetioText()
        )

    def Load(
        self, 
        path = None,
        ):
        if not path:
            path = self.modelPath
            
        try:
            # Keras Load
            self.model = keras.models.load_model(
                path
                )
        except Exception as e:
            # Sklearn Load
            with open(path, 'rb') as mFile:
                self.model = pickle.load(
                    mFile
                )

        self.modelPath = path
        self.xprint(
            self.classname,
            'model',
            'Loaded from:\n',
            self.modelPath
        )


    def Save(
        self, 
        path = None,
        ):
        if not path:
            path = self.modelPath

        try:
            # Keras Save
            self.model.save(
                path,
                save_format='h5',
            )
        except Exception as e:
            # Sklearn Save
            with open(path, "wb") as mFile:
                pickle.dump(
                    self.model,
                    mFile,
                    )

        self.modelPath = path
        self.xprint(
            self.classname,
            'model',
            'Saved to:\n',
            self.modelPath
        )
        return self.modelPack

class TestBase(
    ModuleBase,
    ):
    def __init__(
        self,
        ):
        ModuleBase.__init__(self)

        self.x_test         = None
        self.y_test         = None
        self.dataPack       = {}
        self.modelPack      = {}

        self.modelPath      = None
        self.model          = None
        self.results        = None
        self.predictions    = None

        self.algoModel      = None
        self.aPath          = None

    def Init(
        self,
        x_test,
        y_test,
        modelPath,
        dataPack = {},
        modelPack = {},
        ):
        self.Dataset(
            x_test,
            y_test,
            dataPack,
        )
        self.modelPack  = modelPack
        self.modelPath  = modelPath
        self.Load(modelPath)
        
        # Report Dataset Info
        self.ResetioText()
        self.AddioText(
            'modelPack keys:'
        )
        self.AddioText(
            self.modelPack.keys(),
        )
        self.xprint(
            self.GetioText()
        )

    def Dataset(
        self, 
        x_test,
        y_test,
        dataPack = {},
        ):
        self.x_test     = x_test
        self.y_test     = y_test
        self.dataPack   = dataPack
                
        # Report Dataset Info
        self.ResetioText()
        self.AddioText(
            'Test set:'
        )
        self.datasetInfo(
            x_test  = self.x_test,
            y_test  = self.y_test,
        )
        self.AddioText(
            'dataPack keys:'
        )
        self.AddioText(
            self.dataPack.keys(),
        )
        self.xprint(
            self.GetioText()
        )

    def Load(
        self, 
        path = None,
        ):
        if not path:
            path = self.modelPath
            
        try:
            # Keras Load
            self.model = keras.models.load_model(
                path
                )
        except Exception as e:
            # Sklearn Load
            with open(path, 'rb') as mFile:
                self.model = pickle.load(
                    mFile
                )
                
        self.modelPath = path
        self.xprint(
            self.classname,
            'model',
            'Loaded from:\n',
            self.modelPath
        )

    def Save(
        self, 
        path     = None,
        ):
        if not path:
            path = self.modelPath

        try:
            # Keras Save
            self.model.save(
                path,
                save_format='h5',
            )
        except Exception as e:
            # Sklearn Save
            with open(path, "wb") as mFile:
                pickle.dump(
                    self.model,
                    mFile,
                    )

        self.modelPath = path
        self.xprint(
            self.classname,
            'model',
            'Saved to:\n',
            self.modelPath
        )