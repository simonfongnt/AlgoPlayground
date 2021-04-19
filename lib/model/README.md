# Model Thread Modules

Model Training modules are located in this folder `lib/model/`.
> 3. model training code at `lib/model/`
>     - e.g. `lib/model/KERAS_NN_SAMPLE.py`

Model Thread handles import of these modules by `model module` command. For more infomation, Use `model help` or read this (pending).

Basically, class `Create`, `Compile` and `Fit` are essential during the development.

## Module Class Format
`lib.moduleCore.ModelBase` must be inherited in `class Model`. The mininal template is defined as follows:
```
from lib.moduleCore import ModelBase
from lib.kerasTools import KerasTools   # for Keras model
class Model(
    ModelBase,
    KerasTools,                         # for Keras model
    ):

    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name

    # line by line string that reports to "data info" command
    info = []

    # line by line string that reports to "help" command
    helpinfo = {}

    def __init__(self,):
        ModelBase.__init__(self)
        KerasTools.__init__(self)       # for Keras model

    # module command passed by Model Thread
    def Command(self, cmds,):
        pass
    
    # default Create function be called by Model Thread
    def Create(
        self,
        *arg,
        ):
        self.model = keras.Model()

    # default Compile function to be called by Model Thread
    def Compile(
        self,
        *arg,
        ):
        self.model.compile()
    
    # default Fit function to be called by Model Thread
    def Fit(
        self,
        *arg,
        ):
        self.model.fit()
        self.modelPack = {}
        
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
self.miscroot       # directory of the miscellaneous root
self.filePrefix     # suggested filename prefix in format <module name>-<thread name>-<timestamp>-
self.x_train        # train set features dataframe
self.x_val          # validate set features dataframe
self.y_train        # train set target dataframe
self.y_val          # validate set target dataframe
self.dataPack       # parameters from Data thread module

Expected Params:
self.model          # trained model
self.modelPack      # optional dictionary to Test thread module
```
`Core params` must be defined and `Expected params` should be produced in the module. After the module is loaded, the `self.xprint()` function can be used and miscellaneous storage path (`self.miscroot`) plus the suggested filename prefix (`self.filePrefix`) are also generated.

For example, the `KERAS_NN_SAMPLE.py` `model` module can optionally use `self.miscroot` ([`misc/KERAS_NN_SAMPLE`](misc) folder) and `self.filePrefix` (`KERAS_NN_SAMPLE-Model-1618448689-`) for better file organization.

## Example: create and train a model
`SKLEARN_SVC_SAMPLE.py` uses the dataset from `DATA_SAMPLE.py` Data thread module.
1. Use `model modules` to list the data module
```
lib/model:
...
2:lib/model/SKLEARN_SVC_SAMPLE.py
...
```
2. Use `model module 2` to load the example module
3. [Create / Load Datasets](lib/data/README.md)
4. Use `data save 0.25 0` to ensure no validate set exists
5. Use `data to model` to obtain train set
6. Use `model create` to create the model (optional)
7. Use `model compile` to compile the model (optional)
8. Use `model fit` to train the model and save to `model/tmp`

### Optional: load existing model
Existing model can be loaded for training by replacing step 6 to:
- Use `model list` list the models in `model/`
```
model:
...
4:model/SKLEARN_SVC_SAMPLE
...
```
- Use `model load 4` to load previous trained and tested model in `model/`
