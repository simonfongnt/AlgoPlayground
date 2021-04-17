# Welcome to AlgoPlayground
This is a project template for machine learning. Machine learning requires data processing, model training and testing. During the development, any issues/changes to code would consume a great amount of time. This template allows code changes while the result/params persist. 

## Required Packages
```
tensorflow
pandas
python-telegram-bot
scikit-learn
sqlalchemy
matlotlib
pyarrow
```

## Structure
Data processing requires raw files located in `data/raw/` and code in `lib/data/`. Model Trainning code are in `lib/model/`. Model Test codes are in `lib/test/`. After the preprocessing, dataset will be stored in `data/` separated in train set, validation set and test set. Model Training accepts the train set (and validation set) to train and save the model to `model/tmp`. Model Test collects the test set and trained model to run the test and save in `model/`. Once the model is good, it can be exported as Algomodel to `dist/`.

The file and folder names in the following architecture are used as example for demostration.
```
root
|--config                       : configuration folder
|   |--path.json                : path specification
|   |--login.json               : login details (e.g. telegram, ...)
|--data                         : data folder
|   |--raw                      : raw data folder
|   |   |--RAWSAMPLE
|   |   |   |--ABC.csv
|   |   |--...
|   |--DATA_SAMPLE              : dataset folder
|   |   |--x_train.feather
|   |   |--y_train.csv
|   |   |--...
|--dist                         : exported algomodel
|   |--KERAS_NN_SAMPLE          : algomodel folder 
|   |   |--KERAS_NN_SAMPLE-Test-1618449908-AlgoModel
|   |   |--...
|   |--SKLEARN_SVC_SAMPLE
|   |   |--SKLEARN_SVC_SAMPLE-Test-1618449908-AlgoModel
|   |   |--...
|--lib                          : modules
|   |--data                     : data modules
|   |   |--DATA_SAMPLE.py       
|   |--model                    : model modules
|   |   |--KERAS_NN_SAMPLE.py
|   |   |--SKLEARN_SVC_SAMPLE.py
|   |--test                     : test modules
|   |   |--KERAS_NN_SAMPLE.py
|   |   |--SKLEARN_SVC_SAMPLE.py
|   |--...
|--log                          : logs
|--model                        : trained / untrained model folder
|   |--tmp                      : untrained models
|   |   |--KERAS_NN_SAMPLE
|   |   |--SKLEARN_SVC_SAMPLE
|   |--KERAS_NN_SAMPLE
|   |--SKLEARN_SVC_SAMPLE
|--misc                         : miscellaneous (image, result)
|--script                       : script (shortcut of commands)
|   |--KERAS_NN_SAMPLE.txt
|   |--SKLEARN_SVC_SAMPLE.txt
|--main.py
```
The path constants required in this template are defined in `config/path.json` and `config/login.json` for login details (optional). Scripts, logs and miscellaneous files are stored in their directories as well.

## Required files for a project
Development requires the following files located in specific locations.
1. Raw data at `data/raw/`
    - e.g. `data/raw/RAWSAMPLE/ABC.csv`
2. data preprocessing code at `lib/data/`
    - e.g. `lib/data/DATA_SAMPLE.py `
3. model training code at `lib/model/`
    - e.g. `lib/model/KERAS_NN_SAMPLE.py`
4. model test code at `lib/test/`
    - e.g. `lib/test/KERAS_NN_SAMPLE.py `

## Usage
Dataset, model and algomodel can be generated by commands / scripts. This template runs with commpand prompt which accepts commands or scripts.
### Commands
Command has specific functions in each modules. Use `help` command shows details of each of them.


data option ...    dataset preprocessing, data -h for [more info](lib/data/help.json)
model option ...   model creation, model -h for [more info](lib/model/help.json)
test option ...    model test, test -h for [more info](lib/test/help.json)
kill option ...    kill running thread, kill -h for [more info](lib/script/help.json)
script option ...  automation, script -h for [more info](lib/script/help.json)


### Scripts
Script is a set of commands. 
Use `script list` to list out scripts in `scripts/`
```
>script list
script:
0:script/KERAS_NN_SAMPLE.txt
1:script/SKLEARN_SVC_SAMPLE.txt
```
Use `script run` to run the script by name or index of `script list`
```
>script run 0
>script run KERAS_NN_SAMPLE
```
Example Scripts (script/KERAS_NN_SAMPLE.txt) with description:
```
data module DATA_SAMPLE         # load DATA_SAMPLE.py in lib/data/
model module KERAS_NN_SAMPLE    # load KERAS_NN_SAMPLE.py in lib/model/
test module KERAS_NN_SAMPLE     # load KERAS_NN_SAMPLE.py in lib/test/
data raw RAWSAMPLE              # load RAWSAMPLE folder in data/raw/
data create                     # create dataset from raw
data save 0.25 0.25             # save datasets to data/DATA_SAMPLE/
data to model                   # share dataset to model module
data to test                    # share dataset to test module
model create                    # create model
model compile                   # compile model
model fit                       # train model & save to model/tmp
model to test                   # share model to test module
test run                        # run model test
test save                       # save model to model/
test analysis                   # test algomodel
test export                     # export algomodel to dist/
```

## Algomodel
- Algomodel is the final product saved by pickle in `dist/`.
    - e.g. `dist/KERAS_NN_SAMPLE/KERAS_NN_SAMPLE-Test-1618449908-AlgoModel`

### Usage
The algomodel can simply be loaded and use as follows.
```
# load the AlgoModel
path = `dist/KERAS_NN_SAMPLE/KERAS_NN_SAMPLE-Test-1618449908-AlgoModel`
with open(path, 'rb') as mFile:
    model = pickle.load(
        mFile
    )

# display its info
print(model.Info()) 
# KERAS_NN_SAMPLE: e.g. AlgoModel.Predict([123, 234, 345, 456])

# predict with params
result = model.Predict([123, 234, 345, 456])    
# False
```
## Telegram (Optional)
Update the details in `config/login.json` to remote control the program via Telegram. 
