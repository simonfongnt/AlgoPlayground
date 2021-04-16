from lib.moduleCore import ModelBase

import sys
import os
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics

import matplotlib.pyplot as plt

class Model(
    ModelBase,
    ):
    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name

    # model info
    info = [
        filename,
        'model creation',        
    ]

    # model help ...
    helpinfo = {
        "help":[
                "INFO:",
                filename,
                "USAGE:",
                "test option [source] [operation]",
                ""
            ],
        "summary":[
                "INFO:",
                'show summary.',
                "USAGE:",
                "test summary",
                ""
            ],
    }

    def __init__(
        self,
        ):
        ModelBase.__init__(self)
        self.__initParam()

    def __initParam(self):
        # Default Settings
        self.defaultVals  = {
            'Create':{
                'batch': 4,
                'layerNodes': [16],
                'dropout'   : 0.2,
            },
            'Compile':{
            },
            'Fit':{
                'epochs': 100,
            },
        }
        self.modelPack  = {
            'RESULT': None,
        }
        
    def Command(
        self,
        cmds,
        ):
        if (
            cmds[0] == 'summary'
            ):            
            self.xprint(
                'print Summary'
                )
        return
                
    def Create(
        self,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        layerNodes  = defaultVals['layerNodes']
        dropout     = defaultVals['dropout']
        batch       = defaultVals['batch']
        if len(arg) > 0:
            layerNodes = arg

        self.model = make_pipeline(
            StandardScaler(), 
            SVC(
                gamma='auto'
                ),
            )
        return self.model

    def Compile(
        self,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        # layerNodes = defaultVals['layerNodes']
        if len(arg) > 0:
            pass

        return self.model

    def Fit(
        self,
        *arg,
        ):
        # custom setting?
        defaultVals = self.defaultVals[sys._getframe().f_code.co_name]
        epochs = defaultVals['epochs']
        if len(arg) > 0:
            epochs = int(arg[0])

        self.result = self.model.fit(
            self.x_train,
            self.y_train,
        )

        scores = cross_val_score(
            self.result, 
            self.x_train, 
            self.y_train, 
            cv = 6,
            )

        predictions = cross_val_predict(
            self.model, 
            self.x_train, 
            self.y_train, 
            cv = 6
            )

        self.modelPack['RESULT'] = self.result

        # # list all data in history
        # history = self.result.history
        
        # accuracy history
        path   = os.path.join(
                    self.miscroot,
                    self.filePrefix + sys._getframe().f_code.co_name + '-Accuracy.jpg',
                    )
        plt.scatter(self.y_train, predictions)
        plt.title('model accuracy')
        plt.suptitle(path)
        plt.ylabel('true')
        plt.xlabel('predict')
        plt.legend(['train', 'val'], loc='upper left')
        # plt.show()
        # Save result to file
        plt.savefig(
            path,
            )
        plt.clf()
        plt.close()
        self.xprint(
            path,
        )

        # print metrics
        self.xprint(
            'Cross-Validate Scores:',
            scores,
        )