from lib.moduleCore import TestBase

from lib.hotfix     import *
from lib.database   import database

import sys
import os
import time

import numpy as np
import csv
import statistics
import pickle

import sklearn

class AlgoModel():
    # from tensorflow import keras
    def __init__(
            self,
            model,
            *finetune,
            ):
        self.Model = model
        self.threshold = 0.5
        if len(finetune) > 0:
            self.threshold = float(finetune[0])
    
    def Info(
        self,
        ):
        return '''SKLEARN_SVC_SAMPLE: e.g. AlgoModel.Predict([123, 234, 345, 456])'''

    def Predict(
        self,
        argv,
        ):
        # normalization
        L = argv[3]
        mlist = [(x - L) / L for x in argv]
        mlist = [[
            mlist[0],    # A,
            mlist[1],    # B,
            mlist[2],    # C,
        ]]
        result = self.Model.predict(mlist)[0]
        print(mlist, result)
        if result > self.threshold:
            return True
        return False

class Test(
    TestBase,
    ):
    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name
    
    # test info
    info = [
        filename,
        'model test',        
    ]

    # test help ...
    helpinfo = {
        "help":[
                "INFO:",
                filename,
                "USAGE:",
                "test option [source] [operation]",
                ""
            ],
        "history":[
                "INFO:",
                'show history.',
                "USAGE:",
                "test history",
                ""
            ],
    }

    def __init__(
        self,
        ):
        self.__initParam()
        TestBase.__init__(self)

    def __initParam(self):
        self.defaultVals  = {
            'Export':{
            },
            'Init':{
            },
            'Run':{
            },
            'Analysis':{
            },
        }

    def Command(
        self,
        cmds,
        ):
        if 0:
            pass
        elif(
            cmds[0] == 'history'
            ):
            self.xprint('show some history')
        
    def Export(
        self, 
        path        = None,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        if len(arg) > 0:
            pass
        
        if path:
            self.aPath = os.path.join(
                            path,
                            self.filePrefix + 'AlgoModel.pkl',
                            )
        if not self.aPath:
            return
        algoModel = AlgoModel(
            self.model,
            *arg,
            )
        pickle.dump(algoModel, open(self.aPath, 'wb'))
        self.xprint(
            'Exported to:',
            self.aPath,
        )

    def Analysis(
        self,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        if len(arg) > 0:
            pass

        # Create AlgoModel for usage
        model = AlgoModel(
            self.model,
            *arg,
            )

        # Show some result
        msg = 'analysis...\n'
        msg = msg + model.Info() + '\n'
        result = model.Predict(
            [200000, 20001, 20000, 20004],
            )
        msg = msg + 'result: ' + str(result)
        self.xprint(
            msg
            )
            
        # Save result to path
        path   = os.path.join(
                    self.miscroot,
                    self.filePrefix + sys._getframe().f_code.co_name + '.csv',
                    )
        mFile = open(
            path,
            "w",
            )
        mFile.write(msg)
        mFile.close()

        # Show result path
        self.xprint(
            'Result to:',
            path,
        )

    def Run(
        self,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        if len(arg) > 0:
            pass
        
        # test
        predictions = self.model.predict(self.x_test)
        cMatrix     = sklearn.metrics.multilabel_confusion_matrix(
            predictions, 
            self.y_test
            )
        score       = sklearn.metrics.accuracy_score(
            predictions, 
            self.y_test
            )

        self.ResetioText()

        self.AddioText(
            'Accuracy Score:',
            score,
        )
        
        self.AddioText(
            'Confusion Matrix:',
        )
        self.AddioText(
            cMatrix,
        )

        self.xprint(
            self.GetioText()
        )