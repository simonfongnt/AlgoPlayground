# Commands
commands are available for each threads shown as follows:

## -M modules (#modules)
display list of module with index in specific directory

| Thread | data | model | test |
| --- | --- | --- | --- |
| directory | lib/data/ | lib/model/ | lib/test/ |

e.g. 
```
> model modules
lib/model:
...
2:lib/model/SKLEARN_SVC_SAMPLE.py
3:lib/model/KERAS_NN_SAMPLE.py
```

## -m module (#module)
display list of module with index in specific directory

e.g. 
```
> model module
lib/model:
...
2:lib/model/SKLEARN_SVC_SAMPLE.py
3:lib/model/KERAS_NN_SAMPLE.py
