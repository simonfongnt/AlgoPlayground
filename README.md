# AlgoPlayground
ML requires dataset, model and tester. During development, any issues/changes to code will consume a great amount of time. This project allows code changes while the other result/params persist. 
e.g. if the dataset is ready, some changes is needed in model. The model can be reloaded after changes, and since dataset persists, it can be used immediately and save the time reconstructing the dataset.
## architecture
```
folder
|--config
|   |--const.json
|   |--login.json
|--data
|   |--raw
|--dist
|--lib
|   |--...
|--log
|--model
|--main.py
```
### model strucutre
```
theModel.py
|--model(): 
|   |--get()
|   |--Compile()
|   |--Fit()
|--tester()
|   |--get()
|   |--set()
|   |--Test()
```
### Usage
