# Test Thread Modules

Model Test modules are located in this folder `lib/test/`.
> 4. model test code at `lib/test/`
>     - e.g. `lib/test/KERAS_NN_SAMPLE.py `

Test Thread handles import of these modules by `test module` command. For more infomation, Use `test help` or read this (pending).

Basically, class `Run` and `Export` are essential during the development.

## Model module (Model Trainning) Class Format
`lib.moduleCore.ModelBase` must be inherited in `class Model`. The mininal template is defined as follows:
```
from lib.moduleCore import TestBase

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
        return '''Some Description Here'''

    def Predict(
        self,
        argv,
        ):
        result = self.Model.predict(argv)[0]
        if result > self.threshold:
            return True
        return False

class Model(
    TestBase,
    ):

    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name

    # line by line string that reports to "data info" command
    info = []

    # line by line string that reports to "help" command
    helpinfo = {}

    def __init__(self,):
        TestBase.__init__(self)

    # module command passed by Test Thread
    def Command(self, cmds,):
        pass
    
    # default Export function be called by Test Thread
    def Export(
        self, 
        path        = None,
        *arg,
        ):
        algoModel = AlgoModel(
            self.model,
            *arg,
            )
        pickle.dump(algoModel, open(self.aPath, 'wb'))
        self.xprint(
            'Exported to:',
            self.aPath,
        )
        
    # default Analysis function be called by Test Thread
    def Analysis(
        self,
        *arg,
        ):
        pass
    
    # default Run function be called by Test Thread
    def Run(
        self,
        *arg,
        ):
        # Evaluate the model on the test data using `evaluate`
        results = self.model.evaluate(
            self.x,
            self.y,
            )
        
```
## Give and Take
Model Thread passes numbers of parameters to the mobules and expects specific parameters for Test Thread.
```
Core Params:
self.filepath       # module path
self.filename       # file name of the module 
self.classname      # class name of the module

Available Functions:
self.xprint()       # display on console and messenger api
                    # e.g. self.xprint('123', '234')

Available Params:
self.x_test         # train set features dataframe
self.y_test         # validate set features dataframe
```
`Core params` must be defined and `Expected params` should be produced in the module. After the module is loaded, the `self.xprint()` function can be used and miscellaneous storage path (`self.miscroot`) plus the suggested filename prefix (`self.filePrefix`) are also generated.

For example, the `KERAS_NN_SAMPLE.py` `model` module can optionally use `self.miscroot` ([`misc/KERAS_NN_SAMPLE`](misc) folder) and `self.filePrefix` (`KERAS_NN_SAMPLE-Model-1618448689-`) for better file organization.

It is also recommended to export the Algomodel consisted of the trained model by the `Export` function.

## Example: test a model
`SKLEARN_SVC_SAMPLE.py` uses the dataset from `DATA_SAMPLE.py` Data thread module and the trained model from `SKLEARN_SVC_SAMPLE.py` Model thread module.
1. Use `test modules` to list the data module
```
lib/test:
...
1:lib/test/SKLEARN_SVC_SAMPLE.py
...
```
2. Use [model module](COMMAND.md#modules) 1 to load the example module
3. [Create / Load Datasets](lib/data/README.md)
4. Use `[data save](COMMAND.md#save) 0.25 0` to ensure no validate set exists
5. Use `[data to](COMMAND.md#to) test` to obtain train set
6. [Create / Load Model](lib/test/README.md)
7. Use `[model to](COMMAND.md#to) test` to obtain trained model
8. Use `[test run](COMMAND.md#run)` to start testing
9. Use `[test analysis](COMMAND.md#analysis)` to verify Algomodel functions (optional)
10. Use `[test export](COMMAND.md#export)` to export Algomodel to `dist/`

### Optional: load existing model
Existing model can be loaded for testing by replacing step 6-7 to:
- Use `test list` to list the models in `model/`
```
model:
...
3:model/SKLEARN_SVC_SAMPLE
...
```
- Use `[test load](COMMAND.md#load) 3` to load previous trained and tested model in `model/`
