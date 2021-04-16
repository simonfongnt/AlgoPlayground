from lib.moduleCore import ModelBase
from lib.kerasTools import KerasTools

import sys
import os
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

class Model(
    ModelBase,
    KerasTools,
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
        KerasTools.__init__(self)
        self.__initParam()

    def __initParam(self):
        # Default Settings
        self.defaultVals  = {
            'Create':{
                'layerNodes': [16],
                'batch'     : 4,
                'dropout'   : 0.2,
            },
            'Compile':{
            },
            'Fit':{
                'epochs'    : 100,
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
        defaultVals     = self.defaultVals[sys._getframe().f_code.co_name]
        layerNodes      = defaultVals['layerNodes']
        dropout         = defaultVals['dropout']
        batch           = defaultVals['batch']
        if len(arg) > 0:
            layerNodes  = arg            

        # data preparation
        self.x_train.columns = [
            '0',
            '1',
            '2',
            ]
        self.x_val.columns = [
            '0',
            '1',
            '2',
            ]

        # y_label         = self.dataPack['LABEL']                # get params from Data Function
        self.y_train.columns = [                                # Or do it yourself
            '0',
            ]
        self.y_val.columns = [
            '0',
            ]
        y_label         = '0'
        self.y_train    = self.y_train['0']
        self.y_val      = self.y_val['0']
        labels          = set(self.y_train.values)

        self.trainset = tf.data.Dataset.from_tensor_slices(
            (dict(self.x_train), self.y_train),
        ).shuffle(len(self.x_train)).batch(batch)

        self.valset = tf.data.Dataset.from_tensor_slices(
            (dict(self.x_val), self.y_val),
        ).shuffle(len(self.x_val)).batch(batch)

        for feat, targ in self.trainset.take(2):
            self.xprint(
                'Features: {}, Target: {}'.format(feat, targ)
                )

        inputsDict = {
            'A': keras.Input(shape=(1,), name="0"),
            'B': keras.Input(shape=(1,), name="1"),
            'C': keras.Input(shape=(1,), name="2"),
        }
        inputs = [
            inputsDict.values(),
        ]
        features = layers.concatenate(
            [
                self.encode_numerical_feature(inputsDict['A'], "0",     self.trainset),
                self.encode_numerical_feature(inputsDict['B'], "1",     self.trainset),
                self.encode_numerical_feature(inputsDict['C'], "2",     self.trainset),
            ]
        )
        
        t = layers.Dense(
                layerNodes[0], 
                activation="relu"
                )(features)
        t = layers.Dropout(
                dropout
                )(t)
        for layerNode in layerNodes[1:]:
            t = layers.Dense(
                    layerNode, 
                    activation="relu"
                    )(t)
            t = layers.Dropout(
                    dropout
                    )(t)
        output = layers.Dense(
                1, 
                activation="sigmoid",
                )(t)
        self.model = keras.Model(inputs, output)
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

        optimizer = 'adam'
        # optimizer = 'sgd'

        loss = 'binary_crossentropy'
        
        # loss = 'mean_squared_error'
        metrics = [
            'accuracy',
            ]

        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics,
            )

        # print model summary
        msgls = []
        self.model.summary(print_fn=lambda x: msgls.append(x))
        msg = "\n".join(msgls)
        self.xprint(
            msg,
        )

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

        self.result =  self.model.fit(
            self.trainset,
            epochs      = epochs,
            validation_data = self.valset
        )

        self.modelPack['RESULT'] = self.result

        # list all data in history
        history = self.result.history
        
        # accuracy history
        path   = os.path.join(
                    self.miscroot,
                    self.filePrefix + sys._getframe().f_code.co_name + '-Accuracy.jpg',
                    )
        plt.plot(history['accuracy'])
        plt.plot(history['val_accuracy'])
        plt.title('model accuracy')
        plt.suptitle(path)
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
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
        # loss history
        path   = os.path.join(
                    self.miscroot,
                    self.filePrefix + sys._getframe().f_code.co_name + '-Loss.jpg',
                    )
        plt.plot(history['loss'])
        plt.plot(history['val_loss'])
        plt.title('model loss')
        plt.suptitle(path)
        plt.ylabel('loss')
        plt.xlabel('epoch')
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
        
        # # layer outputs and weights
        # self.ResetioText()

        # for layer in self.model.layers:
        #     self.AddioText(
        #         'output:',
        #         layer.output,
        #     )
        #     self.AddioText(
        #         'weights:',
        #         layer.get_weights(), # list of numpy arrays
        #     )
        # self.xprint(
        #     self.GetioText()
        # )

        self.xprint(
            'Accuracy:',
            history['accuracy'][-1],
            'Loss:',
            history['loss'][-1],
        )