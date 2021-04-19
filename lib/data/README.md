# Data Thread Modules

Data processing modules are located in this folder `lib/data/` and the raw data are located in `data/raw/`. 
> 1. Raw data at `data/raw/`
>     - e.g. `data/raw/RAWSAMPLE/ABC.csv``

Data Thread handles import of these modules by `data module` command. For more infomation, Use `data help` or read this (pending).

Basically, class `Raw` and `Create` are essential during the development.

## Module Class Format
`lib.moduleCore.DataBase` must be inherited in `class Data`. The mininal template is defined as follows:
```
from lib.moduleCore import DataBase
class Data(
    DataBase,
    ):

    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name

    # line by line string that reports to "data info" command
    info = []

    # line by line string that reports to "help" command
    helpinfo = {}

    def __init__(self,):
        DataBase.__init__(self)

    # module command passed by Data Thread
    def Command(self, cmds,):
        pass

    # Raw Directory is selected in Data Thread and pass to here
    def Raw(
        self,
        dir,    
        ):
        pass
    
    # default Create function be called by Data Thread
    def Create(
        self,
        ):
        self.x          = []
        self.y          = []
        self.dataPack   = {}
```
## Give and Take
Data Thread passes numbers of parameters to the loaded mobule and expects specific parameters for Model & Test threads.
```
Core Params:
self.filepath       # string, module path
self.filename       # string, file name of the module 
self.classname      # string, class name of the module

Available Functions:
self.xprint()       # display on console and messenger api
                    # e.g. self.xprint('123', '234')
                    
Available Params:
self.miscroot       # directory of the miscellaneous root
self.filePrefix     # suggested filename prefix in format <module name>-<thread name>-<timestamp>-

Expected Params:
self.x              # dataframe, computed features 
self.y              # dataframe, computed target
self.dataPack       # dictionary, to Model & Test thread modules
```
`Core params` must be defined and `Expected params` should be produced in the module. After the module is loaded, the `self.xprint()` function can be used and miscellaneous storage path (`self.miscroot`) plus the suggested filename prefix (`self.filePrefix`) are also generated.

For example, the `KERAS_NN_SAMPLE.py` `model` module can optionally use `self.miscroot` ([`misc/KERAS_NN_SAMPLE`](misc/README.md) folder) and `self.filePrefix` (`KERAS_NN_SAMPLE-Model-1618448689-`) for better file organization.

## Example: create datasets
`DATA_SAMPLE.py` uses the raw data at `data/raw/RAWSAMPLE/ABC.csv`.
1. Use `data modules` to list the data module
```
lib/data:
0:lib/data/DATA_SAMPLE.py
```
2. Use `data module 0` to load the example module
3. Use `data raws` to list the raw directories in `data/raw`
```
data/raw:
...
4:data/raw/RAWSAMPLE
...
```
4. Use `data raw 4` to pass raw directory path to module Class `Raw`
5. Use `data create` to compute `self.x`, `self.y` and `self.dataPack`
6. Use `data save` to create train set, validate set and test set files in `data/`
> WARNING: `data save` will remove and create all files in the folder.
7. Use `data to model` to pass the train set & validate set to Model thread
8. Use `data to test` to pass the test set to Test thread
> NOTE: `data to` requires modules to be loaded in target threads.

### Optional: load existing datasets
Assume the datasets have been created by `DATA_SAMPLE.py`, the existing datasets can be reused by replacing step 4-6 to:
- Use `data list` to list the dataset directories in `data/`
```
data:
...
4:data/DATA_SAMPLE
...
```
- Use `data load 4` to load the previous train set, validate set and test set files
