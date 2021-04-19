# Commands
commands are available for each threads shown as follows:

# General Commands
## kill

> kill data|model|test

kill running target thread `data`, `model` or `test`.

## help

> cmd... help

display help info of the command.

## list
Both script and threads have `list` command with different functionality:

> script list

list of scripts in `script/` directory or its subdirectory.

> data list [subdirectory...]

list of dataset folders in `data/` directory or its subdirectory.

> model list [subdirectory...]

list of models in `model/` directory or its subdirectory.

> test list [subdirectory...]

list of models in `model/` directory or its subdirectory.

## run

> script run [source]

execute script (last script without source) from `script/` directory or its subdirectory.

> test -r|run

test the model

# Thread Commands
The following commands are for threads only.

## modules

> data|model|test -M|modules [subdirectory...]

display list of module with index under specific module base directory. Index is usable in `module` command.

| thread | data | model | test |
| --- | --- | --- | --- |
| base | lib/data/ | lib/model/ | lib/test/ |

```
> model modules
lib/model:
...
2:lib/model/SKLEARN_SVC_SAMPLE.py
3:lib/model/KERAS_NN_SAMPLE.py
```
subdirectory can be specified but must be under the base directory.

```
> model modules subdir
lib/model/subdir:
...
0:lib/model/SKLEARN_SVC_SAMPLE.py
```

## module

> data|model|test -m|module [subdirectory...] [source]

import module (last module without source) from [specific module base directory](#modules)

```
> model modules
lib/model:
...
2:lib/model/SKLEARN_SVC_SAMPLE.py
3:lib/model/KERAS_NN_SAMPLE.py
>model module 2
model Import new lib: SKLEARN_SVC_SAMPLE
>model module SKLEARN_SVC_SAMPLE
model Import new lib: SKLEARN_SVC_SAMPLE
>model module
model Import new lib: SKLEARN_SVC_SAMPLE
```

## info

> data|model|test info

display info of the loaded module.

## init

> model|test -i|init

passes loaded dataset(s) and model to the loaded module.

## save
Threads have `save` command with different functionality:

> data -s|save [subdirectory...]

save datasets in `data/` directory (if not specified) or its subdirectory

> model -s|save [subdirectory...]

save model in `model/` directory (if not specified) or its subdirectory

> test -s|save [subdirectory...]

save model in `model/` directory (if not specified) or its subdirectory

## load
Threads have `load` command with different functionality:

> data -l|load [subdirectory...]

load datasets in `data/` directory or its subdirectory, which can be index of `data list` command.

> model -l|load [subdirectory...]

load model in `model/` directory or its subdirectory, which can be index of `model list` command.

> test -l|load [subdirectory...]

load model in `model/` directory or its subdirectory, which can be index of `test list` command.

## to
Threads have `to` command with different functionality:

> data -t|to model|test

Either send train set and validate set (if exists) to model thread, or send test set to test thread.

> model -t|to test

send model path in model.tmp directory to test thread

# Data Thread Commands
## raws

> data -R|raws [subdirectory...]

list of raw folders in `data/raw` directory or its subdirectory.

```
> data raws
data/raw:
4:data/raw/RAWSAMPLE
> data raw 4
```

## raw

> data -m|raw [subdirectory...] [source]

load raw data (last raw data without source) from [specific raw base directory](#raws)

```
> data raws
data/raw:
4:data/raw/RAWSAMPLE
> data raw 4
```

## create

> data -c|create [subdirectory...] [source]

create train set, validate set (if necessary) and test set.

# Model Thread Commands
## compile

> model -c|compile

compile the model

## fit

> model -f|fit

train the model


# Test Thread Commands

## analysis

> test -a|analysis

analysis algomodel consisted of the trained model

## export

> test -e|export [subdirectory...]

export the algomodel consisted of the trained model to `dist/` or its subdirectory

# Customized Commands
Apart from the default, command can also be defined inside a module. It is recommended to use the `helpinfo` to describe the commands as well. Let's take model module `KERAS_NN_SAMPLE.py` as an example:
```
class Model(
    ModelBase,
    ):
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
    # customized commands
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
    ......
```
commands will be passed to `Command` function by Model thread if it is not default command. Now `model help` command will the module command list shown at the end as follows:
```
>model module KERAS_NN_SAMPLE
>model help
INFO:
model creation
USAGE:
model option [source] [operation]
Option:
-h, help           display this file
-M, modules        display list of modules
-m, module         import module
-s, save           save model
-L, list           display list of models
-l, load           load model
-i, init           initialize model
-c, compile        compile model
-f, fit            fit model
-t, to             send model to other function
info               display module info
                   other unspecified options are sent to the loaded module
Source:
<index>            index of list command
<file>             actual filename
Operation:
-h, help           display help for option

INFO:
KERAS_NN_SAMPLE.py
USAGE:
test option [source] [operation]

>model summary help
INFO:
show summary.
USAGE:
test summary
```
then the command can simply be used
```
>model summary
print Summary
```
